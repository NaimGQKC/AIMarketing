"""
VisiMind — Crawler Statistics Router
Exposes AI-crawler visit analytics.
"""
from fastapi import APIRouter, Depends
import aiosqlite

from database import get_db

router = APIRouter(prefix="/api/crawler-stats", tags=["crawler-stats"])


@router.get("")
async def get_crawler_stats(db: aiosqlite.Connection = Depends(get_db)):
    """Return aggregate crawler visit statistics."""

    # Total visits per crawler
    cursor = await db.execute(
        """SELECT crawler_name,
                  COUNT(*) AS total_visits,
                  ROUND(AVG(response_time_ms), 2) AS avg_response_ms,
                  MIN(timestamp) AS first_seen,
                  MAX(timestamp) AS last_seen
           FROM crawler_visits
           GROUP BY crawler_name
           ORDER BY total_visits DESC"""
    )
    by_crawler = [dict(row) for row in await cursor.fetchall()]

    # Top 20 most-visited paths
    cursor = await db.execute(
        """SELECT path, COUNT(*) AS visits
           FROM crawler_visits
           GROUP BY path
           ORDER BY visits DESC
           LIMIT 20"""
    )
    top_paths = [dict(row) for row in await cursor.fetchall()]

    # Daily visit counts (last 30 days)
    cursor = await db.execute(
        """SELECT DATE(timestamp) AS day, COUNT(*) AS visits
           FROM crawler_visits
           GROUP BY day
           ORDER BY day DESC
           LIMIT 30"""
    )
    daily = [dict(row) for row in await cursor.fetchall()]

    # Total count
    cursor = await db.execute("SELECT COUNT(*) AS total FROM crawler_visits")
    total = (await cursor.fetchone())["total"]

    return {
        "total_visits": total,
        "by_crawler": by_crawler,
        "top_paths": top_paths,
        "daily": daily,
    }


@router.get("/{brand_id}")
async def get_brand_crawler_stats(
    brand_id: str, db: aiosqlite.Connection = Depends(get_db)
):
    """Return crawler visit statistics for a specific brand."""

    cursor = await db.execute(
        """SELECT crawler_name,
                  COUNT(*) AS total_visits,
                  ROUND(AVG(response_time_ms), 2) AS avg_response_ms,
                  MIN(timestamp) AS first_seen,
                  MAX(timestamp) AS last_seen
           FROM crawler_visits
           WHERE brand_id = ?
           GROUP BY crawler_name
           ORDER BY total_visits DESC""",
        (brand_id,),
    )
    by_crawler = [dict(row) for row in await cursor.fetchall()]

    cursor = await db.execute(
        """SELECT path, COUNT(*) AS visits
           FROM crawler_visits
           WHERE brand_id = ?
           GROUP BY path
           ORDER BY visits DESC
           LIMIT 20""",
        (brand_id,),
    )
    top_paths = [dict(row) for row in await cursor.fetchall()]

    cursor = await db.execute(
        "SELECT COUNT(*) AS total FROM crawler_visits WHERE brand_id = ?",
        (brand_id,),
    )
    total = (await cursor.fetchone())["total"]

    return {
        "brand_id": brand_id,
        "total_visits": total,
        "by_crawler": by_crawler,
        "top_paths": top_paths,
    }
