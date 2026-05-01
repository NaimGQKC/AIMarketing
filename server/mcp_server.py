"""
VisiMind MCP Server
Exposes VisiMind audit data to Claude Desktop / Claude Code via Model Context Protocol.
"""

import json
import sqlite3
from pathlib import Path
from mcp.server.fastmcp import FastMCP

DB_PATH = str(Path(__file__).parent / "visimind.db")

mcp = FastMCP("visimind")


def _get_db() -> sqlite3.Connection:
    """Open a synchronous SQLite connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Tool 1: list_brands ──────────────────────────────────────────────

@mcp.tool()
def list_brands() -> list[dict]:
    """List all brands tracked in VisiMind.

    Returns each brand's ID, name, product category, and top competitor.
    Useful as a first step to see what data is available before querying audits.
    """
    db = _get_db()
    try:
        rows = db.execute(
            "SELECT id, brand_name, product_category, top_competitor FROM brand_profiles ORDER BY brand_name"
        ).fetchall()
        return [
            {
                "brand_id": r["id"],
                "brand_name": r["brand_name"],
                "product_category": r["product_category"],
                "top_competitor": r["top_competitor"],
            }
            for r in rows
        ]
    finally:
        db.close()


# ── Tool 2: get_latest_audit ─────────────────────────────────────────

@mcp.tool()
def get_latest_audit(brand_name: str) -> dict:
    """Get the latest audit results for a brand (looked up by name).

    Returns the IAS score, grade, breakdown by metric, key findings, and timestamp.
    The IAS (Inference Alignment Score) measures how well AI models represent the brand,
    scored 0-100 with RED (<40), YELLOW (40-70), GREEN (70+) grades.
    """
    db = _get_db()
    try:
        row = db.execute(
            """
            SELECT ar.ias_score, ar.ias_data, ar.status, ar.created_at
            FROM audit_results ar
            JOIN brand_profiles bp ON bp.id = ar.brand_profile_id
            WHERE bp.brand_name = ? COLLATE NOCASE
            ORDER BY ar.created_at DESC
            LIMIT 1
            """,
            (brand_name,),
        ).fetchone()

        if not row:
            return {"error": f"No audit found for brand '{brand_name}'. Run list_brands to see available brands."}

        ias_data = json.loads(row["ias_data"]) if row["ias_data"] else {}

        return {
            "ias_score": row["ias_score"],
            "grade": ias_data.get("grade"),
            "breakdown": ias_data.get("breakdown", {}),
            "findings": ias_data.get("findings", []),
            "probes_analyzed": ias_data.get("probes_analyzed"),
            "en_probes": ias_data.get("en_probes"),
            "fr_probes": ias_data.get("fr_probes"),
            "status": row["status"],
            "created_at": row["created_at"],
        }
    finally:
        db.close()


# ── Tool 3: get_audit_history ────────────────────────────────────────

@mcp.tool()
def get_audit_history(brand_name: str) -> list[dict]:
    """Get all audit scores over time for a brand.

    Returns a chronological list of IAS scores, useful for tracking
    whether AI alignment is improving or degrading after remediation efforts.
    """
    db = _get_db()
    try:
        rows = db.execute(
            """
            SELECT ar.ias_score, ar.created_at
            FROM audit_results ar
            JOIN brand_profiles bp ON bp.id = ar.brand_profile_id
            WHERE bp.brand_name = ? COLLATE NOCASE
            ORDER BY ar.created_at ASC
            """,
            (brand_name,),
        ).fetchall()

        if not rows:
            return [{"error": f"No audits found for brand '{brand_name}'."}]

        return [{"ias_score": r["ias_score"], "created_at": r["created_at"]} for r in rows]
    finally:
        db.close()


# ── Tool 4: get_probe_responses ──────────────────────────────────────

@mcp.tool()
def get_probe_responses(brand_name: str, lang: str | None = None) -> list[dict]:
    """Get the raw AI responses from the latest audit for a brand.

    Each probe result shows the actual text that Gemini/GPT returned when asked
    about the brand. Optionally filter by language ('EN' or 'FR') to compare
    how models treat the brand across languages.
    """
    db = _get_db()
    try:
        row = db.execute(
            """
            SELECT ar.results
            FROM audit_results ar
            JOIN brand_profiles bp ON bp.id = ar.brand_profile_id
            WHERE bp.brand_name = ? COLLATE NOCASE
            ORDER BY ar.created_at DESC
            LIMIT 1
            """,
            (brand_name,),
        ).fetchone()

        if not row or not row["results"]:
            return [{"error": f"No probe results found for brand '{brand_name}'."}]

        results = json.loads(row["results"])

        if lang:
            results = [r for r in results if r.get("lang", "").upper() == lang.upper()]

        # Return a focused subset of fields to keep responses manageable
        return [
            {
                "probe_type": r.get("probe_type"),
                "lang": r.get("lang"),
                "query": r.get("query"),
                "provider": r.get("provider"),
                "model": r.get("model"),
                "brand_mentioned": r.get("brand_mentioned"),
                "response_text": r.get("response_text", "")[:1000],  # truncate long responses
                "response_time_ms": r.get("response_time_ms"),
            }
            for r in results
        ]
    finally:
        db.close()


# ── Tool 5: get_recommendations ──────────────────────────────────────

@mcp.tool()
def get_recommendations(brand_name: str) -> dict:
    """Get prioritized fix recommendations based on the latest audit.

    Analyzes which IAS metrics scored lowest and returns actionable steps
    ordered by impact. Metrics checked: brand visibility in French search,
    EN/FR rank parity, spec preservation, competitor hijacking defense,
    and pricing accuracy.
    """
    db = _get_db()
    try:
        row = db.execute(
            """
            SELECT ar.ias_score, ar.ias_data
            FROM audit_results ar
            JOIN brand_profiles bp ON bp.id = ar.brand_profile_id
            WHERE bp.brand_name = ? COLLATE NOCASE
            ORDER BY ar.created_at DESC
            LIMIT 1
            """,
            (brand_name,),
        ).fetchone()

        if not row or not row["ias_data"]:
            return {"error": f"No audit data found for brand '{brand_name}'."}

        ias_data = json.loads(row["ias_data"])
        breakdown = ias_data.get("breakdown", {})
        findings = ias_data.get("findings", [])

        # Max possible points per metric
        max_scores = {
            "brand_in_fr_search": 30,
            "rank_parity": 20,
            "specs_preserved": 20,
            "no_hijacking": 15,
            "pricing_accurate": 15,
        }

        # Recommendations keyed by metric
        recommendation_text = {
            "brand_in_fr_search": (
                "Your brand is invisible in French generic AI searches. "
                "Create French-language structured data (JSON-LD) on your site, "
                "publish French product descriptions, and ensure your sitemap includes FR pages."
            ),
            "rank_parity": (
                "AI models rank your brand differently in English vs French. "
                "Strengthen French content parity: mirror EN product pages in FR with equal depth, "
                "and syndicate French-language content to authoritative directories."
            ),
            "specs_preserved": (
                "Technical specifications are diluted or missing in French AI responses. "
                "Ensure all product specs (materials, certifications, measurements) exist in both languages "
                "with identical detail level."
            ),
            "no_hijacking": (
                "Competitors are being recommended over your brand in French comparison queries. "
                "Create explicit comparison content, strengthen brand entity signals, "
                "and ensure your differentiators are clearly stated in structured data."
            ),
            "pricing_accurate": (
                "AI models lack substantive pricing/accuracy information about your brand. "
                "Publish structured pricing data, ensure product pages have rich schema markup, "
                "and keep external data sources (directories, retailers) up to date."
            ),
        }

        # Build prioritized list: biggest gap first
        recs = []
        for metric, max_val in max_scores.items():
            actual = breakdown.get(metric, 0)
            gap = max_val - actual
            if gap > 0:
                recs.append({
                    "priority": len(recs) + 1,
                    "metric": metric,
                    "current_score": actual,
                    "max_score": max_val,
                    "points_recoverable": gap,
                    "recommendation": recommendation_text[metric],
                })

        # Sort by points recoverable (biggest impact first)
        recs.sort(key=lambda r: r["points_recoverable"], reverse=True)
        for i, r in enumerate(recs):
            r["priority"] = i + 1

        return {
            "brand_name": brand_name,
            "current_ias": row["ias_score"],
            "grade": ias_data.get("grade"),
            "recommendations": recs,
            "findings_summary": [
                {"type": f.get("type"), "severity": f.get("severity"), "message": f.get("message")}
                for f in findings
            ],
        }
    finally:
        db.close()


# ── Tool 6: run_audit (placeholder) ─────────────────────────────────

@mcp.tool()
def run_audit(brand_name: str) -> dict:
    """Trigger a new audit for a brand.

    Note: Full audit execution requires the VisiMind web UI (authentication,
    rate limiting, and the async probe engine). Use this tool to check current
    audit data instead.
    """
    return {
        "status": "not_available",
        "message": (
            f"Audit execution for '{brand_name}' is not available via MCP. "
            "Please use the VisiMind web UI at http://localhost:5173 to run audits. "
            "The UI handles authentication, rate limiting, and the async probe engine. "
            "You can still query existing audit data using get_latest_audit, "
            "get_audit_history, or get_probe_responses."
        ),
    }


if __name__ == "__main__":
    mcp.run()
