"""
VisiMind — FastAPI Main Application
Serves the API, /.well-known/ucp at root level, and task polling endpoint.
"""
import json
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite

# Ensure server directory is in path
sys.path.insert(0, str(Path(__file__).parent))

from config import HOST, PORT, DEBUG, DB_PATH
from database import init_db, get_db
from data.seed import seed_database
from engines.remediation import build_ucp_manifest

# Import routers
from routers.dashboard import router as dashboard_router
from routers.connect import router as connect_router
from routers.diagnose import router as diagnose_router
from routers.remediate import router as remediate_router
from routers.verify import router as verify_router
from routers.ingest import router as ingest_router
from routers.eee import router as eee_router


# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB and seed data."""
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await seed_database(db)
    print(f"✓ VisiMind backend ready — http://{HOST}:{PORT}")
    print(f"  └─ API docs: http://{HOST}:{PORT}/docs")
    print(f"  └─ UCP manifest: http://{HOST}:{PORT}/.well-known/ucp")
    yield


# --- App ---
app = FastAPI(
    title="VisiMind — AI Remediation Layer",
    description="Backend API for the VisiMind Data Remediation Engine. Canadian Luxury Retail / Bilingual.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
app.include_router(dashboard_router)
app.include_router(connect_router)
app.include_router(diagnose_router)
app.include_router(remediate_router)
app.include_router(verify_router)
app.include_router(ingest_router)
app.include_router(eee_router)


# ============================================
# ROOT-LEVEL ROUTES (outside /api)
# ============================================

@app.get("/.well-known/ucp")
async def get_ucp_manifest():
    """
    Google Universal Commerce Protocol manifest.
    Must be served at the ROOT LEVEL of the domain per UCP spec.
    """
    return await build_ucp_manifest()


@app.get("/llms.txt")
async def get_llms_txt():
    """
    llms.txt — machine-readable file for LLM discovery.
    """
    return {
        "name": "VisiMind",
        "description": "AI Remediation Layer for Canadian Luxury Retail brands.",
        "feeds": [
            "https://visimind.ai/feeds/mackage/products.jsonld",
            "https://visimind.ai/feeds/ssense/products.jsonld",
            "https://visimind.ai/feeds/aldo/products.jsonld",
        ],
        "ucp_manifest": "https://visimind.ai/.well-known/ucp",
        "contact": "eng@visimind.ai",
    }


# --- Task Polling Endpoint ---
@app.get("/api/tasks/{task_id}")
async def get_task_status(task_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """
    Poll endpoint for async tasks (probes, audits, deployments).
    Frontend polls this to show "Iteration 12/50 complete".
    """
    cursor = await db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = await cursor.fetchone()

    if not task:
        return {"error": "Task not found", "id": task_id}

    result = None
    if task["result"]:
        try:
            result = json.loads(task["result"])
        except json.JSONDecodeError:
            result = task["result"]

    return {
        "id": task["id"],
        "type": task["type"],
        "status": task["status"],
        "progress": task["progress"],
        "total": task["total"],
        "result": result,
        "error": task["error"],
    }


# --- Health Check ---
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "VisiMind", "version": "1.0.0"}


# --- Run ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)
