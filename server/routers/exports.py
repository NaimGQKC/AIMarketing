"""VisiMind -- Export Router (PDF scary reports)"""
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import aiosqlite
import io

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from routers.auth import require_user
from exports.pdf_report import generate_audit_pdf
from scoring.ias_calculator import estimate_revenue_impact

router = APIRouter(prefix="/api/v1/exports", tags=["exports"])


@router.get("/{brand_id}/pdf")
async def export_audit_pdf(
    brand_id: str,
    user: dict = Depends(require_user),
    db: aiosqlite.Connection = Depends(get_db),
):
    """Export the latest audit as a PDF scary report."""
    # Get brand
    cursor = await db.execute(
        "SELECT * FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Get latest audit
    cursor = await db.execute(
        "SELECT * FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
        (brand_id,),
    )
    audit = await cursor.fetchone()
    if not audit:
        raise HTTPException(status_code=404, detail="No audit results found")

    audit_dict = dict(audit)
    ias_data = (
        json.loads(audit_dict["ias_data"])
        if audit_dict.get("ias_data")
        else {"score": 0, "grade": "RED", "findings": [], "breakdown": {}}
    )
    probe_results = (
        json.loads(audit_dict["results"])
        if audit_dict.get("results")
        else []
    )
    revenue = estimate_revenue_impact(ias_data.get("score", 0))

    pdf_bytes = generate_audit_pdf(dict(brand), ias_data, revenue, probe_results)

    filename = f"VisiMind-Audit-{brand['brand_name'].replace(' ', '-')}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
