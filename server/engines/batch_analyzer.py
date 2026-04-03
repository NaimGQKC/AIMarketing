"""
VisiMind — Batch Analyzer
Takes parsed probe records and runs them through the analytical engines
(brand detection, citation classification, gap classification, bilingual bridge).
Populates the same DB tables the frontend reads from.
No LLM calls — everything runs locally.
"""
import json
import uuid
import re
from datetime import datetime
from typing import Optional

from engines.ingest_parser import classify_sources, detect_brands
from engines.inference_lab import classify_gap
from engines.bilingual_bridge import calculate_fertility


# --- Main Orchestrator ---

async def analyze_and_store_batch(
    db,
    task_id: str,
    brand_name: str,
    probes: list[dict],
):
    """
    Main entry point: analyze a batch of parsed probe records and store results.

    1. Ensures brand exists in DB (creates if new)
    2. Stores individual probe results
    3. Aggregates into signal gaps
    4. Updates parity stats

    Args:
        db: aiosqlite connection
        task_id: task ID for progress tracking
        brand_name: target brand name (one file = one brand)
        probes: list of parsed probe records from ingest_parser
    """
    try:
        # Mark task as running
        await db.execute(
            "UPDATE tasks SET status = 'running', total = ? WHERE id = ?",
            (len(probes), task_id),
        )
        await db.commit()

        # 1. Ensure brand exists
        brand_id, brand_slug = await _ensure_brand(db, brand_name)

        # 2. Process each probe block
        all_results = []
        en_probes = []
        fr_probes = []

        for i, probe in enumerate(probes):
            result = await _process_single_probe(db, task_id, brand_id, brand_slug, probe, i + 1)
            all_results.append(result)

            if probe["lang"] == "FR":
                fr_probes.append(result)
            else:
                en_probes.append(result)

            # Update progress
            await db.execute(
                "UPDATE tasks SET progress = ?, updated_at = ? WHERE id = ?",
                (i + 1, datetime.utcnow().isoformat(), task_id),
            )
            await db.commit()

        # 3. Aggregate into signal gaps
        gaps_created = await _create_signal_gaps(db, brand_id, brand_slug, all_results, probes)

        # 4. Update parity stats
        await _update_parity_stats(db, en_probes, fr_probes)

        # 4.5. Generate mock Fix Kits for the new brand
        await _generate_fix_kits(db, brand_id, brand_slug)

        # 5. Build summary
        summary = _build_summary(brand_name, probes, all_results, en_probes, fr_probes, gaps_created)

        await db.execute(
            "UPDATE tasks SET status = 'completed', result = ?, updated_at = ? WHERE id = ?",
            (json.dumps(summary), datetime.utcnow().isoformat(), task_id),
        )
        await db.commit()

    except Exception as e:
        await db.execute(
            "UPDATE tasks SET status = 'failed', error = ?, updated_at = ? WHERE id = ?",
            (str(e), datetime.utcnow().isoformat(), task_id),
        )
        await db.commit()
        raise


# --- Brand Management ---

async def _ensure_brand(db, brand_name: str) -> tuple[str, str]:
    """Ensure brand exists in DB, create if new. Returns (brand_id, brand_slug)."""
    slug = brand_name.lower().replace(" ", "-").replace("'", "")
    brand_id = slug

    cursor = await db.execute("SELECT id FROM brands WHERE slug = ?", (slug,))
    existing = await cursor.fetchone()

    if not existing:
        await db.execute(
            "INSERT INTO brands (id, name, slug, description) VALUES (?, ?, ?, ?)",
            (brand_id, brand_name, slug, f"Auto-created from batch ingestion on {datetime.utcnow().strftime('%Y-%m-%d')}"),
        )
        await db.commit()

    return brand_id, slug


# --- Individual Probe Processing ---

