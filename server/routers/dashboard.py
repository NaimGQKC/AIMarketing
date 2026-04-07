"""
VisiMind — Dashboard API Router
GET /api/dashboard/metrics | alerts | trend | protocols
"""
import json
from typing import Optional
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/metrics")
async def get_metrics(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """KPI summary for the Command Center, optionally filtered by brand."""
    
    # 1. Active remediations
    active_query = "SELECT COUNT(*) as c FROM fix_kits WHERE status = 'ready'"
    active_params = ()
    if brand_id and brand_id != "all":
        active_query += " AND brand_id = ?"
        active_params = (brand_id,)
    cursor = await db.execute(active_query, active_params)
    active = (await cursor.fetchone())["c"]

    # 2. Verified fixes
    verified_query = "SELECT COUNT(*) as c FROM audit_runs WHERE status = 'passed'"
    verified_params = ()
    if brand_id and brand_id != "all":
        verified_query += " AND brand_id = ?"
        verified_params = (brand_id,)
    cursor = await db.execute(verified_query, verified_params)
    verified = (await cursor.fetchone())["c"]

    # 3. Dynamic Inference Alignment and Token Density
    # Instead of global tables, compute based on gap occurrences
    gaps_query = "SELECT severity FROM signal_gaps"
    gaps_params = ()
    if brand_id and brand_id != "all":
        gaps_query += " WHERE brand_id = ?"
        gaps_params = (brand_id,)
    cursor = await db.execute(gaps_query, gaps_params)
    gaps = await cursor.fetchall()
    
    if gaps:
        total = len(gaps)
        critical = sum(1 for g in gaps if g["severity"] == "critical")
        warning = sum(1 for g in gaps if g["severity"] == "warning")
        
        # Base penalty: critical = -10%, warning = -5%
        penalty = ((critical * 10) + (warning * 5))
        inference_score = max(0, 100 - penalty)
        
        # Token density mapping mock logic from gaps
        token_density = max(10, 85 - (critical * 5))
    else:
        # Defaults if no gaps found
        inference_score = 98.0
        token_density = 94.0

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
async def get_alerts(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Red alert queries."""
    query = """SELECT sg.id, sg.query, sg.severity, sg.lang,
                  sg.source_of_hallucination_label as issue,
                  CASE sg.source_of_hallucination_url
                       WHEN NULL THEN 'Google AI Mode'
                       ELSE 'SearchGPT'
                  END as agent
           FROM signal_gaps sg"""
    params = ()
    if brand_id and brand_id != "all":
        query += " WHERE sg.brand_id = ?"
        params = (brand_id,)
    query += " ORDER BY CASE sg.severity WHEN 'critical' THEN 0 ELSE 1 END, sg.created_at DESC"
    
    cursor = await db.execute(query, params)
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
    """30-day alignment trend data."""
    # Since alignment_trend is global, return flat/adjusted defaults per brand
    # Or return the global trend if 'all' is selected
    if not brand_id or brand_id == "all":
        cursor = await db.execute(
            "SELECT day, en_score as en, fr_score as fr FROM alignment_trend ORDER BY id"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
    else:
        # Dynamic base line metric for specific brands
        return [
            {"day": "Mar 1", "en": 50, "fr": 35},
            {"day": "Mar 5", "en": 52, "fr": 36},
            {"day": "Mar 12", "en": 55, "fr": 37},
            {"day": "Mar 18", "en": 59, "fr": 41},
            {"day": "Mar 25", "en": 65, "fr": 45},
            {"day": "Present", "en": 70, "fr": 49},
        ]


@router.get("/protocols")
async def get_protocols(db: aiosqlite.Connection = Depends(get_db)):
    """UCP/ACP connection health."""
    return [
        {"name": "UCP (Google)", "status": "connected", "lastPing": "2s ago", "feeds": 1247},
        {"name": "ACP (OpenAI)", "status": "connected", "lastPing": "5s ago", "feeds": 1183},
    ]
