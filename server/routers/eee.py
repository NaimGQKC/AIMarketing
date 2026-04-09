"""
VisiMind — EEE (External Environment Engineering) API Router
GET /api/eee/syndication | freshness | authority | priority | roadmap
         | replies | pings | drift | tax | moat
"""
import json
from typing import Optional
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db
from engines.eee_engine import (
    build_syndication_network,
    build_freshness_cycle,
    compute_citation_authority,
    build_agentic_priority_map,
    build_e_score_roadmap,
    generate_verification_replies,
    build_external_ping_manifest,
    check_drift_warning,
    calculate_interpretation_tax,
    compute_montreal_moat,
    probe_toxic_source,
    compute_tax_driven_priority,
    score_reply_effectiveness,
)
from engines.verification import compute_e_score
from engines.bilingual_bridge import calculate_fertility

router = APIRouter(prefix="/api/eee", tags=["eee"])


# --- Shared helpers ---

async def _get_brand_and_products(db, brand_id: str):
    bid = brand_id or "mackage"
    cursor = await db.execute("SELECT * FROM brands WHERE id = ?", (bid,))
    brand_row = await cursor.fetchone()
    brand = dict(brand_row) if brand_row else {"id": bid, "name": bid.title(), "slug": bid}
    cursor2 = await db.execute("SELECT * FROM products WHERE brand_id = ?", (bid,))
    products = [dict(r) for r in await cursor2.fetchall()]
    return bid, brand, products


async def _get_current_e_and_delta(db):
    """Compute current E-Score and delta from real audit data. Returns zeros if no data."""
    # Get delta from product data in DB rather than hardcoded sample strings
    cursor = await db.execute(
        "SELECT description_en, description_fr FROM products WHERE description_en IS NOT NULL LIMIT 1"
    )
    product = await cursor.fetchone()

    if product and product["description_en"] and product["description_fr"]:
        en_fert = calculate_fertility(product["description_en"], "en")
        fr_fert = calculate_fertility(product["description_fr"], "fr")
    else:
        en_fert = {"fertility": 1.0, "tokens": 0, "words": 0}
        fr_fert = {"fertility": 1.0, "tokens": 0, "words": 0}

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

    s_in = round(failed["score_overall"] / 10, 1) if failed and failed["score_overall"] else 0.0
    s_out = round(passed["score_overall"] / 10, 1) if passed and passed["score_overall"] else 0.0

    if s_in == 0 and s_out == 0:
        return 0.0, delta, en_fert, fr_fert

    e_data = compute_e_score(s_in, s_out, delta)
    return e_data["e_score"], delta, en_fert, fr_fert


# --- Existing endpoints ---