async def _process_single_probe(
    db, task_id: str, brand_id: str, brand_slug: str, probe: dict, iteration: int
) -> dict:
    """
    Process a single probe record:
    - Check if target brand appears in the AI response
    - Extract recommendation position
    - Classify source links
    - Compute token fertility
    - Store in probe_results table
    """
    response_text = probe["response_text"]
    query = probe["query"]
    lang = probe["lang"]
    source_links = probe.get("source_links", [])

    # Brand detection — check if OUR target brand is mentioned
    brand_mentioned = brand_slug in response_text.lower() or \
                      brand_id in response_text.lower()

    # Also check with the original brand name variants
    brands_detected = probe.get("brands_detected", [])
    target_brand_data = None
    for bd in brands_detected:
        if bd["slug"] == brand_slug or bd["name"].lower() == brand_id.lower():
            target_brand_data = bd
            brand_mentioned = True
            break

    recommendation_position = target_brand_data["position"] if target_brand_data else None

    # Classify sources
    classified_sources = classify_sources(source_links)
    toxic_sources = [s for s in classified_sources if s["is_toxic"]]

    # Token fertility
    fertility_data = None
    if response_text:
        try:
            fertility_data = calculate_fertility(response_text, lang.lower())
        except Exception:
            pass

    # Store in probe_results
    result_id = str(uuid.uuid4())
    await db.execute(
        """INSERT INTO probe_results
           (id, task_id, query, lang, iteration, model, response_text,
            citations, brand_mentioned, brand_mention_logprob,
            recommendation_position, response_time_ms)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            result_id, task_id, query, lang, iteration, "ingested",
            response_text,
            json.dumps(source_links),
            1 if brand_mentioned else 0,
            None,  # No logprob for ingested data
            recommendation_position,
            0,  # No response time for ingested data
        ),
    )
    await db.commit()

    return {
        "id": result_id,
        "query": query,
        "lang": lang,
        "response_text": response_text,
        "brand_mentioned": brand_mentioned,
        "recommendation_position": recommendation_position,
        "source_links": source_links,
        "classified_sources": classified_sources,
        "toxic_sources": toxic_sources,
        "fertility": fertility_data,
        "brands_detected": brands_detected,
    }


# --- Signal Gap Aggregation ---

async def _create_signal_gaps(
    db, brand_id: str, brand_slug: str, results: list[dict], probes: list[dict]
) -> int:
    """
    Aggregate probe results into signal_gaps entries.
    Groups by (query, lang) and creates one gap per group where the brand is missing or poorly represented.
    """
    # Group results by (query, lang)
    groups: dict[tuple, list[dict]] = {}
    for result in results:
        key = (result["query"], result["lang"])
        if key not in groups:
            groups[key] = []
        groups[key].append(result)

    gaps_created = 0

    for (query, lang), group_results in groups.items():
        # Calculate mention rate for this query+lang combo
        total = len(group_results)
        mentioned = sum(1 for r in group_results if r["brand_mentioned"])
        mention_rate = (mentioned / total * 100) if total > 0 else 0

        # Collect all toxic sources
        all_toxic = []
        all_sources = []
        for r in group_results:
            all_toxic.extend(r["toxic_sources"])
            all_sources.extend(r["classified_sources"])

        # Build top citations list for classify_gap
        citation_freq: dict[str, int] = {}
        for r in group_results:
            for src in r["source_links"]:
                citation_freq[src] = citation_freq.get(src, 0) + 1
        top_citations = sorted(citation_freq.items(), key=lambda x: x[1], reverse=True)[:5]

        # Classify the gap type using the existing logic
        gap_type = classify_gap(mention_rate, None, top_citations)

        # Determine severity
        severity = _determine_severity(mention_rate, len(all_toxic), lang)

        # Calculate AI response quality (0-100)
        ai_quality = _calculate_quality_score(mention_rate, len(all_toxic), len(all_sources))

        # Get the best representative response and top toxic source
        best_response = group_results[0]["response_text"][:500] if group_results else ""
        top_toxic = all_toxic[0] if all_toxic else None
        top_clean = next((s for s in all_sources if not s["is_toxic"]), None)

        # Create the signal gap
        gap_id = str(uuid.uuid4())
        await db.execute(
            """INSERT INTO signal_gaps
               (id, brand_id, query, lang, gap_type, severity, ai_response_quality,
                source_of_truth_label, source_of_truth_url, source_of_truth_detail,
                source_of_hallucination_label, source_of_hallucination_url,
                source_of_hallucination_detail, ai_said, brand_truth)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                gap_id, brand_id, query, lang, gap_type, severity, int(ai_quality),
                # Source of truth — blank for MVP, can be enriched later
                f"{brand_id.title()} Brand Data",
                None,
                f"Brand ground truth data pending — to be enriched from product catalog.",
                # Source of hallucination — top toxic source  
                top_toxic["label"] if top_toxic else "No toxic sources detected",
                _extract_url_from_label(top_toxic["label"]) if top_toxic else None,
                f"Toxic/stale source detected in AI response citations." if top_toxic else "AI response uses neutral sources.",
                # AI said — excerpt from the response
                best_response[:300] if best_response else "",
                # Brand truth — blank for MVP
                "",
            ),
        )
        gaps_created += 1

    await db.commit()
    return gaps_created


def _determine_severity(mention_rate: float, toxic_count: int, lang: str) -> str:
    """Determine gap severity based on metrics."""
    if mention_rate < 30 or (toxic_count > 3 and lang == "FR"):
        return "critical"
    elif mention_rate < 60 or toxic_count > 1:
        return "warning"
    else:
        return "info"


def _calculate_quality_score(mention_rate: float, toxic_count: int, total_sources: int) -> float:
    """Calculate AI response quality as a 0-100 score."""
    # Start with mention rate component (0-50)
    base = min(mention_rate * 0.5, 50)

    # Source quality component (0-50)
    if total_sources > 0:
        toxic_ratio = toxic_count / max(total_sources, 1)
        source_score = (1 - toxic_ratio) * 50
    else:
        source_score = 25  # Neutral if no sources

    return round(base + source_score, 1)


def _extract_url_from_label(label: str) -> Optional[str]:
    """Try to extract a URL from a source label."""
    url_match = re.search(r'https?://\S+', label)
    if url_match:
        return url_match.group(0)

    # Try to construct a plausible URL from the label
    parts = label.lower().split()
    for part in parts:
        if "." in part and not part.startswith("(") and len(part) > 4:
            return f"https://{part}"

    return None


