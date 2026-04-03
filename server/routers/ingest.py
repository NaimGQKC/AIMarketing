"""
VisiMind — Ingestion API Router
POST /api/ingest/batch — Upload pre-collected probe data file
GET  /api/ingest/brands — List all brands with ingested data
Uses the same polling pattern as live probes (task_id → poll /api/tasks/{id}).
"""
import uuid
import asyncio
from datetime import datetime
from typing import List
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form
import aiosqlite

from database import get_db, DATABASE
from engines.ingest_parser import parse_probe_file
from engines.batch_analyzer import analyze_and_store_batch

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/batch")
async def ingest_batch(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    brand_name: str = Form(...),
):
    """
    Upload multiple probe data files for a specific brand.
    The files are combined, parsed, and processed in the background.
    Returns a task_id for progress polling via GET /api/tasks/{task_id}.
    """
    combined_content = ""
    for file in files:
        content = await file.read()
        combined_content += content.decode("utf-8", errors="replace") + "\n\n"

    # Parse the combined file content into probe blocks
    probes = parse_probe_file(combined_content)

    if not probes:
        return {
            "error": "No probe blocks found in files. Expected format: 'Query: ...' followed by response and '--- SOURCE LINKS ---'.",
            "hint": "Ensure your files start with 'Query: <your query text>'",
        }

    # Create task record
    task_id = str(uuid.uuid4())
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            """INSERT INTO tasks (id, type, status, progress, total)
               VALUES (?, 'ingest', 'pending', 0, ?)""",
            (task_id, len(probes)),
        )
        await db.commit()

    # Kick off background processing
    async def _run_analysis():
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            await analyze_and_store_batch(db, task_id, brand_name, probes)

    background_tasks.add_task(_run_analysis)

    return {
        "task_id": task_id,
        "status": "pending",
        "brand": brand_name,
        "total_probes": len(probes),
        "queries_found": list(set(p["query"] for p in probes)),
        "languages_detected": list(set(p["lang"] for p in probes)),
    }


@router.post("/json")
async def ingest_json(
    data: dict,
    background_tasks: BackgroundTasks,
):
    """
    Upload pre-structured JSON probe data directly.

    Body:
    {
        "brand_name": "SSENSE",
        "probes": [
            {
                "query": "...",
                "lang": "EN",
                "response_text": "...",
                "source_links": ["...", "..."]
            },
            ...
        ]
    }
    """
    brand_name = data.get("brand_name")
    probes = data.get("probes", [])

    if not brand_name:
        return {"error": "Missing 'brand_name' field."}
    if not probes:
        return {"error": "Missing or empty 'probes' array."}

    # Ensure each probe has the required fields
    for i, probe in enumerate(probes):
        if "query" not in probe or "response_text" not in probe:
            return {"error": f"Probe at index {i} missing 'query' or 'response_text'."}
        # Add defaults
        probe.setdefault("lang", "EN")
        probe.setdefault("source_links", [])
        probe.setdefault("brands_detected", [])

    # Create task
    task_id = str(uuid.uuid4())
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            """INSERT INTO tasks (id, type, status, progress, total)
               VALUES (?, 'ingest', 'pending', 0, ?)""",
            (task_id, len(probes)),
        )
        await db.commit()

    # Background processing
    async def _run_analysis():
        async with aiosqlite.connect(DATABASE) as db:
            db.row_factory = aiosqlite.Row
            await analyze_and_store_batch(db, task_id, brand_name, probes)

    background_tasks.add_task(_run_analysis)

    return {
        "task_id": task_id,
        "status": "pending",
        "brand": brand_name,
        "total_probes": len(probes),
    }


@router.get("/brands")
async def list_ingested_brands():
    """List all brands that have ingested probe data."""
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            """SELECT b.id, b.name, b.slug, b.description,
                      COUNT(DISTINCT pr.query) as queries_analyzed,
                      COUNT(pr.id) as total_probes,
                      COUNT(DISTINCT sg.id) as gaps_found
               FROM brands b
               LEFT JOIN probe_results pr ON pr.query LIKE '%' || b.slug || '%'
                   OR pr.task_id IN (SELECT t.id FROM tasks t WHERE t.type = 'ingest')
               LEFT JOIN signal_gaps sg ON sg.brand_id = b.id
               GROUP BY b.id
               ORDER BY b.name"""
        )
        rows = await cursor.fetchall()

        return [
            {
                "id": r["id"],
                "name": r["name"],
                "slug": r["slug"],
                "description": r["description"],
                "queries_analyzed": r["queries_analyzed"],
                "total_probes": r["total_probes"],
                "gaps_found": r["gaps_found"],
            }
            for r in rows
        ]
