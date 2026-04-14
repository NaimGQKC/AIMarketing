"""
VisiMind -- Audits Router
Trigger audits (with daily circuit breaker) and retrieve results.
"""
import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from routers.auth import require_user
from routers.system import get_daily_count, increment_daily_count
from config import DAILY_PROBE_LIMIT
from probes.engine import run_audit
from scoring.ias_calculator import compute_ias, estimate_revenue_impact

router = APIRouter(prefix="/api/v1/audits", tags=["audits"])


@router.post("/{brand_id}/run")
async def trigger_audit(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Trigger a full bilingual audit. Enforces daily circuit breaker."""
    # Check daily limit
    daily_count = await get_daily_count(db)
    if daily_count >= DAILY_PROBE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Daily audit limit reached",
                "resets_at": "midnight UTC",
                "used": daily_count,
                "limit": DAILY_PROBE_LIMIT,
            },
        )

    # Verify brand belongs to user
    cursor = await db.execute(
        "SELECT * FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    brand_dict = dict(brand)

    # Increment counter
    await increment_daily_count(db)

    # Run the audit
    audit_data = await run_audit(db, brand_dict)

    # Compute IAS
    ias = compute_ias(audit_data["results"])
    revenue = estimate_revenue_impact(ias["score"])

    # Update audit record with IAS
    await db.execute(
        "UPDATE audit_results SET ias_score = ?, ias_data = ? WHERE id = ?",
        (ias["score"], json.dumps(ias), audit_data["audit_id"]),
    )
    await db.commit()

    return {
        "audit_id": audit_data["audit_id"],
        "brand_name": audit_data["brand_name"],
        "probes_run": audit_data["probes_run"],
        "providers_used": audit_data["providers_used"],
        "ias": ias,
        "revenue_impact": revenue,
    }


@router.get("/{brand_id}/results")
async def get_audit_results(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Get the latest audit results for a brand."""
    # Verify brand belongs to user
    cursor = await db.execute(
        "SELECT id FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")

    cursor = await db.execute(
        "SELECT * FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
        (brand_id,),
    )
    audit = await cursor.fetchone()
    if not audit:
        raise HTTPException(status_code=404, detail="No audit results found. Run an audit first.")

    audit_dict = dict(audit)
    results = json.loads(audit_dict["results"]) if audit_dict["results"] else []
    ias_data = json.loads(audit_dict["ias_data"]) if audit_dict.get("ias_data") else None

    # Compute revenue impact
    ias_score = audit_dict.get("ias_score", 0) or 0
    revenue = estimate_revenue_impact(ias_score)

    return {
        "audit_id": audit_dict["id"],
        "brand_profile_id": audit_dict["brand_profile_id"],
        "status": audit_dict["status"],
        "ias": ias_data,
        "revenue_impact": revenue,
        "results": results,
        "created_at": audit_dict["created_at"],
    }


@router.get("/{brand_id}/score")
async def get_ias_score(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Get just the IAS score for the latest audit."""
    cursor = await db.execute(
        "SELECT id FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")

    cursor = await db.execute(
        "SELECT ias_score, ias_data FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
        (brand_id,),
    )
    audit = await cursor.fetchone()
    if not audit:
        raise HTTPException(status_code=404, detail="No audit results found")

    ias_data = json.loads(audit["ias_data"]) if audit["ias_data"] else {"score": 0, "grade": "RED"}
    return ias_data


@router.get("/{brand_id}/history")
async def get_audit_history(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Get all audit scores over time for trend display."""
    cursor = await db.execute(
        "SELECT id FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")

    cursor = await db.execute(
        "SELECT id, ias_score, created_at FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at ASC",
        (brand_id,),
    )
    rows = await cursor.fetchall()
    return [{"audit_id": r["id"], "ias_score": r["ias_score"], "created_at": r["created_at"]} for r in rows]
