"""
VisiMind — Verify API Router (v2 — Neuro-Symbolic)
GET/POST /api/verify/schedule | timeline | confidence | reasoning | audit | efficiency | escore | raft | kg
"""
import json
from typing import Optional
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db
from models import ScheduleAuditRequest, RAFTCycleRequest
from engines.verification import (
    schedule_audit, run_audit, compute_e_score, build_raft_cadence,
)

router = APIRouter(prefix="/api/verify", tags=["verify"])


@router.get("/schedule")
async def get_schedule(db: aiosqlite.Connection = Depends(get_db)):
    """Audit schedule."""
    cursor = await db.execute(
        """SELECT DISTINCT day_number, scheduled_date, status, label
           FROM audit_runs
           WHERE status = 'scheduled' OR status = 'pending'
           ORDER BY day_number"""
    )
    rows = await cursor.fetchall()

    if not rows:
        return [
            {"day": 3, "date": "2026-03-28", "status": "scheduled", "label": "Day 3 — Initial Check"},
            {"day": 7, "date": "2026-04-01", "status": "scheduled", "label": "Day 7 — Mid Audit"},
            {"day": 14, "date": "2026-04-08", "status": "scheduled", "label": "Day 14 — Full Verification"},
        ]

    return [
        {
            "day": r["day_number"],
            "date": r["scheduled_date"],
            "status": r["status"],
            "label": r["label"],
        }
        for r in rows
    ]


@router.post("/schedule")
async def create_schedule(req: ScheduleAuditRequest, db: aiosqlite.Connection = Depends(get_db)):
    """Create audit schedule for a specific brand/fix kit."""
    audits = await schedule_audit(db, req.brand_id, req.fix_kit_id, "", req.days)
    return {"scheduled": audits}


@router.get("/timeline")
async def get_timeline(db: aiosqlite.Connection = Depends(get_db)):
    """Audit event timeline."""
    cursor = await db.execute(
        "SELECT * FROM audit_runs ORDER BY scheduled_date, day_number"
    )
    rows = await cursor.fetchall()

    return [
        {
            "id": r["id"],
            "date": r["scheduled_date"],
            "label": r["label"],
            "status": r["status"],
            "detail": r["detail"],
            "score": r["score_overall"],
            "scores": {
                "technical_accuracy": r["score_technical_accuracy"],
                "citation_fidelity": r["score_citation_fidelity"],
                "linguistic_parity": r["score_linguistic_parity"],
            } if r["score_technical_accuracy"] is not None else None,
        }
        for r in rows
    ]


@router.get("/confidence")
async def get_confidence(db: aiosqlite.Connection = Depends(get_db)):
    """Confidence shift chart data per brand."""
    return [
        {"day": "Baseline", "mackage": 23, "ssense": 35, "aldo": 38},
        {"day": "Day 1", "mackage": 25, "ssense": 36, "aldo": 39},
        {"day": "Day 3", "mackage": 48, "ssense": 45, "aldo": 52},
        {"day": "Day 5", "mackage": 62, "ssense": 58, "aldo": 61},
        {"day": "Day 7", "mackage": 81, "ssense": 72, "aldo": 74},
        {"day": "Day 10", "mackage": 85, "ssense": 78, "aldo": 79},
        {"day": "Day 14", "mackage": None, "ssense": None, "aldo": None},
    ]


@router.get("/reasoning")
async def get_reasoning(db: aiosqlite.Connection = Depends(get_db)):
    """Side-by-side before/after reasoning snapshots."""
    cursor = await db.execute(
        "SELECT rs.*, b.name as brand_name FROM reasoning_snapshots rs JOIN brands b ON rs.brand_id = b.id"
    )
    rows = await cursor.fetchall()

    return [
        {
            "id": r["id"],
            "brand": r["brand_name"],
            "query": r["query"],
            "before": {
                "verdict": r["before_verdict"],
                "reasoning": r["before_reasoning"],
                "citations": json.loads(r["before_citations"]),
                "confidence": r["before_confidence"],
            },
            "after": {
                "verdict": r["after_verdict"],
                "reasoning": r["after_reasoning"],
                "citations": json.loads(r["after_citations"]),
                "confidence": r["after_confidence"],
            },
        }
        for r in rows
    ]


