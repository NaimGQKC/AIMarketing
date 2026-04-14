"""
VisiMind — Remediate API Router (v2 — Neuro-Symbolic)
GET/POST /api/remediate/kits | deploy | compare | dpo | graph
"""
import json
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db
from engines.bilingual_bridge import inject_bilingual_context
from engines.remediation import (
    build_deterministic_graph, build_dpo_constraint_set,
    generate_truth_clip_metadata, generate_youtube_deployment,
)

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
    """Preview a fix kit's payload with full deterministic @graph JSON-LD."""
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

    # Get KG boundary if available
    kg_boundary = None
    cursor2 = await db.execute(
        "SELECT COUNT(*) as cnt, AVG(confidence) as avg_conf FROM kg_triples WHERE brand_id = ?",
        (row["brand_id"],),
    )
    kg_row = await cursor2.fetchone()
    if kg_row and kg_row["cnt"] > 0:
        kg_boundary = {
            "boundary_score": round(kg_row["avg_conf"], 3),
            "hard_count": kg_row["cnt"],
            "total_triples": kg_row["cnt"],
        }

    # Generate full deterministic @graph preview
    graph = build_deterministic_graph(product, kg_boundary=kg_boundary)

    # Also generate DPO constraints if hardAttributes type
    dpo = None
    if row["type"] == "hardAttributes":
        dpo = build_dpo_constraint_set(product, kg_boundary)

    # Also generate truth clip metadata if truthClip type
    clip_meta = None
    if row["type"] == "truthClip":
        clip_meta = generate_truth_clip_metadata(product)

    return {
        "kit_id": kit_id,
        "type": row["type"],
        "brand": row["brand_name"],
        "product": row["name_en"],
        "graph": graph,
        "dpo_constraints": dpo,
        "truth_clip": clip_meta,
        "payload": json.loads(row["payload"]) if row["payload"] else None,
        "impact": row["impact"],
    }


@router.post("/kits/{kit_id}/deploy")
async def deploy_kit(kit_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Deploy a fix kit — updates status, records deployment, logs E-Score event."""
    now = datetime.utcnow().isoformat()

    await db.execute(
        "UPDATE fix_kits SET status = 'deployed', deployed_at = ? WHERE id = ?",
        (now, kit_id),
    )

    # Log E-Score event for deployment tracking
    cursor = await db.execute("SELECT brand_id FROM fix_kits WHERE id = ?", (kit_id,))
    kit = await cursor.fetchone()
    if kit:
        await db.execute(
            """INSERT INTO e_score_history (brand_id, e_score, status, trigger, detail, created_at)
               VALUES (?, ?, 'marginal', 'kit_deployment', ?, ?)""",
            (kit["brand_id"], 1.0, f"Fix kit {kit_id} deployed", now),
        )

    await db.commit()

    return {"kit_id": kit_id, "status": "deployed", "deployed_at": now}


@router.get("/compare")
async def get_comparison(db: aiosqlite.Connection = Depends(get_db)):
    """Before/after feed comparison with @graph enhancement."""
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
        "schema_type": "Unstructured HTML",
        "entity_disambiguation": "None",
        "constraint_decoding": "None",
    }

    product_dict = dict(product)
    product_dict["brand_name"] = product["brand_name"]
    graph = build_deterministic_graph(product_dict)

    after = {
        "product_name": product["name_en"],
        "category": product["category"],
        "description": product["description_en"],
        "price": f"{product['price_cad']} CAD",
        "thermal_rating": product["thermal_rating"],
        "fill_power": product["fill_power"],
        "material": product["material"],
        "certifications": json.loads(product["certifications"]) if product["certifications"] else [],
        "schema_type": "Deterministic @graph JSON-LD",
        "entity_disambiguation": f"urn:visimind:product:{product['id']}",
        "constraint_decoding": "DPO — P(contradiction) = 0",
        "graph_nodes": len(graph.get("@graph", [])),
    }

    return {"before": before, "after": after}


@router.get("/dpo/{product_id}")
async def get_dpo_constraints(product_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Get DPO constraint set for a specific product."""
    cursor = await db.execute(
        "SELECT p.*, b.name as brand_name FROM products p JOIN brands b ON p.brand_id = b.id WHERE p.id = ?",
        (product_id,),
    )
    row = await cursor.fetchone()
    if not row:
        return {"error": "Product not found"}

    product = dict(row)
    product["brand_name"] = row["brand_name"]

    # Get KG boundary
    kg_boundary = None
    cursor2 = await db.execute(
        "SELECT COUNT(*) as cnt, AVG(confidence) as avg_conf FROM kg_triples WHERE brand_id = ?",
        (row["brand_id"],),
    )
    kg_row = await cursor2.fetchone()
    if kg_row and kg_row["cnt"] > 0:
        kg_boundary = {
            "boundary_score": round(kg_row["avg_conf"], 3),
            "hard_count": kg_row["cnt"],
            "total_triples": kg_row["cnt"],
        }

    return build_dpo_constraint_set(product, kg_boundary)


@router.get("/graph/{brand_id}")
async def get_brand_graph(brand_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Get the deterministic @graph JSON-LD for an entire brand."""
    cursor = await db.execute(
        "SELECT p.*, b.name as brand_name FROM products p JOIN brands b ON p.brand_id = b.id WHERE b.id = ?",
        (brand_id,),
    )
    products = await cursor.fetchall()

    if not products:
        return {"error": "No products found for brand"}

    graphs = []
    for p in products:
        product = dict(p)
        product["brand_name"] = p["brand_name"]
        graphs.append(build_deterministic_graph(product))

    return {
        "brand_id": brand_id,
        "product_count": len(graphs),
        "graphs": graphs,
    }


@router.get("/youtube-recommendations/{brand_id}")
async def get_youtube_recommendations(brand_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """
    YouTube video deployment recommendations for all products of a brand.

    Each recommendation includes bilingual titles, descriptions, tags, a
    thumbnail prompt, a script outline, and SEO data. YouTube mentions
    correlate at 0.737 with AI brand visibility (Ahrefs, 75K brand study).
    """
    cursor = await db.execute(
        "SELECT p.*, b.name as brand_name FROM products p JOIN brands b ON p.brand_id = b.id WHERE b.id = ?",
        (brand_id,),
    )
    products = await cursor.fetchall()

    if not products:
        return {"error": "No products found for brand", "brand_id": brand_id}

    recommendations = []
    for p in products:
        product = dict(p)
        product["brand_name"] = p["brand_name"]
        yt = generate_youtube_deployment(product)
        recommendations.append({
            "product_id": product["id"],
            "product_name_en": product["name_en"],
            "product_name_fr": product.get("name_fr", ""),
            "youtube_deployment": yt,
        })

    return {
        "brand_id": brand_id,
        "brand_name": products[0]["brand_name"],
        "total_recommendations": len(recommendations),
        "rationale": (
            "YouTube mentions correlate at 0.737 with AI brand visibility "
            "(Ahrefs, 75K brand study). French YouTube content for this brand "
            "is near-zero, creating a bilingual visibility gap."
        ),
        "recommendations": recommendations,
    }
