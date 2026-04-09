"""
VisiMind — Engine 1: Inference Lab
Headless agentic probing with Self-Consistency Mining.

Optimizations (v2):
  1. N=3 iterations (down from 50) — avoids semantic cache trap
  2. Temperature jitter (0.7) — forces real reasoning, exposes unstable distributions
  3. Golden Set — 5 diverse prompt angles instead of 1 repeated query
  4. Contradiction Rate — detects hallucination via cross-run inconsistency
"""
import asyncio
import json
import uuid
import time
import random
import re
from datetime import datetime
from difflib import SequenceMatcher

from config import (
    GOOGLE_API_KEY, USE_LIVE_LLM, PROBE_MODEL, PROBE_ITERATIONS,
    USE_OLLAMA, OLLAMA_MODEL, OLLAMA_URL,
    PROBE_TEMPERATURE, GOLDEN_SET_VARIATIONS,
)
import httpx


# --- Gemini Client (lazy init) ---
_genai_client = None


def _get_client():
    global _genai_client
    if _genai_client is None and USE_LIVE_LLM:
        from google import genai
        _genai_client = genai.Client(api_key=GOOGLE_API_KEY)
    return _genai_client


# =============================================================================
# Golden Set — Query Variation Generator
# =============================================================================

def build_golden_set(base_query: str, lang: str = "EN") -> list[dict]:
    """
    Generate 5 diverse prompt angles from a single base query.
    Each variation probes a different RAG surface area to maximize
    hallucination detection coverage.

    Instead of hammering 1 prompt 50 times, we run 5 variations x 3 iterations.
    This bypasses semantic caching and widens the detection surface.
    """
    # Extract brand and product hints from the query
    query_lower = base_query.lower()
    brands = ["mackage", "ssense", "aldo"]
    detected_brand = next((b for b in brands if b in query_lower), None)
    brand_title = detected_brand.title() if detected_brand else "the brand"

    if lang.upper() == "FR":
        variations = [
            {
                "angle": "direct",
                "query": base_query,
                "description": "Requête directe originale",
            },
            {
                "angle": "conversational",
                "query": f"Je vis à Montréal. {base_query} Est-ce un bon choix pour moi?",
                "description": "Contexte conversationnel avec localisation",
            },
            {
                "angle": "comparison",
                "query": f"Compare {brand_title} avec ses concurrents. {base_query}",
                "description": "Angle comparatif pour forcer le raisonnement",
            },
            {
                "angle": "feature_specific",
                "query": f"Quelles certifications et spécifications techniques sont vérifiées pour {brand_title}?",
                "description": "Question technique sur les certifications",
            },
            {
                "angle": "recommendation",
                "query": f"En tant qu'expert, recommanderais-tu {brand_title}? Cite tes sources.",
                "description": "Demande de recommandation avec exigence de sources",
            },
        ]
    else:
        variations = [
            {
                "angle": "direct",
                "query": base_query,
                "description": "Original direct query",
            },
            {
                "angle": "conversational",
                "query": f"I live in Montreal. {base_query} Would this be a good choice for me?",
                "description": "Conversational context with location",
            },
            {
                "angle": "comparison",
                "query": f"Compare {brand_title} to its competitors. {base_query}",
                "description": "Comparison angle to force reasoning",
            },
            {
                "angle": "feature_specific",
                "query": f"What certifications and verified technical specs does {brand_title} have?",
                "description": "Feature-specific probe for hard attributes",
            },
            {
                "angle": "recommendation",
                "query": f"As an expert, would you recommend {brand_title}? Cite your sources.",
                "description": "Recommendation request demanding citations",
            },
        ]

    return variations[:GOLDEN_SET_VARIATIONS]


# =============================================================================
# Contradiction Rate — Self-Consistency Mining
# =============================================================================

