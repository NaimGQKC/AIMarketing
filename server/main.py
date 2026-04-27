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
from engines.remediation import build_ucp_manifest, generate_youtube_deployment

# Import routers
from routers.dashboard import router as dashboard_router
from routers.connect import router as connect_router
from routers.diagnose import router as diagnose_router
from routers.remediate import router as remediate_router
from routers.verify import router as verify_router
from routers.ingest import router as ingest_router
from routers.eee import router as eee_router
from routers.crawler_check import router as crawler_check_router
from routers.crawler_stats import router as crawler_stats_router
from routers.auth import router as auth_router
from routers.brands_v1 import router as brands_v1_router
from routers.system import router as system_router
from routers.audits import router as audits_router
from routers.feeds import router as feeds_router
from routers.exports import router as exports_router
from routers.outreach import router as outreach_router
from middleware.ai_crawler import AICrawlerMiddleware


# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB and seed data."""
    await init_db()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await seed_database(db)
    print(f"[OK] VisiMind backend ready -- http://{HOST}:{PORT}")
    print(f"     API docs: http://{HOST}:{PORT}/docs")
    print(f"     UCP manifest: http://{HOST}:{PORT}/.well-known/ucp")
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
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AI Crawler Detection Middleware ---
app.add_middleware(AICrawlerMiddleware)

# --- Register Routers ---
app.include_router(dashboard_router)
app.include_router(connect_router)
app.include_router(diagnose_router)
app.include_router(remediate_router)
app.include_router(verify_router)
app.include_router(ingest_router)
app.include_router(eee_router)
app.include_router(crawler_check_router)
app.include_router(crawler_stats_router)
app.include_router(auth_router)
app.include_router(brands_v1_router)
app.include_router(system_router)
app.include_router(audits_router)
app.include_router(feeds_router)
app.include_router(exports_router)
app.include_router(outreach_router)


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


# --- YouTube Recommendations (convenience alias at /api/youtube-recommendations) ---
@app.get("/api/youtube-recommendations/{brand_id}")
async def youtube_recommendations_alias(brand_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """
    YouTube video deployment recommendations for all products of a brand.
    Convenience alias — canonical endpoint is /api/remediate/youtube-recommendations/{brand_id}.
    """
    cursor = await db.execute(
        "SELECT p.*, b.name as brand_name FROM products p JOIN brands b ON p.brand_id = b.id WHERE b.id = ?",
        (brand_id,),
    )
    products = await cursor.fetchall()

    if not products:
        return {"error": "No products found for brand", "brand_id": brand_id}

    recommendations = []
    for p in products:
        product = dict(p)
        product["brand_name"] = p["brand_name"]
        yt = generate_youtube_deployment(product)
        recommendations.append({
            "product_id": product["id"],
            "product_name_en": product["name_en"],
            "product_name_fr": product.get("name_fr", ""),
            "youtube_deployment": yt,
        })

    return {
        "brand_id": brand_id,
        "brand_name": products[0]["brand_name"],
        "total_recommendations": len(recommendations),
        "rationale": (
            "YouTube mentions correlate at 0.737 with AI brand visibility "
            "(Ahrefs, 75K brand study). French YouTube content for this brand "
            "is near-zero, creating a bilingual visibility gap."
        ),
        "recommendations": recommendations,
    }


# --- Health Check ---
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "VisiMind", "version": "1.0.0"}


# --- Serve frontend static files in production ---
from pathlib import Path as _Path
_dist_dir = _Path(__file__).parent.parent / "dist"
if _dist_dir.exists():
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = _dist_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(_dist_dir / "index.html")


# --- Run ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=DEBUG)