@router.get("/syndication")
async def get_syndication(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Semantic Saturation network."""
    bid, brand, products = await _get_brand_and_products(db, brand_id)
    return build_syndication_network(brand, products)


@router.get("/freshness")
async def get_freshness(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Freshness Bias cycle."""
    bid, brand, products = await _get_brand_and_products(db, brand_id)
    current_e, delta, _, _ = await _get_current_e_and_delta(db)
    return build_freshness_cycle(bid, products, current_e, delta)


@router.get("/authority")
async def get_authority(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Citation Authority map."""
    bid = brand_id or "mackage"
    cursor = await db.execute("SELECT * FROM signal_gaps WHERE brand_id = ?", (bid,))
    gaps = [dict(r) for r in await cursor.fetchall()]
    return compute_citation_authority(bid, gaps)


@router.get("/priority")
async def get_priority(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Agentic Commerce priority map."""
    bid, brand, products = await _get_brand_and_products(db, brand_id)
    kg_boundary = None
    cursor = await db.execute(
        "SELECT COUNT(*) as cnt, AVG(confidence) as avg_conf FROM kg_triples WHERE brand_id = ?", (bid,),
    )
    kg_row = await cursor.fetchone()
    if kg_row and kg_row["cnt"] > 0:
        kg_boundary = {"boundary_score": round(kg_row["avg_conf"], 3), "hard_count": kg_row["cnt"], "total_triples": kg_row["cnt"]}
    return build_agentic_priority_map(brand, products, kg_boundary)


@router.get("/roadmap")
async def get_roadmap(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """Complete E-Score roadmap from 0.6 -> 1.4+."""
    bid, brand, products = await _get_brand_and_products(db, brand_id)
    current_e, delta, _, _ = await _get_current_e_and_delta(db)
    syndication = build_syndication_network(brand, products)
    saturation = syndication["saturation_score"]["overall"]
    cursor = await db.execute("SELECT * FROM signal_gaps WHERE brand_id = ?", (bid,))
    gaps = [dict(r) for r in await cursor.fetchall()]
    authority = compute_citation_authority(bid, gaps)
    return build_e_score_roadmap(bid, current_e, delta, saturation, authority["authority_ratio"])


# --- New endpoints ---

@router.get("/replies")
async def get_verification_replies(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """
    Counter-Sentiment Logic: Verification Replies for Tier 5 toxic citations.
    Links toxic Reddit/YouTube threads back to Tier 2 URIs to close the RAG loop.
    """
    bid, brand, products = await _get_brand_and_products(db, brand_id)
    cursor = await db.execute("SELECT * FROM signal_gaps WHERE brand_id = ?", (bid,))
    gaps = [dict(r) for r in await cursor.fetchall()]
    return generate_verification_replies(brand, products, gaps)


@router.get("/pings")
async def get_external_pings(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """
    External Ping manifest: sitemap, HTTP headers, and ping targets
    for forcing crawler cache flush.
    """
    bid, brand, products = await _get_brand_and_products(db, brand_id)
    current_e, delta, _, _ = await _get_current_e_and_delta(db)

    # Determine cycle hours from E-Score
    if current_e < 0.8:
        cycle_hours = 2
    elif current_e < 1.0:
        cycle_hours = 6
    elif current_e < 1.2:
        cycle_hours = 12
    elif current_e < 1.4:
        cycle_hours = 24
    else:
        cycle_hours = 48

    return build_external_ping_manifest(brand, products, cycle_hours)


@router.get("/drift")
async def get_drift_warning(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """
    Drift Warning: detect E-Score drops > 0.2, trigger Defensive Freshness,
    and run binary-search probe to identify the toxic source.
    """
    bid = brand_id or "mackage"
    current_e, delta, _, _ = await _get_current_e_and_delta(db)

    # Get E-Score history
    cursor = await db.execute(
        "SELECT e_score, status, trigger, created_at FROM e_score_history ORDER BY created_at DESC LIMIT 20"
    )
    history = [dict(r) for r in await cursor.fetchall()]

    drift = check_drift_warning(history, current_e)

    # If drift detected, run binary-search probe to find the toxic source
    if drift["drift_detected"]:
        cursor2 = await db.execute(
            "SELECT * FROM signal_gaps WHERE brand_id = ? ORDER BY created_at DESC", (bid,)
        )
        gaps = [dict(r) for r in await cursor2.fetchall()]
        probe = probe_toxic_source(gaps, drift["peak_e"], current_e)
        drift["toxic_probe"] = probe
    else:
        drift["toxic_probe"] = None

    return drift


@router.get("/tax")
async def get_interpretation_tax(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """
    Interpretation Tax Calculator: quantify token savings of @graph vs HTML.
    Includes tax-driven priority scores per product.
    """
    bid, brand, products = await _get_brand_and_products(db, brand_id)

    # Get KG boundary for priority scoring
    kg_boundary = None
    cursor = await db.execute(
        "SELECT COUNT(*) as cnt, AVG(confidence) as avg_conf FROM kg_triples WHERE brand_id = ?", (bid,),
    )
    kg_row = await cursor.fetchone()
    if kg_row and kg_row["cnt"] > 0:
        kg_boundary = {"boundary_score": round(kg_row["avg_conf"], 3), "hard_count": kg_row["cnt"], "total_triples": kg_row["cnt"]}

    if products:
        product = products[0]
        product["brand_name"] = brand.get("name", "")
        tax = calculate_interpretation_tax(product)

        # Tax-driven priority scores for each product
        priority_scores = []
        for p in products:
            p["brand_name"] = brand.get("name", "")
            tdp = compute_tax_driven_priority(p, kg_boundary)
            priority_scores.append(tdp)

        tax["total_products"] = len(products)
        tax["aggregate_savings"] = {
            "tokens_saved_per_query": tax["interpretation_tax"]["tokens_saved"],
            "at_1000_queries_per_day": tax["interpretation_tax"]["tokens_saved"] * 1000,
            "monthly_token_savings": tax["interpretation_tax"]["tokens_saved"] * 1000 * 30,
        }
        tax["tax_driven_priorities"] = priority_scores
        tax["avg_priority_score"] = round(
            sum(p["priority_score"] for p in priority_scores) / max(len(priority_scores), 1), 3
        )
        return tax
    else:
        return calculate_interpretation_tax({"id": "sample", "name_en": "Sample Product"})


@router.get("/moat")
async def get_montreal_moat(brand_id: Optional[str] = None, db: aiosqlite.Connection = Depends(get_db)):
    """
    Montreal Moat: EN vs FR E-Score split showing bilingual competitive advantage.
    """
    current_e, delta, en_fert, fr_fert = await _get_current_e_and_delta(db)

    # Compute separate EN/FR E-Scores
    # FR E-Score is penalized by full delta; EN is unpenalized
    en_e = round(current_e / max(1 - delta, 0.01), 2)  # Remove delta penalty to get EN-only
    fr_e = round(current_e * (1 - delta * 0.5), 2)     # Apply extra FR penalty

    return compute_montreal_moat(
        en_e_score=en_e,
        fr_e_score=fr_e,
        delta=delta,
        en_fertility=en_fert["fertility"],
        fr_fertility=fr_fert["fertility"],
    )
