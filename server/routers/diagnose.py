"""
VisiMind — Diagnose API Router
GET/POST /api/diagnose/gaps | parity | probe | fertility
Includes polling-based probe task: POST returns task_id, GET /api/tasks/{id} for progress.
"""
import json
import uuid
import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks
import aiosqlite

from database import get_db
from models import ProbeRequest
from engines.inference_lab import run_probe_task
from engines.bilingual_bridge import calculate_fertility, compare_fertility

router = APIRouter(prefix="/api/diagnose", tags=["diagnose"])


@router.get("/gaps")
async def get_signal_gaps(db: aiosqlite.Connection = Depends(get_db)):
    """Signal gap table with toxic citations."""
    cursor = await db.execute(
        "SELECT * FROM signal_gaps ORDER BY CASE severity WHEN 'critical' THEN 0 ELSE 1 END"
    )
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


@router.get("/parity")
async def get_parity(db: aiosqlite.Connection = Depends(get_db)):
    """EN/FR reasoning parity stats."""
    cursor = await db.execute("SELECT * FROM parity_stats LIMIT 1")
    r = await cursor.fetchone()
    if not r:
        return {"en": 85, "fr": 42, "en_queries": 156, "fr_queries": 134,
                "en_hallucinations": 12, "fr_hallucinations": 47,
                "token_breakdown": {"en": {"avgTokens": 6.2, "maxTokens": 11},
                                    "fr": {"avgTokens": 12.8, "maxTokens": 23}}}

    return {
        "en": r["en_visibility"],
        "fr": r["fr_visibility"],
        "en_queries": r["en_queries"],
        "fr_queries": r["fr_queries"],
        "en_hallucinations": r["en_hallucinations"],
        "fr_hallucinations": r["fr_hallucinations"],
        "token_breakdown": {
            "en": {"avgTokens": r["en_avg_tokens"], "maxTokens": r["en_max_tokens"]},
            "fr": {"avgTokens": r["fr_avg_tokens"], "maxTokens": r["fr_max_tokens"]},
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
            await run_probe_task(db, task_id, req.query, req.lang, req.iterations)

    background_tasks.add_task(_run_probe)

    return {"task_id": task_id, "status": "pending", "total": req.iterations}


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
