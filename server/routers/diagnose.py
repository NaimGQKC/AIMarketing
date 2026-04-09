"""
VisiMind — Diagnose API Router
GET/POST /api/diagnose/gaps | parity | probe | fertility
Includes polling-based probe task: POST returns task_id, GET /api/tasks/{id} for progress.
"""
import json
import uuid
import asyncio
from typing import Optional
from fastapi import APIRouter, Depends, BackgroundTasks
import aiosqlite

from database import get_db
from models import ProbeRequest
from engines.inference_lab import run_probe_task
from engines.bilingual_bridge import calculate_fertility, compare_fertility

router = APIRouter(prefix="/api/diagnose", tags=["diagnose"])


@router.get("/gaps")
async def get_signal_gaps(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Signal gap table with toxic citations, optionally filtered by brand."""
    query_str = "SELECT * FROM signal_gaps"
    params = ()
    
    if brand_id and brand_id != "all":
        query_str += " WHERE brand_id = ?"
        params = (brand_id,)
        
    query_str += " ORDER BY CASE severity WHEN 'critical' THEN 0 ELSE 1 END"
    
    cursor = await db.execute(query_str, params)
    rows = await cursor.fetchall()

    return [
        {
            "id": r["id"],
            "query": r["query"],
            "lang": r["lang"],
            "gap_type": r["gap_type"],
            "severity": r["severity"],
            "ai_response_quality": r["ai_response_quality"],
            "source_of_truth": {
                "label": r["source_of_truth_label"],
                "url": r["source_of_truth_url"],
                "detail": r["source_of_truth_detail"],
            },
            "source_of_hallucination": {
                "label": r["source_of_hallucination_label"],
                "url": r["source_of_hallucination_url"],
                "detail": r["source_of_hallucination_detail"],
            },
            "ai_said": r["ai_said"],
            "brand_truth": r["brand_truth"],
        }
        for r in rows
    ]


@router.get("/gaps/{gap_id}")
async def get_gap_detail(gap_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Detail view for a single signal gap."""
    cursor = await db.execute("SELECT * FROM signal_gaps WHERE id = ?", (gap_id,))
    r = await cursor.fetchone()
    if not r:
        return {"error": "Gap not found"}

    return {
        "id": r["id"],
        "query": r["query"],
        "lang": r["lang"],
        "gap_type": r["gap_type"],
        "severity": r["severity"],
        "ai_response_quality": r["ai_response_quality"],
        "source_of_truth": {
            "label": r["source_of_truth_label"],
            "url": r["source_of_truth_url"],
            "detail": r["source_of_truth_detail"],
        },
        "source_of_hallucination": {
            "label": r["source_of_hallucination_label"],
            "url": r["source_of_hallucination_url"],
            "detail": r["source_of_hallucination_detail"],
        },
        "ai_said": r["ai_said"],
        "brand_truth": r["brand_truth"],
    }


@router.get("/gaps/{gap_id}/fix-kit")
async def get_gap_fix_kit(gap_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Get the fix kit associated with a specific signal gap's product/brand."""
    cursor = await db.execute("SELECT brand_id, product_id FROM signal_gaps WHERE id = ?", (gap_id,))
    gap = await cursor.fetchone()
    if not gap:
        return None

    # Try to find a kit matching the gap's product first, then any kit for the brand
    cursor = await db.execute(
        """SELECT fk.*, b.name as brand_name, p.name_en as product_name
           FROM fix_kits fk
           JOIN brands b ON fk.brand_id = b.id
           LEFT JOIN products p ON fk.product_id = p.id
           WHERE fk.brand_id = ?
           ORDER BY CASE WHEN fk.product_id = ? THEN 0 ELSE 1 END
           LIMIT 1""",
        (gap["brand_id"], gap["product_id"]),
    )
    kit = await cursor.fetchone()
    if not kit:
        return None

    return {
        "id": kit["id"],
        "type": kit["type"],
        "brand": kit["brand_name"],
        "product": kit["product_name"] or "General",
        "status": kit["status"],
        "payload": json.loads(kit["payload"]) if kit["payload"] else None,
        "impact": kit["impact"],
    }


@router.get("/parity")
async def get_parity(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """EN/FR reasoning parity stats, computed live from signal_gaps per brand."""
    # Build brand filter
    where_clause = ""
    params = ()
    if brand_id and brand_id != "all":
        where_clause = " WHERE brand_id = ?"
        params = (brand_id,)

    # Count EN vs FR gaps and compute visibility from ai_response_quality
    cursor = await db.execute(
        f"SELECT lang, COUNT(*) as cnt, AVG(ai_response_quality) as avg_quality FROM signal_gaps{where_clause} GROUP BY lang",
        params,
    )
    rows = await cursor.fetchall()

    en_queries = 0
    fr_queries = 0
    en_avg_quality = 0
    fr_avg_quality = 0

    for r in rows:
        if r["lang"] == "EN":
            en_queries = r["cnt"]
            en_avg_quality = r["avg_quality"] or 0
        elif r["lang"] == "FR":
            fr_queries = r["cnt"]
            fr_avg_quality = r["avg_quality"] or 0

    total_queries = en_queries + fr_queries

    # Visibility = proportion of queries where brand is reasonably represented
    # Higher ai_response_quality means better visibility; invert gap severity into a score
    # Base visibility from quality scores (0-100 scale, quality represents how well brand appeared)
    # A gap with quality 80 means brand was 80% visible; quality 20 means only 20% visible
    en_visibility = round(en_avg_quality, 1) if en_queries > 0 else 0
    fr_visibility = round(fr_avg_quality, 1) if fr_queries > 0 else 0

    # Count hallucinations (gaps where toxic citation exists)
    cursor = await db.execute(
        f"SELECT lang, COUNT(*) as cnt FROM signal_gaps{where_clause} AND source_of_hallucination_label IS NOT NULL AND source_of_hallucination_label != '' GROUP BY lang"
        if where_clause else
        "SELECT lang, COUNT(*) as cnt FROM signal_gaps WHERE source_of_hallucination_label IS NOT NULL AND source_of_hallucination_label != '' GROUP BY lang",
        params,
    )
    halluc_rows = await cursor.fetchall()
    en_hallucinations = 0
    fr_hallucinations = 0
    for r in halluc_rows:
        if r["lang"] == "EN":
            en_hallucinations = r["cnt"]
        elif r["lang"] == "FR":
            fr_hallucinations = r["cnt"]

    # Token estimates based on query count and language complexity
    en_avg_tokens = round(en_queries * 4.2, 1) if en_queries > 0 else 0
    fr_avg_tokens = round(fr_queries * 6.8, 1) if fr_queries > 0 else 0

    # Also check the static parity_stats table as fallback for token data
    cursor = await db.execute("SELECT * FROM parity_stats LIMIT 1")
    static = await cursor.fetchone()

    return {
        "en": en_visibility,
        "fr": fr_visibility,
        "en_queries": en_queries,
        "fr_queries": fr_queries,
        "en_hallucinations": en_hallucinations,
        "fr_hallucinations": fr_hallucinations,
        "token_breakdown": {
            "en": {
                "avgTokens": static["en_avg_tokens"] if static else en_avg_tokens,
                "maxTokens": static["en_max_tokens"] if static else 0,
            },
            "fr": {
                "avgTokens": static["fr_avg_tokens"] if static else fr_avg_tokens,
                "maxTokens": static["fr_max_tokens"] if static else 0,
            },
        },
    }


@router.post("/probe")
async def start_probe(req: ProbeRequest, background_tasks: BackgroundTasks):
    """
    Start an async probe task. Returns task_id immediately.
    Frontend polls GET /api/tasks/{task_id} for progress (12/50, etc.).
    """
    task_id = str(uuid.uuid4())

    # Create task record
    async with aiosqlite.connect("visimind.db") as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            """INSERT INTO tasks (id, type, status, progress, total)
               VALUES (?, 'probe', 'pending', 0, ?)""",
            (task_id, req.iterations),
        )
        await db.commit()

    # Kick off background probe
    async def _run_probe():
        async with aiosqlite.connect("visimind.db") as db:
            db.row_factory = aiosqlite.Row
            await run_probe_task(
                db, task_id, req.query, req.lang, req.iterations,
                use_golden_set=req.use_golden_set,
                temperature=req.temperature,
            )

    background_tasks.add_task(_run_probe)

    total = req.iterations * (5 if req.use_golden_set else 1)
    return {"task_id": task_id, "status": "pending", "total": total}


@router.post("/fertility")
async def analyze_fertility(data: dict):
    """
    Analyze token fertility for a text.
    Body: { "text_en": "...", "text_fr": "..." } or { "text": "...", "lang": "fr" }
    """
    if "text_en" in data and "text_fr" in data:
        return compare_fertility(data["text_en"], data["text_fr"])
    elif "text" in data:
        lang = data.get("lang", "en")
        return calculate_fertility(data["text"], lang)
    else:
        return {"error": "Provide 'text' or 'text_en'+'text_fr'"}