@router.post("/audit/{audit_id}/run")
async def trigger_audit(audit_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Trigger an audit run."""
    result = await run_audit(db, audit_id)
    return result


@router.get("/efficiency")
async def get_efficiency(db: aiosqlite.Connection = Depends(get_db)):
    """
    Live Remediation Efficiency with full E-Score breakdown.
    E = (S_out / S_in) * (1 - delta)
    Includes path from 0.6 failure state to 1.4+ optimal.
    """
    from engines.bilingual_bridge import calculate_fertility

    sample_en = "Mackage Lena jacket 800-fill power goose down rated -30C seam-sealed construction"
    sample_fr = "Mackage Lena manteau duvet d'oie facteur gonflement 800 indice thermique -30C coutures scellees"

    en_fertility = calculate_fertility(sample_en, "en")
    fr_fertility = calculate_fertility(sample_fr, "fr")

    # Token Decay Factor
    delta = max(0, min(1,
        (fr_fertility["fertility"] - en_fertility["fertility"]) / fr_fertility["fertility"]
    )) if fr_fertility["fertility"] > 0 else 0
    delta = round(delta, 3)

    # Get S_in and S_out from audit data
    cursor = await db.execute(
        "SELECT score_overall FROM audit_runs WHERE status = 'passed' ORDER BY scheduled_date DESC LIMIT 1"
    )
    passed = await cursor.fetchone()

    cursor2 = await db.execute(
        "SELECT score_overall FROM audit_runs WHERE status = 'failed' ORDER BY scheduled_date ASC LIMIT 1"
    )
    failed = await cursor2.fetchone()

    s_in = round(failed["score_overall"] / 10, 1) if failed and failed["score_overall"] else 3.2
    s_out = round(passed["score_overall"] / 10, 1) if passed and passed["score_overall"] else 8.5

    # Check for KG grounding score
    kg_grounding = None
    cursor3 = await db.execute(
        "SELECT AVG(confidence) as avg_conf FROM kg_triples LIMIT 1"
    )
    kg_row = await cursor3.fetchone()
    if kg_row and kg_row["avg_conf"]:
        kg_grounding = round(kg_row["avg_conf"], 3)

    # Compute full E-Score with path
    e_data = compute_e_score(s_in, s_out, delta, kg_grounding)

    # Add fertility data
    e_data["en_fertility"] = en_fertility["fertility"]
    e_data["fr_fertility"] = fr_fertility["fertility"]
    e_data["kg_grounding"] = kg_grounding

    # Get E-Score history
    cursor4 = await db.execute(
        "SELECT e_score, status, trigger, created_at FROM e_score_history ORDER BY created_at DESC LIMIT 10"
    )
    history_rows = await cursor4.fetchall()
    e_data["history"] = [
        {
            "e_score": r["e_score"],
            "status": r["status"],
            "trigger": r["trigger"],
            "date": r["created_at"],
        }
        for r in history_rows
    ]

    return e_data


@router.get("/raft")
async def get_raft_cadence(
    brand_id: Optional[str] = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    """
    Get RAFT (Retrieval-Augmented Fine-Tuning) cadence plan.
    Computes schedule based on current E-Score.
    """
    from engines.bilingual_bridge import calculate_fertility

    # Get current E-Score
    sample_en = "Mackage Lena jacket 800-fill power goose down rated -30C"
    sample_fr = "Mackage Lena manteau duvet d'oie facteur gonflement 800"
    en_fert = calculate_fertility(sample_en, "en")
    fr_fert = calculate_fertility(sample_fr, "fr")
    delta = max(0, min(1,
        (fr_fert["fertility"] - en_fert["fertility"]) / fr_fert["fertility"]
    )) if fr_fert["fertility"] > 0 else 0

    cursor = await db.execute(
        "SELECT score_overall FROM audit_runs WHERE status = 'passed' ORDER BY scheduled_date DESC LIMIT 1"
    )
    passed = await cursor.fetchone()
    cursor2 = await db.execute(
        "SELECT score_overall FROM audit_runs WHERE status = 'failed' ORDER BY scheduled_date ASC LIMIT 1"
    )
    failed = await cursor2.fetchone()

    s_in = round(failed["score_overall"] / 10, 1) if failed and failed["score_overall"] else 3.2
    s_out = round(passed["score_overall"] / 10, 1) if passed and passed["score_overall"] else 8.5

    e_data = compute_e_score(s_in, s_out, delta)
    current_e = e_data["e_score"]

    bid = brand_id or "mackage"
    cadence = build_raft_cadence(bid, current_e, delta)

    # Get existing RAFT schedule from DB
    cursor3 = await db.execute(
        "SELECT * FROM raft_schedule WHERE brand_id = ? ORDER BY cycle", (bid,)
    )
    existing = await cursor3.fetchall()
    if existing:
        cadence["db_schedule"] = [
            {
                "cycle": r["cycle"],
                "date": r["scheduled_date"],
                "status": r["status"],
                "e_before": r["e_score_before"],
                "e_after": r["e_score_after"],
                "e1_purged": r["e1_errors_purged"],
            }
            for r in existing
        ]

    return cadence


@router.get("/kg")
async def get_kg_stats(
    brand_id: Optional[str] = None,
    db: aiosqlite.Connection = Depends(get_db),
):
    """Knowledge Graph statistics and KGQA scores for a brand."""
    bid = brand_id or "mackage"

    # Entity count
    cursor = await db.execute(
        "SELECT COUNT(*) as cnt FROM kg_entities WHERE brand_id = ?", (bid,)
    )
    entity_count = (await cursor.fetchone())["cnt"]

    # Triple count and avg confidence
    cursor2 = await db.execute(
        "SELECT COUNT(*) as cnt, AVG(confidence) as avg_conf FROM kg_triples WHERE brand_id = ?",
        (bid,),
    )
    row = await cursor2.fetchone()
    triple_count = row["cnt"]
    avg_confidence = round(row["avg_conf"], 3) if row["avg_conf"] else 0

    # Hard constraint count (confidence >= 0.9)
    cursor3 = await db.execute(
        "SELECT COUNT(*) as cnt FROM kg_triples WHERE brand_id = ? AND confidence >= 0.9",
        (bid,),
    )
    hard_count = (await cursor3.fetchone())["cnt"]

    # Compute fuzzy boundary
    cursor4 = await db.execute(
        "SELECT confidence FROM kg_triples WHERE brand_id = ?", (bid,)
    )
    confidences = [r["confidence"] for r in await cursor4.fetchall()]

    boundary_score = 0.0
    if confidences:
        product = 1.0
        for c in confidences:
            product *= (1.0 - c)
        boundary_score = round(1.0 - product, 6)

    return {
        "brand_id": bid,
        "entity_count": entity_count,
        "triple_count": triple_count,
        "avg_confidence": avg_confidence,
        "hard_constraint_count": hard_count,
        "boundary_score": boundary_score,
        "formulas": {
            "kgqa": "S_KGQA_out = {(e, Score(e)) : e in E}",
            "fuzzy_union": "T(v?) = I - prod_{1<=i<=K}(I - T(v_i))",
        },
    }
