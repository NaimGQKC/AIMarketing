"""
VisiMind — Dashboard API Router
GET /api/dashboard/metrics | alerts | trend | protocols

All metrics computed from real DB data — no hardcoded mock values.
"""
import json
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def _brand_filter(brand_id: Optional[str], column: str = "brand_id"):
    """Return (WHERE clause, params) for optional brand filtering."""
    if brand_id and brand_id != "all":
        return f" AND {column} = ?", (brand_id,)
    return "", ()


@router.get("/metrics")
async def get_metrics(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """KPI summary for the Command Center — all values computed from DB."""
    bf, bp = _brand_filter(brand_id)

    # 1. Inference Alignment — derived from signal gaps severity
    cursor = await db.execute(
        f"SELECT severity, ai_response_quality FROM signal_gaps WHERE 1=1{bf}", bp
    )
    gaps = await cursor.fetchall()

    if gaps:
        total = len(gaps)
        critical = sum(1 for g in gaps if g["severity"] == "critical")
        warning = sum(1 for g in gaps if g["severity"] == "warning")
        avg_quality = sum(g["ai_response_quality"] for g in gaps) / total
        inference_score = round(avg_quality, 1)
    else:
        inference_score = 0.0

    # 2. Active remediations
    cursor = await db.execute(
        f"SELECT COUNT(*) as c FROM fix_kits WHERE status = 'ready'{bf}", bp
    )
    active = (await cursor.fetchone())["c"]

    # 3. Verified fixes
    cursor = await db.execute(
        f"SELECT COUNT(*) as c FROM audit_runs WHERE status = 'passed'{bf}", bp
    )
    verified = (await cursor.fetchone())["c"]

    # 4. Token density — compute from parity stats or probe data
    cursor = await db.execute("SELECT * FROM parity_stats LIMIT 1")
    parity = await cursor.fetchone()
    if parity:
        # Token density = ratio of EN efficiency vs FR overhead
        en_tokens = parity["en_avg_tokens"] or 1
        fr_tokens = parity["fr_avg_tokens"] or 1
        # Higher = better. 100 means no overhead; lower means FR is bloated
        token_density = round(min(100, (en_tokens / fr_tokens) * 100), 1)
    else:
        token_density = 0.0

    # 5. Trends — compute from e_score_history (compare latest vs previous)
    cursor = await db.execute(
        f"""SELECT e_score, created_at FROM e_score_history
            WHERE 1=1{bf} ORDER BY created_at DESC LIMIT 2""", bp
    )
    e_rows = await cursor.fetchall()

    if len(e_rows) >= 2:
        latest_e = e_rows[0]["e_score"]
        prev_e = e_rows[1]["e_score"]
        inference_trend = round((latest_e - prev_e) / max(prev_e, 0.01) * 100, 1)
    elif len(e_rows) == 1:
        inference_trend = 0.0
    else:
        inference_trend = 0.0

    # Active remediations trend — compare ready vs deployed
    cursor = await db.execute(
        f"SELECT COUNT(*) as c FROM fix_kits WHERE status = 'deployed'{bf}", bp
    )
    deployed = (await cursor.fetchone())["c"]
    remediations_trend = active - deployed  # positive = more pending work

    # Verified trend — count recent passes vs fails
    cursor = await db.execute(
        f"SELECT COUNT(*) as c FROM audit_runs WHERE status = 'failed'{bf}", bp
    )
    failed = (await cursor.fetchone())["c"]
    verified_trend = verified - failed

    # Token density trend — parity gap between EN and FR visibility
    if parity:
        en_vis = parity["en_visibility"] or 0
        fr_vis = parity["fr_visibility"] or 0
        # Positive = FR is catching up, negative = FR falling behind
        token_density_trend = round(fr_vis - en_vis, 1)
    else:
        token_density_trend = 0.0

    return {
        "inference_score": inference_score,
        "active_remediations": active,
        "verified_fixes": verified,
        "token_density": token_density,
        "inference_score_trend": inference_trend,
        "active_remediations_trend": remediations_trend,
        "verified_fixes_trend": verified_trend,
        "token_density_trend": token_density_trend,
    }


@router.get("/alerts")
async def get_alerts(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Red alert queries — derived from signal_gaps with toxic citations."""
    bf, bp = _brand_filter(brand_id, "sg.brand_id")
    query = f"""SELECT sg.id, sg.query, sg.severity, sg.lang,
                  sg.source_of_hallucination_label as issue,
                  CASE sg.source_of_hallucination_url
                       WHEN NULL THEN 'Google AI Mode'
                       ELSE 'SearchGPT'
                  END as agent
           FROM signal_gaps sg
           WHERE 1=1{bf}
           ORDER BY CASE sg.severity WHEN 'critical' THEN 0 ELSE 1 END, sg.created_at DESC"""

    cursor = await db.execute(query, bp)
    rows = await cursor.fetchall()
    return [
        {
            "id": r["id"],
            "query": r["query"],
            "agent": r["agent"],
            "issue": f"Citing: {r['issue']}",
            "severity": r["severity"],
            "lang": r["lang"],
        }
        for r in rows
    ]


@router.get("/trend")
async def get_trend(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Alignment trend — from alignment_trend table (seeded from real audit data)."""
    cursor = await db.execute(
        "SELECT day, en_score as en, fr_score as fr FROM alignment_trend ORDER BY id"
    )
    rows = await cursor.fetchall()

    if rows:
        return [dict(r) for r in rows]

    # If no trend data exists yet, return empty array — frontend should handle this
    return []


@router.get("/protocols")
async def get_protocols(db: aiosqlite.Connection = Depends(get_db)):
    """UCP/MCP connection health — derived from actual PIM connections."""
    # MCP is the dominant standard — 97M+ monthly SDK downloads, governed by Linux Foundation Agentic AI Foundation.
    cursor = await db.execute(
        """SELECT provider, status, last_sync, items_synced, errors
           FROM pim_connections ORDER BY provider"""
    )
    rows = await cursor.fetchall()

    if not rows:
        return []

    protocols = {}
    for r in rows:
        provider = r["provider"]
        # Map providers to protocol groups
        if provider in ("shopify", "akeneo"):
            proto = "UCP (Google)"
        elif provider in ("peec", "otterly"):
            proto = "MCP (Anthropic)"
        else:
            proto = provider

        if proto not in protocols:
            protocols[proto] = {
                "name": proto,
                "status": "disconnected",
                "lastPing": "never",
                "feeds": 0,
            }

        entry = protocols[proto]
        entry["feeds"] += r["items_synced"] or 0

        # Status: connected if any provider in the group is connected
        if r["status"] == "connected":
            entry["status"] = "connected"

        # Last ping: use the most recent sync time
        if r["last_sync"]:
            try:
                sync_time = datetime.fromisoformat(r["last_sync"])
                delta = datetime.utcnow() - sync_time
                seconds = int(delta.total_seconds())
                if seconds < 60:
                    entry["lastPing"] = f"{seconds}s ago"
                elif seconds < 3600:
                    entry["lastPing"] = f"{seconds // 60}m ago"
                elif seconds < 86400:
                    entry["lastPing"] = f"{seconds // 3600}h ago"
                else:
                    entry["lastPing"] = f"{seconds // 86400}d ago"
            except (ValueError, TypeError):
                pass

    return list(protocols.values())
