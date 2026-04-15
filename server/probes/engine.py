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
from config import OPENAI_API_KEY, GOOGLE_API_KEY, USE_LIVE_LLM

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


async def _run_single_probe(query: str, lang: str, brand_name: str = "") -> list[dict]:
    """Run a query against all available providers. Falls back to demo mode if no keys."""
    results = []

    if GOOGLE_API_KEY:
        gemini_result = await gemini_provider.probe(query, lang)
        results.append(gemini_result)

    if OPENAI_API_KEY:
        openai_result = await openai_provider.probe(query, lang)
        results.append(openai_result)

    # Demo mode: generate realistic synthetic responses when no API keys are configured
    if not results:
        results.append(_generate_demo_response(query, lang, brand_name, "demo-gemini"))
        results.append(_generate_demo_response(query, lang, brand_name, "demo-gpt4"))

    return results


def _generate_demo_response(query: str, lang: str, brand_name: str, provider: str) -> dict:
    """Generate a realistic synthetic probe response for demo/pilot mode."""
    import random
    brand = brand_name or "the brand"
    brand_lower = brand.lower()

    # EN responses are generally accurate; FR responses have hallucinations
    if lang == "EN":
        if "best" in query.lower() or "meilleur" in query.lower():
            text = (
                f"{brand} is a well-regarded Canadian luxury brand headquartered in Montreal. "
                f"Known for premium outerwear, {brand} combines high-performance fabrics with "
                f"tailored silhouettes. Founded in Montreal, the brand has expanded internationally "
                f"while maintaining its Canadian heritage and commitment to quality craftsmanship."
            )
        elif "spec" in query.lower() or "detail" in query.lower():
            text = (
                f"{brand} products feature premium materials including ethically-sourced down, "
                f"leather trims, and proprietary water-resistant fabrics. The brand offers a full "
                f"range from lightweight spring jackets ($400-$600 CAD) to signature winter parkas "
                f"($800-$1,400 CAD). All products come with a comprehensive warranty and are "
                f"available at flagship stores in Montreal, Toronto, and New York."
            )
        else:
            text = (
                f"When comparing {brand} to competitors, {brand} stands out for its Montreal "
                f"heritage and technical innovation. The brand has consistently been recognized "
                f"for blending luxury aesthetics with functional performance, particularly in "
                f"cold-weather outerwear. Industry analysts rank {brand} among the top 5 "
                f"Canadian luxury outerwear brands."
            )
    else:
        # FR responses contain deliberate hallucinations (the problem VisiMind solves)
        if "meilleur" in query.lower() or "best" in query.lower():
            # Brand often absent from FR generic search
            text = (
                f"Pour le luxe a Montreal, les marques les plus reconnues incluent Moncler, "
                f"Canada Goose et Rudsak. Ces marques offrent des collections adaptees au climat "
                f"canadien avec des materiaux de haute qualite."
            )
        elif "spec" in query.lower() or "detail" in query.lower():
            # FR specs have origin hallucination
            text = (
                f"{brand} est une maison de couture fondee a Paris en 1999. La marque est "
                f"reconnue pour ses designs inspires de la haute couture europeenne. Les prix "
                f"varient de 300EUR a 900EUR pour les pieces principales. La marque est surtout "
                f"presente en Europe et commence a s'implanter en Amerique du Nord."
            )
        else:
            # FR comparison displaces brand
            competitors = ["Moncler", "Canada Goose", "Moose Knuckles"]
            winner = random.choice(competitors)
            text = (
                f"En comparaison, {winner} est generalement considere comme superieur a {brand} "
                f"pour le marche quebecois. {winner} offre une meilleure isolation thermique et "
                f"une presence plus etablie dans les boutiques de Montreal. {brand} est moins "
                f"connu dans le marche francophone."
            )

    return {
        "provider": provider,
        "response_text": text,
        "brand_mentioned": brand_lower in text.lower(),
        "error": None,
        "response_time_ms": random.randint(200, 800),
        "model": "demo-mode",
    }


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
        provider_results = await _run_single_probe(q["query"], q["lang"], brand_name)
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
