"""
VisiMind — Connect API Router
GET/POST /api/connect/integrations | feeds
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db

router = APIRouter(prefix="/api/connect", tags=["connect"])

ICONS = {"shopify": "ShoppingBag", "akeneo": "Database", "peec": "Eye", "otterly": "Search"}
DESCRIPTIONS = {
    "shopify": "E-commerce PIM for live product catalog sync",
    "akeneo": "Enterprise PIM for structured product data",
    "peec": "AI visibility monitoring & citation tracking",
    "otterly": "AI search presence & competitive intelligence",
}


@router.get("/integrations")
async def get_integrations(db: aiosqlite.Connection = Depends(get_db)):
    """All PIM and monitoring connections."""
    cursor = await db.execute("SELECT * FROM pim_connections ORDER BY type, name")
    rows = await cursor.fetchall()

    return [
        {
            "id": r["id"],
            "name": r["name"],
            "type": r["type"],
            "provider": r["provider"],
            "status": r["status"],
            "description": DESCRIPTIONS.get(r["provider"], ""),
            "last_sync": r["last_sync"],
            "items_synced": r["items_synced"],
            "queries_tracked": r["queries_tracked"],
            "errors": r["errors"],
            "icon": ICONS.get(r["provider"], "Database"),
        }
        for r in rows
    ]


@router.post("/integrations/{provider}/sync")
async def sync_integration(provider: str, db: aiosqlite.Connection = Depends(get_db)):
    """Trigger a PIM sync."""
    now = datetime.utcnow().isoformat()

    await db.execute(
        """UPDATE pim_connections
           SET status = 'connected', last_sync = ?, items_synced = items_synced + 15
           WHERE provider = ?""",
        (now, provider),
    )
    await db.commit()

    return {"status": "synced", "provider": provider, "synced_at": now}


@router.get("/feeds")
async def get_feeds(db: aiosqlite.Connection = Depends(get_db)):
    """Feed status table data."""
    # Build from brands + protocols
    cursor = await db.execute("SELECT name FROM brands")
    brands = await cursor.fetchall()

    feeds = []
    for b in brands:
        name = b["name"]
        for protocol in ["UCP", "ACP"]:
            cursor = await db.execute(
                "SELECT COUNT(*) as c FROM products WHERE brand_id = (SELECT id FROM brands WHERE name = ?)",
                (name,),
            )
            count = (await cursor.fetchone())["c"]
            feeds.append({
                "feed": f"{name} — {protocol}",
                "items": count * 85 + (50 if protocol == "UCP" else 43),
                "last_sync": "12 min ago" if protocol == "UCP" else "25 min ago",
                "status": "success" if count > 0 else "warning",
                "errors": 0 if protocol == "UCP" else count + 1,
            })

    return feeds