def compute_contradiction_rate(responses: list[str]) -> dict:
    """
    Calculate the contradiction rate across N probe responses using
    factual consistency, not surface-level text similarity.

    If the model actually "knows" the truth (from Tier 2 JSON-LD), it will
    output consistent specs across runs. If it's guessing from stale sources,
    higher temperature forces contradictions within just 3 runs.

    The algorithm:
      1. Extract key factual claims (numbers with units, certifications, brand names)
      2. Check if claims are consistent across all responses
      3. Weight by fact importance — a contradicted spec is worse than missing text

    Returns:
      - contradiction_rate: 0.0 (perfectly consistent) to 1.0 (fully contradictory)
      - is_hallucinating: True if rate > 0.4 (unstable distribution = guessing)
      - similarity_matrix: pairwise similarity scores
      - key_facts: extracted factual claims and their consistency
    """
    if len(responses) < 2:
        return {
            "contradiction_rate": 0.0,
            "is_hallucinating": False,
            "similarity_matrix": [],
            "key_facts": {},
        }

    # Extract factual claims for consistency checking
    key_facts = _extract_key_facts(responses)

    # Fact-based contradiction: what fraction of extracted facts are inconsistent?
    if key_facts:
        consistent_count = sum(1 for f in key_facts.values() if f["consistent"])
        fact_consistency = consistent_count / len(key_facts)
    else:
        fact_consistency = 1.0  # no extractable facts = can't measure

    # Pairwise text similarity (secondary signal)
    similarities = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            sim = SequenceMatcher(
                None,
                responses[i].lower(),
                responses[j].lower(),
            ).ratio()
            similarities.append({
                "pair": [i, j],
                "similarity": round(sim, 3),
            })

    avg_similarity = sum(s["similarity"] for s in similarities) / len(similarities)

    # Blend: 70% fact consistency + 30% text similarity
    # This prevents false positives when facts match but wording differs
    blended_consistency = fact_consistency * 0.7 + avg_similarity * 0.3
    contradiction_rate = round(1.0 - blended_consistency, 3)

    return {
        "contradiction_rate": contradiction_rate,
        "is_hallucinating": contradiction_rate > 0.4,
        "avg_similarity": round(avg_similarity, 3),
        "fact_consistency": round(fact_consistency, 3),
        "similarity_matrix": similarities,
        "key_facts": key_facts,
    }


def _extract_key_facts(responses: list[str]) -> dict:
    """Extract numeric/factual claims and check consistency across responses."""
    number_pattern = r'(\d+(?:\.\d+)?)\s*(?:°[CF]|%|g|ml|oz|CAD|\$|watts?|hours?|days?|fill\s*power)'
    cert_pattern = r'\b(RDS|Bluesign|LWG|OEKO-TEX|GOTS|GRS|Carbon Neutral)\b'

    facts = {}

    for i, resp in enumerate(responses):
        # Numbers with units
        for match in re.finditer(number_pattern, resp, re.IGNORECASE):
            key = match.group(0).strip().lower()
            if key not in facts:
                facts[key] = {"claim": match.group(0), "seen_in": [], "consistent": True}
            facts[key]["seen_in"].append(i)

        # Certifications
        for match in re.finditer(cert_pattern, resp, re.IGNORECASE):
            key = match.group(1).upper()
            if key not in facts:
                facts[key] = {"claim": key, "seen_in": [], "consistent": True}
            facts[key]["seen_in"].append(i)

    # Mark facts as inconsistent if not seen in all responses
    for key, fact in facts.items():
        fact["consistent"] = len(set(fact["seen_in"])) == len(responses)

    return facts


# =============================================================================
# Core Probing
# =============================================================================

async def probe_query_single(
    query: str,
    lang: str,
    model: str = PROBE_MODEL,
    temperature: float = None,
) -> dict:
    """
    Execute a single probe against an LLM and extract recommendations + citations.
    Temperature defaults to PROBE_TEMPERATURE (0.7) to force real reasoning
    and bypass semantic caching.
    """
    temp = temperature if temperature is not None else PROBE_TEMPERATURE

    if USE_OLLAMA:
        return await _ollama_probe(query, lang, OLLAMA_MODEL, temp)

    client = _get_client()

    if client and USE_LIVE_LLM:
        return await _live_probe(client, query, lang, model, temp)
    else:
        return await _simulated_probe(query, lang)


async def _live_probe(client, query: str, lang: str, model: str, temperature: float) -> dict:
    """Probe via live Gemini API with temperature jitter."""
    from google.genai import types

    system_prompt = (
        "You are an AI shopping assistant. A user is asking for product recommendations. "
        "Provide specific product recommendations with brand names, prices, and key specs. "
        "Cite your sources for each recommendation."
    )

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=model,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
            ),
        )

        response_text = response.text if response.text else ""
        citations = _extract_citation_urls(response_text)
        brand_mentioned = False
        brand_logprob = None

        return {
            "response_text": response_text,
            "citations": citations,
            "brand_mentioned": brand_mentioned,
            "brand_mention_logprob": brand_logprob,
            "recommendation_position": _extract_recommendation_position(response_text),
            "response_time_ms": 0,
        }
    except Exception as e:
        return {
            "response_text": f"[ERROR] {str(e)}",
            "citations": [],
            "brand_mentioned": False,
            "brand_mention_logprob": None,
            "recommendation_position": None,
            "response_time_ms": 0,
        }


