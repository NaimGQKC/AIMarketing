"""
VisiMind -- Feeds Router
MCP feed serving, JSON-LD generation, robots.txt analysis.
"""
import json
import logging
import re
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import aiosqlite
import httpx

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from routers.auth import require_user
from feeds.mcp_generator import generate_mcp_feed, validate_mcp_feed
from feeds.jsonld_generator import generate_all_patches

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/feeds", tags=["feeds"])

AI_BOT_PATTERNS = [
    ("GPTBot", r"GPTBot"),
    ("Google-Extended", r"Google-Extended"),
    ("Anthropic-AI", r"anthropic-ai|ClaudeBot"),
    ("CCBot", r"CCBot"),
    ("Bytespider", r"Bytespider"),
    ("Amazonbot", r"Amazonbot"),
]


@router.get("/{brand_id}/mcp.json")
async def get_mcp_feed(brand_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """
    Serve the MCP feed for a brand. This is a PUBLIC endpoint --
    AI agents need to access it without authentication.

    Security: Only select the columns we need for feed generation.
    Never expose user_id, logo_url, or internal metadata.
    """
    # Only select public-safe columns -- never SELECT *
    cursor = await db.execute(
        "SELECT id, brand_name, primary_url, product_category, language_pair "
        "FROM brand_profiles WHERE id = ?",
        (brand_id,),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Get latest audit results if available
    audit_results = None
    try:
        cursor = await db.execute(
            "SELECT results FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
            (brand_id,),
        )
        audit = await cursor.fetchone()
        if audit and audit["results"]:
            audit_results = json.loads(audit["results"])
    except Exception as exc:
        logger.warning("Failed to load audit results for brand %s: %s", brand_id, exc)

    feed = generate_mcp_feed(dict(brand), audit_results)
    return JSONResponse(
        content=feed,
        media_type="application/json",
        headers={
            "Cache-Control": "public, max-age=3600, s-maxage=86400",
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.get("/{brand_id}/mcp/preview")
async def preview_mcp_feed(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Preview the MCP feed (authenticated, for dashboard display)."""
    cursor = await db.execute(
        "SELECT id, brand_name, primary_url, product_category, language_pair "
        "FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    audit_results = None
    try:
        cursor = await db.execute(
            "SELECT results FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
            (brand_id,),
        )
        audit = await cursor.fetchone()
        if audit and audit["results"]:
            audit_results = json.loads(audit["results"])
    except Exception as exc:
        logger.warning("Failed to load audit results for preview (brand %s): %s", brand_id, exc)

    feed = generate_mcp_feed(dict(brand), audit_results)
    validation = validate_mcp_feed(feed)

    return {
        "feed": feed,
        "validation": validation,
        "feed_url": f"/api/v1/feeds/{brand_id}/mcp.json",
    }


@router.post("/{brand_id}/mcp/deploy")
async def deploy_mcp_feed(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Mark the MCP feed as deployed / active for a brand."""
    cursor = await db.execute(
        "SELECT id, brand_name, primary_url FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    feed_url = f"/api/v1/feeds/{brand_id}/mcp.json"

    # Validate the feed is actually ready
    feed = generate_mcp_feed(dict(brand))
    validation = validate_mcp_feed(feed)
    if not validation["valid"]:
        raise HTTPException(
            status_code=422,
            detail=f"Feed validation failed. Missing fields: {validation['missing_root'] + validation['missing_brand']}",
        )

    return {
        "status": "deployed",
        "feed_url": feed_url,
        "brand_name": brand["brand_name"],
        "validation": validation,
        "message": f"MCP feed is live at {feed_url}. AI agents can now access your brand truth data.",
        "next_steps": [
            f"Add this URL to your llms.txt file: {feed_url}",
            "Link the feed from your website's <head> section for discoverability.",
            "Run an audit in 7 days to verify AI models have updated their knowledge.",
        ],
    }


@router.get("/{brand_id}/jsonld")
async def get_jsonld_patches(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Generate JSON-LD structured data patches for a brand."""
    cursor = await db.execute(
        "SELECT id, brand_name, primary_url, product_category, language_pair "
        "FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Get findings from latest audit
    findings = None
    try:
        cursor = await db.execute(
            "SELECT ias_data FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
            (brand_id,),
        )
        audit = await cursor.fetchone()
        if audit and audit["ias_data"]:
            ias = json.loads(audit["ias_data"])
            findings = ias.get("findings", [])
    except Exception as exc:
        logger.warning("Failed to load IAS data for JSON-LD (brand %s): %s", brand_id, exc)

    patches = generate_all_patches(dict(brand), findings)
    return patches


class RobotsTxtRequest(BaseModel):
    url: str


@router.post("/{brand_id}/robots-check")
async def check_robots_txt(brand_id: str, req: RobotsTxtRequest, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """
    Fetch a brand's robots.txt and check if AI bots are blocked.
    """
    cursor = await db.execute(
        "SELECT id FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")

    url = req.url.rstrip("/")
    robots_url = f"{url}/robots.txt"

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(robots_url)
            if resp.status_code != 200:
                return {
                    "url": robots_url,
                    "status": "not_found",
                    "message": f"robots.txt returned HTTP {resp.status_code}",
                    "blocked_bots": [],
                    "allowed_bots": [],
                    "recommendation": "No robots.txt found. AI bots can access your site by default.",
                }

            content = resp.text
    except Exception as e:
        return {
            "url": robots_url,
            "status": "error",
            "message": f"Could not fetch robots.txt: {str(e)}",
            "blocked_bots": [],
            "allowed_bots": [],
        }

    # Parse for AI bot blocks
    blocked = []
    allowed = []

    for bot_name, pattern in AI_BOT_PATTERNS:
        # Check if there's a Disallow for this bot
        bot_section = re.search(
            rf"User-agent:\s*{pattern}.*?(?=User-agent:|$)",
            content,
            re.IGNORECASE | re.DOTALL,
        )
        if bot_section:
            section_text = bot_section.group()
            if re.search(r"Disallow:\s*/", section_text):
                blocked.append(bot_name)
            else:
                allowed.append(bot_name)
        else:
            # Check global disallow
            global_section = re.search(
                r"User-agent:\s*\*.*?(?=User-agent:|$)",
                content,
                re.IGNORECASE | re.DOTALL,
            )
            if global_section and re.search(r"Disallow:\s*/\s*$", global_section.group(), re.MULTILINE):
                blocked.append(bot_name)
            else:
                allowed.append(bot_name)

    # Generate recommendation
    if blocked:
        recommendation = (
            f"Your robots.txt blocks {len(blocked)} AI bot(s): {', '.join(blocked)}. "
            "This means these AI agents cannot crawl your site to update their knowledge. "
            "Consider allowing them to improve your brand's AI visibility."
        )
        recommended_robots = _generate_recommended_robots(url, blocked)
    else:
        recommendation = "Your robots.txt allows all major AI bots. Good."
        recommended_robots = None

    return {
        "url": robots_url,
        "status": "analyzed",
        "raw_content": content[:2000],
        "blocked_bots": blocked,
        "allowed_bots": allowed,
        "recommendation": recommendation,
        "recommended_robots_txt": recommended_robots,
    }


def _generate_recommended_robots(url: str, blocked_bots: list) -> str:
    """Generate a recommended robots.txt that unblocks AI bots."""
    lines = [
        "# Recommended robots.txt for AI visibility",
        "# Generated by VisiMind",
        "",
        "User-agent: *",
        "Allow: /",
        "",
    ]
    for bot_name, _ in AI_BOT_PATTERNS:
        lines.extend([
            f"User-agent: {bot_name}",
            "Allow: /",
            "",
        ])
    lines.extend([
        f"Sitemap: {url}/sitemap.xml",
    ])
    return "\n".join(lines)
