"""
VisiMind -- Gemini Probe Adapter
Uses Google GenAI SDK to probe Gemini via Vertex AI or API key.
Includes retry with exponential backoff for rate limits.
"""
import asyncio
import time
import re

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import (
    GOOGLE_API_KEY, PROBE_MODEL, PROBE_TEMPERATURE,
    USE_VERTEX_AI, GCP_PROJECT_ID, GCP_LOCATION, GCP_CREDENTIALS_FILE,
)

_client = None

MAX_RETRIES = 3
BACKOFF_BASE = 1.5  # seconds: 1.5, 3, 6


def _get_client():
    global _client
    if _client is not None:
        return _client

    from google import genai

    if USE_VERTEX_AI and GCP_CREDENTIALS_FILE and Path(GCP_CREDENTIALS_FILE).exists():
        from google.oauth2 import credentials as oauth2_creds
        import json

        with open(GCP_CREDENTIALS_FILE) as f:
            cred_data = json.load(f)

        if cred_data.get("type") == "authorized_user":
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            creds = Credentials(
                token=None,
                refresh_token=cred_data["refresh_token"],
                client_id=cred_data["client_id"],
                client_secret=cred_data["client_secret"],
                token_uri="https://oauth2.googleapis.com/token",
            )
            creds.refresh(Request())
        else:
            from google.oauth2.service_account import Credentials
            creds = Credentials.from_service_account_file(
                GCP_CREDENTIALS_FILE,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

        _client = genai.Client(
            vertexai=True,
            project=GCP_PROJECT_ID,
            location=GCP_LOCATION,
            credentials=creds,
        )
        print(f"[Gemini] Using Vertex AI ({GCP_PROJECT_ID}/{GCP_LOCATION})")
        return _client

    if GOOGLE_API_KEY:
        _client = genai.Client(api_key=GOOGLE_API_KEY)
        print("[Gemini] Using API key")
        return _client

    return None


async def probe(query: str, lang: str, temperature: float | None = None) -> dict:
    """Run a single probe against Gemini with retry on transient errors."""
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
            "error": "No Gemini credentials configured",
        }

    from google.genai import types

    system_prompt = (
        "You are an AI assistant helping consumers research products and brands. "
        "Answer factually with specific details: brand names, prices, specs, availability. "
        "If you cite information, mention where it comes from."
    )

    last_error = None
    start = time.time()

    for attempt in range(MAX_RETRIES + 1):
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
            last_error = e
            error_str = str(e).lower()
            is_retryable = "429" in error_str or "resource exhausted" in error_str or "500" in error_str or "503" in error_str
            if is_retryable and attempt < MAX_RETRIES:
                wait = BACKOFF_BASE * (2 ** attempt)
                print(f"[Gemini] Retry {attempt + 1}/{MAX_RETRIES} after {wait:.1f}s -- {e}")
                await asyncio.sleep(wait)
                continue
            break

    elapsed = int((time.time() - start) * 1000)
    return {
        "provider": "gemini",
        "model": PROBE_MODEL,
        "response_text": "",
        "citations": [],
        "brand_mentioned": False,
        "response_time_ms": elapsed,
        "error": str(last_error),
    }


def _extract_urls(text: str) -> list[str]:
    return re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
