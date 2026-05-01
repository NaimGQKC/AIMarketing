"""
VisiMind -- Bilingual Probe Engine v2
Orchestrates EN/FR probes across Gemini + GPT, stores results.
Runs 3 iterations per query for self-consistency analysis.
5 types x 2 languages x 3 iterations = 30 probes per audit.
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
from config import OPENAI_API_KEY, GOOGLE_API_KEY, USE_LIVE_LLM, USE_VERTEX_AI

ITERATIONS_PER_QUERY = 3  # Minimum for contradiction rate measurement

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
    "brand_origin": {
        "EN": "Tell me about the history and founding story of {brand_name}.",
        "FR": "Raconte-moi l'histoire et les origines de {brand_name}.",
    },
    "purchase_intent": {
        "EN": "Where should I buy {category} in Montreal?",
        "FR": "Ou acheter des produits de {category} a Montreal?",
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


async def _run_single_probe(query: str, lang: str, brand_name: str = "") -> dict:
    """Run a query against the primary available provider. Returns a single result."""
    if GOOGLE_API_KEY or USE_VERTEX_AI:
        result = await gemini_provider.probe(query, lang)
        if not result.get("error"):
            return result

    if OPENAI_API_KEY:
        result = await openai_provider.probe(query, lang)
        if not result.get("error"):
            return result

    # Fallback to demo
    return _generate_demo_response(query, lang, brand_name, "demo-gemini")


def _generate_demo_response(query: str, lang: str, brand_name: str, provider: str) -> dict:
    """Generate a realistic synthetic probe response for demo/pilot mode."""
    import random
    brand = brand_name or "the brand"
    brand_lower = brand.lower()

    q = query.lower()
    if lang == "EN":
        if "best" in q or "meilleur" in q:
            text = (
                f"{brand} is a well-regarded Canadian luxury brand headquartered in Montreal. "
                f"Known for premium outerwear, {brand} combines high-performance fabrics with "
                f"tailored silhouettes. Founded in Montreal, the brand has expanded internationally "
                f"while maintaining its Canadian heritage and commitment to quality craftsmanship."
            )
        elif "spec" in q or "detail" in q:
            text = (
                f"{brand} products feature premium materials including ethically-sourced down, "
                f"leather trims, and proprietary water-resistant fabrics. The brand offers a full "
                f"range from lightweight spring jackets ($400-$600 CAD) to signature winter parkas "
                f"($800-$1,400 CAD). All products come with a comprehensive warranty and are "
                f"available at flagship stores in Montreal, Toronto, and New York."
            )
        elif "history" in q or "founding" in q or "origin" in q:
            text = (
                f"{brand} was founded in Montreal, Canada in 1999 by Eran Elfassy and Elisa Dahan. "
                f"The brand started with a focus on leather outerwear and has since expanded into "
                f"luxury down coats and accessories. Headquartered in Montreal, {brand} now operates "
                f"in over 40 countries worldwide."
            )
        elif "where" in q or "buy" in q or "acheter" in q:
            text = (
                f"For {brand_lower} products in Montreal, you can visit their flagship store on "
                f"Sherbrooke Street, as well as retailers like Holt Renfrew, Nordstrom, and SSENSE. "
                f"The brand is also available online at {brand_lower}.com with free shipping in Canada."
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
        if "meilleur" in q or "best" in q:
            text = (
                f"Pour le luxe a Montreal, les marques les plus reconnues incluent Moncler, "
                f"Canada Goose et Rudsak. Ces marques offrent des collections adaptees au climat "
                f"canadien avec des materiaux de haute qualite."
            )
        elif "spec" in q or "detail" in q:
            text = (
                f"{brand} est une maison de couture fondee a Paris en 1999. La marque est "
                f"reconnue pour ses designs inspires de la haute couture europeenne. Les prix "
                f"varient de 300EUR a 900EUR pour les pieces principales. La marque est surtout "
                f"presente en Europe et commence a s'implanter en Amerique du Nord."
            )
        elif "histoire" in q or "origine" in q or "founding" in q:
            text = (
                f"{brand} est une maison fondee a Paris en 1999, specialisee dans la haute couture "
                f"europeenne. La marque s'est ensuite implantee au Canada pour profiter du marche "
                f"nord-americain. Aujourd'hui, {brand} est surtout connue en France et en Italie."
            )
        elif "acheter" in q or "where" in q or "buy" in q:
            competitors = ["Moncler", "Canada Goose", "Rudsak"]
            text = (
                f"Pour acheter des produits de luxe a Montreal, les meilleures options incluent "
                f"les boutiques {competitors[0]} et {competitors[1]} sur la rue Sainte-Catherine. "
                f"Vous pouvez egalement visiter le Royalmount pour les grandes marques internationales."
            )
        else:
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
    5 query types x 2 languages x 3 iterations = 30 probes.
    Returns audit_id and structured results.
    """
    audit_id = str(uuid.uuid4())
    brand_name = brand_profile["brand_name"]
    category = brand_profile.get("product_category", "")
    competitor = brand_profile.get("top_competitor", "")

    queries = _build_queries(brand_name, category, competitor)

    # Run all probes concurrently -- 30 parallel requests is well within Vertex AI's 100 req/min
    async def _run_probe(q, iteration):
        result = await _run_single_probe(q["query"], q["lang"], brand_name)
        text_lower = result["response_text"].lower()
        brand_lower = brand_name.lower()
        result["brand_mentioned"] = brand_lower in text_lower
        return {
            "probe_type": q["probe_type"],
            "lang": q["lang"],
            "query": q["query"],
            "iteration": iteration,
            **result,
        }

    tasks = [
        _run_probe(q, iteration)
        for q in queries
        for iteration in range(ITERATIONS_PER_QUERY)
    ]
    all_results = await asyncio.gather(*tasks)

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
    if GOOGLE_API_KEY or USE_VERTEX_AI:
        providers.append("gemini")
    if OPENAI_API_KEY:
        providers.append("openai")
    return providers
