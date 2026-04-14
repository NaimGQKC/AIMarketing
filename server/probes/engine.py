"""
VisiMind -- Bilingual Probe Engine
Orchestrates EN/FR probes across Gemini + GPT, stores results, computes IAS.
"""
import asyncio
import json
import uuid
from datetime import datetime, timezone

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from probes.providers import gemini as gemini_provider
from probes.providers import openai_provider
from config import OPENAI_API_KEY, GOOGLE_API_KEY

# Probe templates
PROBE_TEMPLATES = {
    "generic_discovery": {
        "EN": "What is the best {category} brand in Montreal?",
        "FR": "Quelle est la meilleure marque de {category} a Montreal?",
    },
    "brand_accuracy": {
        "EN": "Tell me the full specs and details of {brand_name} products.",
        "FR": "Donne-moi les specifications completes des produits {brand_name}.",
    },
    "competitive_displacement": {
        "EN": "{brand_name} vs {competitor}: which is better and why?",
        "FR": "{brand_name} vs {competitor}: lequel est meilleur et pourquoi?",
    },
}


def _build_queries(brand_name: str, category: str, competitor: str) -> list[dict]:
    """Build the set of EN/FR probe queries for a brand."""
    queries = []
    for probe_type, templates in PROBE_TEMPLATES.items():
        for lang, template in templates.items():
            query = template.format(
                brand_name=brand_name,
                category=category or "luxury fashion",
                competitor=competitor or "competitors",
            )
            queries.append({
                "probe_type": probe_type,
                "lang": lang,
                "query": query,
            })
    return queries


async def _run_single_probe(query: str, lang: str) -> list[dict]:
    """Run a query against all available providers."""
    results = []

    if GOOGLE_API_KEY:
        gemini_result = await gemini_provider.probe(query, lang)
        results.append(gemini_result)

    if OPENAI_API_KEY:
        openai_result = await openai_provider.probe(query, lang)
        results.append(openai_result)

    return results


async def run_audit(db, brand_profile: dict) -> dict:
    """
    Run a full bilingual audit for a brand.
    Returns audit_id and structured results.
    """
    audit_id = str(uuid.uuid4())
    brand_name = brand_profile["brand_name"]
    category = brand_profile.get("product_category", "")
    competitor = brand_profile.get("top_competitor", "")

    queries = _build_queries(brand_name, category, competitor)
    all_results = []

    for q in queries:
        provider_results = await _run_single_probe(q["query"], q["lang"])
        for pr in provider_results:
            # Check if brand is mentioned in response
            text_lower = pr["response_text"].lower()
            brand_lower = brand_name.lower()
            pr["brand_mentioned"] = brand_lower in text_lower

            all_results.append({
                "probe_type": q["probe_type"],
                "lang": q["lang"],
                "query": q["query"],
                **pr,
            })

    # Store results in DB
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO audit_results
           (id, brand_profile_id, status, results, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (audit_id, brand_profile["id"], "completed", json.dumps(all_results), now),
    )
    await db.commit()

    return {
        "audit_id": audit_id,
        "brand_name": brand_name,
        "probes_run": len(all_results),
        "providers_used": _providers_used(),
        "results": all_results,
    }


def _providers_used() -> list[str]:
    providers = []
    if GOOGLE_API_KEY:
        providers.append("gemini")
    if OPENAI_API_KEY:
        providers.append("openai")
    return providers
