"""VisiMind -- System Router (capacity, waitlist, health)"""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DAILY_PROBE_LIMIT
from database import get_db

router = APIRouter(prefix="/api/v1/system", tags=["system"])

class WaitlistRequest(BaseModel):
    email: str

def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

async def get_daily_count(db: aiosqlite.Connection) -> int:
    today = _today()
    cursor = await db.execute("SELECT count FROM daily_probe_counter WHERE date = ?", (today,))
    row = await cursor.fetchone()
    return row["count"] if row else 0

async def increment_daily_count(db: aiosqlite.Connection) -> int:
    today = _today()
    cursor = await db.execute("SELECT count FROM daily_probe_counter WHERE date = ?", (today,))
    row = await cursor.fetchone()
    if row:
        new_count = row["count"] + 1
        await db.execute("UPDATE daily_probe_counter SET count = ? WHERE date = ?", (new_count, today))
    else:
        new_count = 1
        await db.execute("INSERT INTO daily_probe_counter (date, count) VALUES (?, ?)", (today, 1))
    await db.commit()
    return new_count

@router.get("/capacity")
async def get_capacity(db: aiosqlite.Connection = Depends(get_db)):
    used = await get_daily_count(db)
    return {
        "used": used,
        "limit": DAILY_PROBE_LIMIT,
        "slots_remaining": max(0, DAILY_PROBE_LIMIT - used),
    }

@router.post("/waitlist")
async def join_waitlist(req: WaitlistRequest, db: aiosqlite.Connection = Depends(get_db)):
    wl_id = str(uuid.uuid4())
    await db.execute(
        "INSERT INTO waitlist (id, email) VALUES (?, ?)",
        (wl_id, req.email.lower()),
    )
    await db.commit()
    return {"status": "ok", "message": "You've been added to the waitlist. We'll notify you when a slot opens."}