# --- Fix Kit Generation ---

async def _generate_fix_kits(db, brand_id: str, brand_slug: str):
    """Generate 3 automated fix kits for a newly ingested brand."""
    cursor = await db.execute("SELECT id FROM fix_kits WHERE brand_id = ?", (brand_id,))
    if await cursor.fetchone():
        return  # Already has kits

    now = datetime.utcnow().isoformat()
    kits = [
        (
            f"kit-{brand_id}-1", brand_id, f"{brand_slug}-prod-001", "hardAttributes", "ready",
            json.dumps({"description": f"Verified product attributes for {brand_slug.title()}", "verified": True}),
            "Expected +20% inference alignment", None, now
        ),
        (
            f"kit-{brand_id}-2", brand_id, f"{brand_slug}-prod-002", "jsonLd", "ready",
            json.dumps({"@type": "Brand", "name": brand_slug.title(), "founder": "TBD"}),
            "Expected +30% fact density score", None, now
        ),
        (
            f"kit-{brand_id}-3", brand_id, f"{brand_slug}-vid-001", "truthClip", "ready",
            json.dumps({"duration": "15s", "content": "Official brand certification", "format": "MP4"}),
            "Expected +15% entity trust", None, now
        )
    ]

    await db.executemany(
        """INSERT INTO fix_kits (id, brand_id, product_id, type, status, payload, impact, deployed_at, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        kits
    )
    await db.commit()


# --- Parity Stats ---

async def _update_parity_stats(db, en_probes: list[dict], fr_probes: list[dict]):
    """
    Update the parity_stats table with EN vs FR analysis from ingested data.
    Computes visibility scores, hallucination counts, and token fertility.
    """
    # EN stats
    en_total = len(en_probes)
    en_mentioned = sum(1 for p in en_probes if p["brand_mentioned"])
    en_visibility = (en_mentioned / en_total * 100) if en_total > 0 else 0
    en_toxic = sum(len(p["toxic_sources"]) for p in en_probes)

    # FR stats
    fr_total = len(fr_probes)
    fr_mentioned = sum(1 for p in fr_probes if p["brand_mentioned"])
    fr_visibility = (fr_mentioned / fr_total * 100) if fr_total > 0 else 0
    fr_toxic = sum(len(p["toxic_sources"]) for p in fr_probes)

    # Token fertility averages
    en_fertilities = [p["fertility"]["fertility"] for p in en_probes if p.get("fertility")]
    fr_fertilities = [p["fertility"]["fertility"] for p in fr_probes if p.get("fertility")]
    en_token_counts = [p["fertility"]["token_count"] for p in en_probes if p.get("fertility")]
    fr_token_counts = [p["fertility"]["token_count"] for p in fr_probes if p.get("fertility")]

    en_avg_fert = round(sum(en_fertilities) / len(en_fertilities), 1) if en_fertilities else 1.0
    fr_avg_fert = round(sum(fr_fertilities) / len(fr_fertilities), 1) if fr_fertilities else 1.0
    en_max_tokens = max(en_token_counts) if en_token_counts else 0
    fr_max_tokens = max(fr_token_counts) if fr_token_counts else 0

    # Only update if we have data
    if en_total == 0 and fr_total == 0:
        return

    # Upsert parity stats (replace existing)
    parity_id = f"parity-ingested-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    await db.execute("DELETE FROM parity_stats")  # Single-row table
    await db.execute(
        """INSERT INTO parity_stats
           (id, en_visibility, fr_visibility, en_queries, fr_queries,
            en_hallucinations, fr_hallucinations,
            en_avg_tokens, en_max_tokens, fr_avg_tokens, fr_max_tokens)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            parity_id,
            round(en_visibility, 1), round(fr_visibility, 1),
            en_total, fr_total,
            en_toxic, fr_toxic,
            en_avg_fert, en_max_tokens,
            fr_avg_fert, fr_max_tokens,
        ),
    )
    await db.commit()


# --- Summary ---

def _build_summary(
    brand_name: str,
    probes: list[dict],
    results: list[dict],
    en_probes: list[dict],
    fr_probes: list[dict],
    gaps_created: int,
) -> dict:
    """Build the final task summary."""
    total = len(probes)
    mentioned = sum(1 for r in results if r["brand_mentioned"])
    mention_rate = round((mentioned / total * 100), 1) if total > 0 else 0

    all_toxic = []
    for r in results:
        all_toxic.extend(r["toxic_sources"])

    # Unique queries
    unique_queries = set(p["query"] for p in probes)

    return {
        "brand": brand_name,
        "total_probes": total,
        "unique_queries": len(unique_queries),
        "en_probes": len(en_probes),
        "fr_probes": len(fr_probes),
        "mention_rate": mention_rate,
        "gaps_created": gaps_created,
        "toxic_sources_found": len(all_toxic),
        "top_toxic_sources": list(set(s["label"] for s in all_toxic))[:5],
        "queries_analyzed": list(unique_queries),
    }
