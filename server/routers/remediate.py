"""
VisiMind — Remediate API Router
GET/POST /api/remediate/kits | deploy | compare
"""
import json
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db
from engines.bilingual_bridge import inject_bilingual_context

router = APIRouter(prefix="/api/remediate", tags=["remediate"])


@router.get("/kits")
async def get_fix_kits(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Available fix kits, optionally filtered by brand."""
    query_str = """SELECT fk.*, b.name as brand_name, p.name_en as product_name
           FROM fix_kits fk
           JOIN brands b ON fk.brand_id = b.id
           JOIN products p ON fk.product_id = p.id"""
    params = ()
    
    if brand_id and brand_id != "all":
        query_str += " WHERE fk.brand_id = ?"
        params = (brand_id,)
        
    query_str += " ORDER BY fk.created_at"
    
    cursor = await db.execute(query_str, params)
    rows = await cursor.fetchall()

    return [
        {
            "id": r["id"],
            "type": r["type"],
            "brand": r["brand_name"],
            "product": r["product_name"],
            "status": r["status"],
            "payload": json.loads(r["payload"]) if r["payload"] else None,
            "impact": r["impact"],
        }
        for r in rows
    ]


@router.get("/kits/{kit_id}/preview")
async def preview_kit(kit_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Preview a fix kit's payload with full JSON-LD."""
    cursor = await db.execute(
        """SELECT fk.*, p.*, b.name as brand_name
           FROM fix_kits fk
           JOIN products p ON fk.product_id = p.id
           JOIN brands b ON fk.brand_id = b.id
           WHERE fk.id = ?""",
        (kit_id,),
    )
    row = await cursor.fetchone()
    if not row:
        return {"error": "Kit not found"}

    product = dict(row)
    product["brand_name"] = row["brand_name"]

    # Generate full JSON-LD preview
    jsonld = inject_bilingual_context(product)

    return {
        "kit_id": kit_id,
        "type": row["type"],
        "brand": row["brand_name"],
        "product": row["name_en"],
        "jsonld": jsonld,
        "payload": json.loads(row["payload"]) if row["payload"] else None,
        "impact": row["impact"],
    }


@router.post("/kits/{kit_id}/deploy")
async def deploy_kit(kit_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Deploy a fix kit — updates status and records deployment."""
    await db.execute(
        "UPDATE fix_kits SET status = 'deployed', deployed_at = ? WHERE id = ?",
        (datetime.utcnow().isoformat(), kit_id),
    )
    await db.commit()

    return {"kit_id": kit_id, "status": "deployed", "deployed_at": datetime.utcnow().isoformat()}


@router.get("/compare")
async def get_comparison(db: aiosqlite.Connection = Depends(get_db)):
    """Before/after feed comparison."""
    # Get a product for comparison
    cursor = await db.execute(
        "SELECT p.*, b.name as brand_name FROM products p JOIN brands b ON p.brand_id = b.id LIMIT 1"
    )
    product = await cursor.fetchone()
    if not product:
        return {"before": {}, "after": {}}

    before = {
        "product_name": product["name_en"],
        "category": "Outerwear",
        "description": "A warm winter jacket for cold climates.",
        "price": f"{product['price_cad']} CAD",
    }

    after_dict = dict(product)
    after_dict["brand_name"] = product["brand_name"]
    jsonld = inject_bilingual_context(after_dict)

    after = {
        "product_name": product["name_en"],
        "category": product["category"],
        "description": product["description_en"],
        "price": f"{product['price_cad']} CAD",
        "thermal_rating": product["thermal_rating"],
        "fill_power": product["fill_power"],
        "material": product["material"],
        "certifications": json.loads(product["certifications"]) if product["certifications"] else [],
    }

    return {"before": before, "after": after}