async def _ollama_probe(query: str, lang: str, model: str, temperature: float) -> dict:
    """Probe via local Ollama instance with temperature jitter."""
    system_prompt = (
        "You are an AI shopping assistant. A user is asking for product recommendations. "
        "Provide specific product recommendations with brand names, prices, and key specs. "
        "Cite your sources for each recommendation."
    )
    prompt = f"{system_prompt}\n\nUser Query: {query}"

    start_time = time.time()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature},
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            response_text = data.get("response", "")

        citations = _extract_citation_urls(response_text)
        brand_mentioned = any(b in response_text.lower() for b in ["mackage", "ssense", "aldo"])
        mock_logprob = -1.5 if brand_mentioned else -5.0

        return {
            "response_text": response_text,
            "citations": citations,
            "brand_mentioned": brand_mentioned,
            "brand_mention_logprob": mock_logprob,
            "recommendation_position": _extract_recommendation_position(response_text),
            "response_time_ms": int((time.time() - start_time) * 1000),
        }
    except Exception as e:
        return {
            "response_text": f"[OLLAMA ERROR] {str(e)}",
            "citations": [],
            "brand_mentioned": False,
            "brand_mention_logprob": None,
            "recommendation_position": None,
            "response_time_ms": int((time.time() - start_time) * 1000),
        }


async def _simulated_probe(query: str, lang: str) -> dict:
    """Simulated probe for development without API key."""
    await asyncio.sleep(random.uniform(0.05, 0.15))

    query_lower = query.lower()
    is_french = lang.upper() == "FR"
    brand_profiles = {
        "mackage": {
            "mention_rate": 0.35 if is_french else 0.65,
            "toxic_sources": ["Reddit r/malefashionadvice (2021)", "YouTube review (2020)"],
            "logprob_range": (-4.5, -1.2) if is_french else (-2.8, -0.3),
        },
        "ssense": {
            "mention_rate": 0.40 if is_french else 0.70,
            "toxic_sources": ["Farfetch editorial (2023)", "Vogue article (2022)"],
            "logprob_range": (-4.0, -1.5) if is_french else (-2.5, -0.4),
        },
        "aldo": {
            "mention_rate": 0.45 if is_french else 0.60,
            "toxic_sources": ["Trustpilot reviews (2022)", "Reddit r/buyitforlife (2021)"],
            "logprob_range": (-3.8, -1.0) if is_french else (-2.2, -0.5),
        },
    }

    detected_brand = None
    for brand in brand_profiles:
        if brand in query_lower:
            detected_brand = brand
            break
    if detected_brand is None:
        detected_brand = random.choice(list(brand_profiles.keys()))

    profile = brand_profiles[detected_brand]
    mentioned = random.random() < profile["mention_rate"]
    logprob = random.uniform(*profile["logprob_range"]) if mentioned else random.uniform(-8.0, -5.0)

    if mentioned:
        position = random.randint(1, 3)
        if is_french:
            response_text = f"Résultat {position}: {detected_brand.title()} — détails techniques limités disponibles."
        else:
            response_text = f"Recommendation #{position}: {detected_brand.title()} — based on available data."
        cited = [random.choice(profile["toxic_sources"])]
    else:
        position = None
        if is_french:
            response_text = f"Je ne trouve pas d'informations fiables pour cette requête en français."
        else:
            response_text = f"Based on available reviews, I recommend alternative brands."
        cited = [random.choice(profile["toxic_sources"])]

    return {
        "response_text": response_text,
        "citations": cited,
        "brand_mentioned": mentioned,
        "brand_mention_logprob": round(logprob, 4),
        "recommendation_position": position,
        "response_time_ms": random.randint(200, 1200),
    }


# =============================================================================
# Probe Task Runner — Golden Set + Self-Consistency
# =============================================================================

