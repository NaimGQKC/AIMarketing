"""
VisiMind -- MCP Feed Generator
Generates Model Context Protocol feeds that AI agents can consume to correct brand representations.
"""
import json
from datetime import datetime, timezone


def generate_mcp_feed(brand_profile: dict, audit_results: list = None) -> dict:
    """
    Generate an MCP-compliant structured feed for a brand.
    This feed can be served at a public URL for AI agents to consume.
    """
    now = datetime.now(timezone.utc).isoformat()
    brand_name = brand_profile.get("brand_name", "Unknown")

    feed = {
        "@context": "https://modelcontextprotocol.io/schema/v1",
        "@type": "BrandContextFeed",
        "version": "1.0",
        "generated_at": now,
        "brand": {
            "name": brand_name,
            "url": brand_profile.get("primary_url", ""),
            "category": brand_profile.get("product_category", ""),
            "language_pair": brand_profile.get("language_pair", "EN/FR"),
        },
        "corrections": [],
        "structured_data": {
            "organization": {
                "@type": "Organization",
                "name": brand_name,
                "url": brand_profile.get("primary_url", ""),
                "description": f"{brand_name} - Official brand information",
                "description_fr": f"{brand_name} - Informations officielles de la marque",
            }
        },
        "bilingual_mappings": {},
        "metadata": {
            "generator": "VisiMind v2.0",
            "protocol": "Model Context Protocol (MCP)",
            "refresh_interval": "weekly",
        }
    }

    # Add corrections from audit findings if available
    if audit_results:
        ias_data = None
        try:
            if isinstance(audit_results, str):
                audit_results = json.loads(audit_results)
        except:
            pass

        for result in (audit_results if isinstance(audit_results, list) else []):
            if result.get("brand_mentioned") and result.get("response_text"):
                feed["corrections"].append({
                    "probe_type": result.get("probe_type", ""),
                    "language": result.get("lang", ""),
                    "provider": result.get("provider", ""),
                    "observed_response": result.get("response_text", "")[:300],
                    "correction_needed": not result.get("brand_mentioned", False),
                })

    return feed


def validate_mcp_feed(feed: dict) -> dict:
    """Validate that a feed has all required MCP fields."""
    required_fields = ["@context", "@type", "version", "brand"]
    missing = [f for f in required_fields if f not in feed]
    brand_fields = ["name"]
    if "brand" in feed:
        missing_brand = [f for f in brand_fields if f not in feed["brand"]]
    else:
        missing_brand = brand_fields

    return {
        "valid": len(missing) == 0 and len(missing_brand) == 0,
        "missing_root": missing,
        "missing_brand": missing_brand,
    }
