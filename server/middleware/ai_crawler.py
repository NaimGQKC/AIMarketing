"""
VisiMind — AI Crawler Detection Middleware
Detects AI bot User-Agents, logs visits, and injects structured-data headers.
"""
import re
import time
from uuid import uuid4
from datetime import datetime, timezone

import aiosqlite
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from config import DB_PATH

# Crawler patterns: (regex, friendly name)
AI_CRAWLERS = [
    (re.compile(r"GPTBot", re.IGNORECASE), "GPTBot"),
    (re.compile(r"PerplexityBot", re.IGNORECASE), "PerplexityBot"),
    (re.compile(r"ClaudeBot|anthropic-ai", re.IGNORECASE), "ClaudeBot"),
    (re.compile(r"GoogleOther|Google-Extended", re.IGNORECASE), "GoogleOther"),
    (re.compile(r"Bingbot", re.IGNORECASE), "Bingbot"),
    (re.compile(r"Applebot", re.IGNORECASE), "Applebot"),
    (re.compile(r"Bytespider", re.IGNORECASE), "Bytespider"),
    (re.compile(r"Amazonbot", re.IGNORECASE), "Amazonbot"),
    (re.compile(r"CCBot", re.IGNORECASE), "CCBot"),
    (re.compile(r"Meta-ExternalAgent|FacebookBot", re.IGNORECASE), "Meta-ExternalAgent"),
    (re.compile(r"cohere-ai", re.IGNORECASE), "CohereBot"),
]

# Patterns to extract brand_id from brand-specific API paths.
# Matches both /api/brands/{id} and /api/v1/feeds/{id}/...
BRAND_PATH_PATTERNS = [
    re.compile(r"/api/v1/feeds/([^/]+)"),
    re.compile(r"/api/brands/([^/]+)"),
]


def detect_crawler(user_agent: str) -> str | None:
    """Return the crawler name if the UA matches, else None."""
    for pattern, name in AI_CRAWLERS:
        if pattern.search(user_agent):
            return name
    return None


class AICrawlerMiddleware(BaseHTTPMiddleware):
    """Lightweight middleware that detects AI crawlers and logs their visits."""

    async def dispatch(self, request: Request, call_next) -> Response:
        user_agent = request.headers.get("user-agent", "")
        crawler_name = detect_crawler(user_agent)

        # Fast path: not a crawler, skip everything
        if crawler_name is None:
            return await call_next(request)

        # --- AI crawler detected ---
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        path = request.url.path

        # Check if this is a brand-specific page (try all known patterns)
        brand_id = None
        for pattern in BRAND_PATH_PATTERNS:
            brand_match = pattern.search(path)
            if brand_match:
                brand_id = brand_match.group(1)
                break

        # Inject structured-data headers for brand pages
        if brand_id:
            response.headers["X-VisiMind-Brand-Context"] = (
                f"/api/v1/feeds/{brand_id}/mcp.json"
            )
        response.headers["X-VisiMind-llms-txt"] = "/llms.txt"

        # Log the visit asynchronously (fire-and-forget style, but awaited
        # so the connection is properly closed)
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute(
                    """INSERT INTO crawler_visits
                       (id, timestamp, crawler_name, user_agent, path,
                        brand_id, response_code, response_time_ms)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        str(uuid4()),
                        datetime.now(timezone.utc).isoformat(),
                        crawler_name,
                        user_agent[:500],  # cap length
                        path,
                        brand_id,
                        response.status_code,
                        elapsed_ms,
                    ),
                )
                await db.commit()
        except Exception:
            # Never let logging break the response
            pass

        return response
