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

    # Add corrections from audit findings -- focus on gaps and misrepresentations
    if audit_results:
        try:
            if isinstance(audit_results, str):
                audit_results = json.loads(audit_results)
        except Exception:
            audit_results = []

        results_list = audit_results if isinstance(audit_results, list) else []

        # Group by probe_type+lang to find patterns
        from collections import defaultdict
        groups = defaultdict(list)
        for r in results_list:
            groups[(r.get("probe_type", ""), r.get("lang", ""))].append(r)

        for (probe_type, lang), probes in groups.items():
            total = len(probes)
            mentioned = sum(1 for p in probes if p.get("brand_mentioned"))
            mention_rate = mentioned / total if total else 0

            if mention_rate < 1.0:
                # Brand is missing in some responses -- this needs correction
                missing_sample = next(
                    (p["response_text"][:300] for p in probes if not p.get("brand_mentioned") and p.get("response_text")),
                    None,
                )
                feed["corrections"].append({
                    "type": "brand_omission",
                    "probe_type": probe_type.replace("_", " "),
                    "language": lang,
                    "mention_rate": f"{mention_rate:.0%}",
                    "total_probes": total,
                    "issue": f"{brand_name} was only mentioned in {mentioned}/{total} responses for '{probe_type.replace('_', ' ')}' queries ({lang})",
                    "sample_response_without_brand": missing_sample,
                    "recommended_action": f"Ensure {brand_name} is represented in {probe_type.replace('_', ' ')} contexts in {lang}",
                })

        # Add bilingual parity data
        en_probes = [r for r in results_list if r.get("lang") == "EN"]
        fr_probes = [r for r in results_list if r.get("lang") == "FR"]
        en_rate = sum(1 for p in en_probes if p.get("brand_mentioned")) / len(en_probes) if en_probes else 0
        fr_rate = sum(1 for p in fr_probes if p.get("brand_mentioned")) / len(fr_probes) if fr_probes else 0

        feed["bilingual_mappings"] = {
            "en_mention_rate": f"{en_rate:.0%}",
            "fr_mention_rate": f"{fr_rate:.0%}",
            "parity_gap": f"{abs(en_rate - fr_rate):.0%}",
            "weaker_language": "FR" if fr_rate < en_rate else "EN" if en_rate < fr_rate else "parity",
        }

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
