"""
VisiMind -- OpenAI/GPT Probe Adapter
Uses the openai SDK to probe GPT. Skips gracefully if no API key.
"""
import time

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import OPENAI_API_KEY

_client = None
GPT_MODEL = "gpt-4o-mini"


def _get_client():
    global _client
    if _client is None and OPENAI_API_KEY:
        try:
            from openai import OpenAI
            _client = OpenAI(api_key=OPENAI_API_KEY)
        except ImportError:
            return None
    return _client


async def probe(query: str, lang: str, temperature: float = 0.7) -> dict:
    """Run a single probe against GPT. Returns structured result."""
    client = _get_client()

    if not client:
        return {
            "provider": "openai",
            "model": GPT_MODEL,
            "response_text": "",
            "citations": [],
            "brand_mentioned": False,
            "response_time_ms": 0,
            "error": "No OPENAI_API_KEY configured or openai package not installed",
        }

    import asyncio
    import re

    system_prompt = (
        "You are an AI assistant helping consumers research products and brands. "
        "Answer factually with specific details: brand names, prices, specs, availability. "
        "If you cite information, mention where it comes from."
    )

    start = time.time()
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=temperature,
        )
        elapsed = int((time.time() - start) * 1000)
        text = response.choices[0].message.content or ""
        citations = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)

        return {
            "provider": "openai",
            "model": GPT_MODEL,
            "response_text": text,
            "citations": citations,
            "brand_mentioned": False,
            "response_time_ms": elapsed,
            "error": None,
        }
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        return {
            "provider": "openai",
            "model": GPT_MODEL,
            "response_text": "",
            "citations": [],
            "brand_mentioned": False,
            "response_time_ms": elapsed,
            "error": str(e),
        }
