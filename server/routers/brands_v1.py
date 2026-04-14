"""VisiMind -- Brand Profile Router"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from routers.auth import require_user

router = APIRouter(prefix="/api/v1/brands", tags=["brands"])

class CreateBrandRequest(BaseModel):
    brand_name: str = Field(min_length=1)
    primary_url: str = ""
    product_category: str = ""
    top_competitor: str = ""
    language_pair: str = "EN/FR"

@router.post("")
async def create_brand(req: CreateBrandRequest, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    brand_id = str(uuid.uuid4())
    await db.execute(
        "INSERT INTO brand_profiles (id, user_id, brand_name, primary_url, product_category, top_competitor, language_pair) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (brand_id, user["id"], req.brand_name, req.primary_url, req.product_category, req.top_competitor, req.language_pair),
    )
    await db.commit()
    return {"id": brand_id, "brand_name": req.brand_name, "primary_url": req.primary_url, "product_category": req.product_category, "top_competitor": req.top_competitor, "language_pair": req.language_pair}

@router.get("/{brand_id}")
async def get_brand(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM brand_profiles WHERE id = ? AND user_id = ?", (brand_id, user["id"]))
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return dict(brand)

@router.get("")
async def list_brands(user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM brand_profiles WHERE user_id = ? ORDER BY created_at DESC", (user["id"],))
    brands = await cursor.fetchall()
    return [dict(b) for b in brands]