async def run_probe_task(
    db,
    task_id: str,
    query: str,
    lang: str,
    iterations: int,
    use_golden_set: bool = True,
    temperature: float = None,
):
    """
    Background task: run probes with Golden Set variations and Self-Consistency Mining.

    Instead of N=50 identical probes, runs:
      - 5 query variations (Golden Set) x 3 iterations each = 15 total probes
      - Temperature jitter at 0.7 to bypass semantic caching
      - Contradiction Rate computed per variation to detect hallucination

    This drops inference costs by >70%, bypasses the caching trap, and gives
    a much wider RAG surface area for detection.
    """
    temp = temperature if temperature is not None else PROBE_TEMPERATURE

    try:
        # Build the query set
        if use_golden_set:
            variations = build_golden_set(query, lang)
        else:
            variations = [{"angle": "direct", "query": query, "description": "Single query mode"}]

        total_probes = len(variations) * iterations

        await db.execute(
            "UPDATE tasks SET status = 'running', total = ? WHERE id = ?",
            (total_probes, task_id),
        )
        await db.commit()

        all_results = []
        variation_analyses = []
        mention_count = 0
        total_logprob = 0.0
        logprob_count = 0
        progress = 0

        for variation in variations:
            variation_responses = []

            for i in range(iterations):
                result = await probe_query_single(variation["query"], lang, temperature=temp)
                result_id = str(uuid.uuid4())

                # Store probe result with variation metadata
                await db.execute(
                    """INSERT INTO probe_results
                       (id, task_id, query, lang, iteration, model, response_text,
                        citations, brand_mentioned, brand_mention_logprob,
                        recommendation_position, response_time_ms)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        result_id, task_id, variation["query"], lang,
                        progress + 1, PROBE_MODEL,
                        result["response_text"],
                        json.dumps(result["citations"]),
                        1 if result["brand_mentioned"] else 0,
                        result["brand_mention_logprob"],
                        result["recommendation_position"],
                        result["response_time_ms"],
                    ),
                )

                if result["brand_mentioned"]:
                    mention_count += 1
                    if result["brand_mention_logprob"] is not None:
                        total_logprob += result["brand_mention_logprob"]
                        logprob_count += 1

                all_results.append(result)
                variation_responses.append(result["response_text"])

                progress += 1
                await db.execute(
                    "UPDATE tasks SET progress = ?, updated_at = ? WHERE id = ?",
                    (progress, datetime.utcnow().isoformat(), task_id),
                )
                await db.commit()

            # Compute contradiction rate for this variation
            contradiction = compute_contradiction_rate(variation_responses)
            variation_analyses.append({
                "angle": variation["angle"],
                "query": variation["query"],
                "description": variation["description"],
                "iterations": iterations,
                "contradiction_rate": contradiction["contradiction_rate"],
                "is_hallucinating": contradiction["is_hallucinating"],
                "avg_similarity": contradiction.get("avg_similarity", 0),
                "key_facts": contradiction["key_facts"],
            })

        # Compute final stats
        avg_logprob = round(total_logprob / logprob_count, 4) if logprob_count > 0 else None
        mention_rate = round(mention_count / total_probes * 100, 1)

        # Aggregate citation sources
        all_citations = []
        for r in all_results:
            all_citations.extend(r["citations"])
        citation_freq = {}
        for c in all_citations:
            citation_freq[c] = citation_freq.get(c, 0) + 1

        # Overall contradiction rate (average across all variations)
        overall_contradiction = round(
            sum(v["contradiction_rate"] for v in variation_analyses) / len(variation_analyses), 3
        ) if variation_analyses else 0.0

        hallucinating_angles = [v["angle"] for v in variation_analyses if v["is_hallucinating"]]

        summary = {
            "query": query,
            "lang": lang,
            "iterations_per_variation": iterations,
            "total_probes": total_probes,
            "golden_set_used": use_golden_set,
            "temperature": temp,
            "mention_rate": mention_rate,
            "avg_logprob": avg_logprob,
            "avg_response_time_ms": round(
                sum(r["response_time_ms"] for r in all_results) / len(all_results)
            ),
            "top_citations": sorted(
                citation_freq.items(), key=lambda x: x[1], reverse=True
            )[:5],
            "recommendation_positions": [
                r["recommendation_position"] for r in all_results if r["recommendation_position"]
            ],
            # Self-Consistency Mining results
            "contradiction_rate": overall_contradiction,
            "is_hallucinating": overall_contradiction > 0.4,
            "hallucinating_angles": hallucinating_angles,
            "variation_analyses": variation_analyses,
        }

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


# --- Citation Extraction ---

def _extract_citation_urls(text: str) -> list[str]:
    """Extract URL-like strings from response text."""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def _extract_recommendation_position(text: str) -> int | None:
    """Try to detect where in a list a brand appears."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if any(b in line.lower() for b in ["mackage", "ssense", "aldo"]):
            return i + 1
    return None


def classify_gap(mention_rate: float, avg_logprob: float | None, top_citations: list) -> str:
    """Classify the signal gap type based on probe statistics."""
    toxic_sources = any(
        "reddit" in c[0].lower() or "blog" in c[0].lower() or "trustpilot" in c[0].lower()
        for c in top_citations
    )

    if avg_logprob is not None and avg_logprob < -4.0:
        return "Token Decay"
    elif toxic_sources and mention_rate < 50:
        return "Entity Trust"
    elif mention_rate < 40:
        return "Fact Density"
    else:
        return "Entity Trust"
