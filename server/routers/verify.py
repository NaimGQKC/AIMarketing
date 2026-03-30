"""
VisiMind — Verify API Router
GET/POST /api/verify/schedule | timeline | confidence | reasoning | audit
"""
import json
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db
from models import ScheduleAuditRequest
from engines.verification import schedule_audit, run_audit

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
    Live Remediation Efficiency: E = (S_out / S_in) · (1 − δ)
    Where δ = Token Decay Factor derived from bilingual bridge fertility analysis.
    """
    from engines.bilingual_bridge import calculate_fertility

    # Representative bilingual content for live δ calculation
    sample_en = "Mackage Lena jacket 800-fill power goose down rated -30°C seam-sealed construction"
    sample_fr = "Mackage Lena manteau duvet d'oie facteur gonflement 800 indice thermique -30°C coutures scellées"

    en_fertility = calculate_fertility(sample_en, "en")
    fr_fertility = calculate_fertility(sample_fr, "fr")

    # Token Decay Factor: normalized difference in fertility
    # δ = (fr_fertility - en_fertility) / fr_fertility, clamped [0, 1]
    delta = max(0, min(1,
        (fr_fertility["fertility"] - en_fertility["fertility"]) / fr_fertility["fertility"]
    )) if fr_fertility["fertility"] > 0 else 0
    delta = round(delta, 3)

    # Semantic clarity scores from aggregate metrics
    # S_in = baseline PIM quality, S_out = post-remediation quality
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

    # Compute E
    e_score = round((s_out / s_in) * (1 - delta), 2) if s_in > 0 else 0

    return {
        "e_score": e_score,
        "s_in": s_in,
        "s_out": s_out,
        "delta": delta,
        "en_fertility": en_fertility["fertility"],
        "fr_fertility": fr_fertility["fertility"],
        "formula": f"E = ({s_out} / {s_in}) × (1 − {delta}) = {e_score}",
    }
