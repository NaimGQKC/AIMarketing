"""
VisiMind — Engine 1: Inference Lab
Headless agentic probing, citation extraction, bilingual parity audit.
Uses polling pattern: probe_query returns task_id, frontend polls /api/tasks/{id}.
"""
import asyncio
import json
import uuid
import time
import random
from datetime import datetime

from config import (
    GOOGLE_API_KEY, USE_LIVE_LLM, PROBE_MODEL, PROBE_ITERATIONS,
    USE_OLLAMA, OLLAMA_MODEL, OLLAMA_URL
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


# --- Core Probing ---

async def probe_query_single(query: str, lang: str, model: str = PROBE_MODEL) -> dict:
    """
    Execute a single probe against an LLM and extract recommendations + citations.
    Returns structured probe result with logprob-level data.
    """
    if USE_OLLAMA:
        return await _ollama_probe(query, lang, OLLAMA_MODEL)

    client = _get_client()

    if client and USE_LIVE_LLM:
        return await _live_probe(client, query, lang, model)
    else:
        return await _simulated_probe(query, lang)



async def _live_probe(client, query: str, lang: str, model: str) -> dict:
    """Probe via live Gemini API."""
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
                temperature=0.8,  # Higher temp for non-determinism testing
            ),
        )

        response_text = response.text if response.text else ""

        # Extract citations from grounding metadata if available
        citations = []
        brand_mentioned = False
        brand_logprob = None

        # Parse response for citation-like URLs
        citations = _extract_citation_urls(response_text)

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


async def _ollama_probe(query: str, lang: str, model: str) -> dict:
    """Probe via local Ollama instance."""
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
                    "stream": False
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            response_text = data.get("response", "")
            
        citations = _extract_citation_urls(response_text)
        brand_mentioned = any(b in response_text.lower() for b in ["mackage", "ssense", "aldo"])
        
        # Mock logprob for Ollama since it doesn't easily expose token-level logprobs via the basic API
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
    await asyncio.sleep(random.uniform(0.05, 0.15))  # Simulate latency

    query_lower = query.lower()

    # Simulate different response profiles based on query content
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

    # Detect which brand is relevant
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

    # Build simulated response
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


async def run_probe_task(db, task_id: str, query: str, lang: str, iterations: int):
    """
    Background task: run N probe iterations, updating task progress.
    This is what the /api/diagnose/probe endpoint kicks off.
    """
    try:
        await db.execute(
            "UPDATE tasks SET status = 'running', total = ? WHERE id = ?",
            (iterations, task_id),
        )
        await db.commit()

        results = []
        mention_count = 0
        total_logprob = 0.0
        logprob_count = 0

        for i in range(iterations):
            result = await probe_query_single(query, lang)
            result_id = str(uuid.uuid4())

            # Store probe result
            await db.execute(
                """INSERT INTO probe_results
                   (id, task_id, query, lang, iteration, model, response_text,
                    citations, brand_mentioned, brand_mention_logprob,
                    recommendation_position, response_time_ms)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    result_id, task_id, query, lang, i + 1, PROBE_MODEL,
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

            results.append(result)

            # Update progress
            await db.execute(
                "UPDATE tasks SET progress = ?, updated_at = ? WHERE id = ?",
                (i + 1, datetime.utcnow().isoformat(), task_id),
            )
            await db.commit()

        # Compute final stats
        avg_logprob = round(total_logprob / logprob_count, 4) if logprob_count > 0 else None
        mention_rate = round(mention_count / iterations * 100, 1)

        # Aggregate citation sources
        all_citations = []
        for r in results:
            all_citations.extend(r["citations"])
        citation_freq = {}
        for c in all_citations:
            citation_freq[c] = citation_freq.get(c, 0) + 1

        summary = {
            "query": query,
            "lang": lang,
            "iterations": iterations,
            "mention_rate": mention_rate,
            "avg_logprob": avg_logprob,
            "avg_response_time_ms": round(
                sum(r["response_time_ms"] for r in results) / len(results)
            ),
            "top_citations": sorted(
                citation_freq.items(), key=lambda x: x[1], reverse=True
            )[:5],
            "recommendation_positions": [
                r["recommendation_position"] for r in results if r["recommendation_position"]
            ],
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
    import re
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
    """
    Classify the signal gap type based on probe statistics.
    """
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
