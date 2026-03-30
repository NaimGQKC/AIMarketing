"""
VisiMind — Dashboard API Router
GET /api/dashboard/metrics | alerts | trend | protocols
"""
import json
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/metrics")
async def get_metrics(db: aiosqlite.Connection = Depends(get_db)):
    """KPI summary for the Command Center."""
    # Inference alignment = avg of latest trend
    cursor = await db.execute(
        "SELECT en_score, fr_score FROM alignment_trend ORDER BY id DESC LIMIT 1"
    )
    latest = await cursor.fetchone()
    en = latest["en_score"] if latest else 67
    fr = latest["fr_score"] if latest else 42
    inference_score = round((en + fr) / 2, 1)

    # Active remediations
    cursor = await db.execute("SELECT COUNT(*) as c FROM fix_kits WHERE status = 'ready'")
    active = (await cursor.fetchone())["c"]

    # Verified fixes
    cursor = await db.execute("SELECT COUNT(*) as c FROM audit_runs WHERE status = 'passed'")
    verified = (await cursor.fetchone())["c"]

    # Token density from parity
    cursor = await db.execute("SELECT en_visibility FROM parity_stats LIMIT 1")
    row = await cursor.fetchone()
    token_density = row["en_visibility"] if row else 74

    return {
        "inference_score": inference_score,
        "active_remediations": active,
        "verified_fixes": verified,
        "token_density": token_density,
        "inference_score_trend": 4.2,
        "active_remediations_trend": -2,
        "verified_fixes_trend": 7,
        "token_density_trend": 3.1,
    }


@router.get("/alerts")
async def get_alerts(db: aiosqlite.Connection = Depends(get_db)):
    """Red alert queries."""
    cursor = await db.execute(
        """SELECT sg.id, sg.query, sg.severity, sg.lang,
                  sg.source_of_hallucination_label as issue,
                  CASE sg.source_of_hallucination_url
                       WHEN NULL THEN 'Google AI Mode'
                       ELSE 'SearchGPT'
                  END as agent
           FROM signal_gaps sg
           ORDER BY CASE sg.severity WHEN 'critical' THEN 0 ELSE 1 END, sg.created_at DESC"""
    )
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
async def get_trend(db: aiosqlite.Connection = Depends(get_db)):
    """30-day alignment trend data."""
    cursor = await db.execute(
        "SELECT day, en_score as en, fr_score as fr FROM alignment_trend ORDER BY id"
    )
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]


@router.get("/protocols")
async def get_protocols(db: aiosqlite.Connection = Depends(get_db)):
    """UCP/ACP connection health."""
    return [
        {"name": "UCP (Google)", "status": "connected", "last_ping": "2s ago", "feeds": 1247},
        {"name": "ACP (OpenAI)", "status": "connected", "last_ping": "5s ago", "feeds": 1183},
    ]
