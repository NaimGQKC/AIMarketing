"""
VisiMind — "Are You Invisible?" AI Crawler Check
Free top-of-funnel tool: checks if a website accidentally blocks AI crawlers.
"""
import asyncio
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api", tags=["Crawler Check"])

# AI crawler User-Agent strings
CRAWLERS = {
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) GPTBot/1.0 +https://openai.com/gptbot",
    "PerplexityBot": "PerplexityBot/1.0",
    "ClaudeBot": "ClaudeBot/1.0",
    "GoogleOther": "GoogleOther",
    "Browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

BLOCKED_CODES = {401, 403, 503}
ALLOWED_CODES = {200, 301, 302}
TIMEOUT = 10.0


def _normalise_url(url: str) -> str:
    """Ensure the URL has a scheme."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")


async def _probe_crawler(client: httpx.AsyncClient, url: str, name: str, ua: str) -> dict:
    """Send a single request with a specific User-Agent and measure response."""
    try:
        start = time.perf_counter()
        resp = await client.get(url, headers={"User-Agent": ua}, follow_redirects=True)
        elapsed_ms = round((time.perf_counter() - start) * 1000)
        return {
            "status_code": resp.status_code,
            "blocked": resp.status_code in BLOCKED_CODES,
            "response_ms": elapsed_ms,
        }
    except httpx.TimeoutException:
        return {"status_code": None, "blocked": True, "response_ms": None, "error": "timeout"}
    except httpx.RequestError as exc:
        return {"status_code": None, "blocked": True, "response_ms": None, "error": str(exc)[:120]}


def _parse_robots_txt(text: str, ai_crawler_names: list[str]) -> dict:
    """Parse robots.txt and check which AI crawlers are blocked."""
    blocks = []
    allows = []
    raw_rules = []

    # Normalise names for case-insensitive matching
    lower_names = {n.lower(): n for n in ai_crawler_names}

    current_agents: list[str] = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue

        if line.lower().startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip()
            current_agents.append(agent)
        elif line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path in ("", None):
                continue
            # Check if this disallow applies to any AI crawler
            for agent in current_agents:
                agent_lower = agent.lower()
                if agent_lower == "*":
                    # Blanket block
                    if path == "/":
                        for name in ai_crawler_names:
                            if name not in blocks:
                                blocks.append(name)
                                raw_rules.append(f"User-agent: *\nDisallow: /")
                elif agent_lower in lower_names:
                    real_name = lower_names[agent_lower]
                    if real_name not in blocks:
                        blocks.append(real_name)
                        raw_rules.append(f"User-agent: {agent}\nDisallow: {path}")
        elif line.lower().startswith("allow:"):
            # Reset: if we see Allow after Disallow for same agent, it's complex.
            # Keep it simple — just track explicit allows.
            pass
        else:
            # New directive group resets current agents
            if not line.lower().startswith(("sitemap:", "crawl-delay:")):
                current_agents = []
            continue

        # Reset agents on blank-ish transition (handled by continue above)
        # Actually, agents accumulate until a non-user-agent, non-directive line
        # but we keep accumulating for the group.

    # Anything not blocked is considered allowed
    for name in ai_crawler_names:
        if name not in blocks and name not in allows:
            allows.append(name)

    return {
        "blocks": blocks,
        "allows": allows,
        "raw_rules": list(set(raw_rules)),
    }


async def _check_resource(client: httpx.AsyncClient, url: str) -> dict:
    """Check if a resource exists (200) or not."""
    try:
        resp = await client.get(
            url,
            headers={"User-Agent": CRAWLERS["Browser"]},
            follow_redirects=True,
        )
        return {"exists": resp.status_code == 200, "status_code": resp.status_code}
    except (httpx.TimeoutException, httpx.RequestError):
        return {"exists": False, "status_code": None}


def _compute_score(crawlers: dict, robots_info: dict, llms_txt: dict, ucp: dict) -> int:
    """Compute visibility score out of 10."""
    score = 10

    # -3 per blocked AI crawler (exclude Browser control)
    ai_names = [n for n in crawlers if n != "Browser"]
    for name in ai_names:
        if crawlers[name].get("blocked"):
            score -= 3

    # -2 if robots.txt blocks any AI crawlers
    if robots_info.get("blocks_ai_crawlers"):
        score -= 2

    # -1 if no llms.txt
    if not llms_txt.get("exists"):
        score -= 1

    # -1 if no UCP
    if not ucp.get("exists"):
        score -= 1

    return max(score, 0)


def _build_recommendations(crawlers: dict, robots_info: dict, llms_txt: dict, ucp: dict) -> list[str]:
    """Generate actionable recommendations."""
    recs = []
    ai_names = [n for n in crawlers if n != "Browser"]

    for name in ai_names:
        info = crawlers[name]
        if info.get("blocked"):
            code = info.get("status_code")
            if code == 403:
                recs.append(f"Your server returns 403 to {name}. This is likely a WAF/CDN configuration issue.")
            elif code == 401:
                recs.append(f"Your server returns 401 to {name}. Authentication is blocking this crawler.")
            elif code == 503:
                recs.append(f"Your server returns 503 to {name}. The server may be rate-limiting or blocking this bot.")
            elif info.get("error") == "timeout":
                recs.append(f"{name} request timed out. The server may be blocking or throttling AI crawlers.")
            else:
                recs.append(f"{name} appears to be blocked (status: {code}).")

    if robots_info.get("blocks_ai_crawlers"):
        blocked = ", ".join(robots_info["blocks_ai_crawlers"])
        recs.append(f"robots.txt explicitly blocks: {blocked}. Review your robots.txt to allow AI discovery.")

    if not llms_txt.get("exists"):
        recs.append("No llms.txt found. Create one to help AI engines understand your brand.")

    if not ucp.get("exists"):
        recs.append("No UCP manifest found. This is needed for Google Shopping AI integration.")

    return recs


@router.get("/crawler-check")
async def crawler_check(url: str = Query(..., description="Website URL to check")):
    """
    'Are You Invisible?' — Check if a website blocks AI crawlers.
    """
    base_url = _normalise_url(url)

    async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:
        # Run all checks concurrently
        crawler_tasks = {
            name: _probe_crawler(client, base_url, name, ua)
            for name, ua in CRAWLERS.items()
        }
        robots_task = _check_resource(client, f"{base_url}/robots.txt")
        llms_task = _check_resource(client, f"{base_url}/llms.txt")
        ucp_task = _check_resource(client, f"{base_url}/.well-known/ucp")

        # Gather all
        all_tasks = list(crawler_tasks.values()) + [robots_task, llms_task, ucp_task]
        results = await asyncio.gather(*all_tasks, return_exceptions=True)

    # Unpack crawler results
    crawler_names = list(crawler_tasks.keys())
    crawlers = {}
    for i, name in enumerate(crawler_names):
        r = results[i]
        crawlers[name] = r if isinstance(r, dict) else {"status_code": None, "blocked": True, "error": str(r)[:120]}

    offset = len(crawler_names)
    robots_result = results[offset] if isinstance(results[offset], dict) else {"exists": False}
    llms_result = results[offset + 1] if isinstance(results[offset + 1], dict) else {"exists": False}
    ucp_result = results[offset + 2] if isinstance(results[offset + 2], dict) else {"exists": False}

    # Parse robots.txt if it exists
    ai_crawler_names = [n for n in CRAWLERS if n != "Browser"]
    robots_info = {"exists": robots_result["exists"], "blocks_ai_crawlers": [], "allows_ai_crawlers": ai_crawler_names, "raw_relevant_rules": []}

    if robots_result["exists"]:
        # Fetch robots.txt content for parsing
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT, verify=False) as client:
                resp = await client.get(
                    f"{base_url}/robots.txt",
                    headers={"User-Agent": CRAWLERS["Browser"]},
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    parsed = _parse_robots_txt(resp.text, ai_crawler_names)
                    robots_info["blocks_ai_crawlers"] = parsed["blocks"]
                    robots_info["allows_ai_crawlers"] = parsed["allows"]
                    robots_info["raw_relevant_rules"] = parsed["raw_rules"]
        except (httpx.TimeoutException, httpx.RequestError):
            pass

    llms_txt = {"exists": llms_result["exists"]}
    ucp = {"exists": ucp_result["exists"]}

    # Score and status
    score = _compute_score(crawlers, robots_info, llms_txt, ucp)
    if score >= 8:
        status = "visible"
    elif score >= 4:
        status = "partially_visible"
    else:
        status = "invisible"

    recommendations = _build_recommendations(crawlers, robots_info, llms_txt, ucp)

    # Strip scheme for display URL
    display_url = urlparse(base_url).netloc or url

    return {
        "url": display_url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_score": score,
        "overall_status": status,
        "crawlers": crawlers,
        "robots_txt": robots_info,
        "llms_txt": llms_txt,
        "ucp": ucp,
        "recommendations": recommendations,
    }
