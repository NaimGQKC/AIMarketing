"""
VisiMind -- Gemini Probe Adapter
Uses Google GenAI SDK to probe Gemini for brand representations.
"""
import asyncio
import time
import re

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import GOOGLE_API_KEY, PROBE_MODEL, PROBE_TEMPERATURE

_client = None


def _get_client():
    global _client
    if _client is None and GOOGLE_API_KEY:
        from google import genai
        _client = genai.Client(api_key=GOOGLE_API_KEY)
    return _client


async def probe(query: str, lang: str, temperature: float | None = None) -> dict:
    """Run a single probe against Gemini. Returns structured result."""
    temp = temperature if temperature is not None else PROBE_TEMPERATURE
    client = _get_client()

    if not client:
        return {
            "provider": "gemini",
            "model": PROBE_MODEL,
            "response_text": "",
            "citations": [],
            "brand_mentioned": False,
            "response_time_ms": 0,
            "error": "No GEMINI_API_KEY configured",
        }

    from google.genai import types

    system_prompt = (
        "You are an AI assistant helping consumers research products and brands. "
        "Answer factually with specific details: brand names, prices, specs, availability. "
        "If you cite information, mention where it comes from."
    )

    start = time.time()
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=PROBE_MODEL,
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temp,
            ),
        )
        elapsed = int((time.time() - start) * 1000)
        text = response.text if response.text else ""
        citations = _extract_urls(text)

        return {
            "provider": "gemini",
            "model": PROBE_MODEL,
            "response_text": text,
            "citations": citations,
            "brand_mentioned": False,
            "response_time_ms": elapsed,
            "error": None,
        }
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        return {
            "provider": "gemini",
            "model": PROBE_MODEL,
            "response_text": "",
            "citations": [],
            "brand_mentioned": False,
            "response_time_ms": elapsed,
            "error": str(e),
        }


def _extract_urls(text: str) -> list[str]:
    return re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
