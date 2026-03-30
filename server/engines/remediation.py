"""
VisiMind — Engine 3: Remediation Factory
Fix kit generation, JSON-LD builder, UCP manifest, ACP feed formatting, Truth Clip metadata.
"""
import json
import uuid
from datetime import datetime

from engines.bilingual_bridge import inject_bilingual_context, generate_bilingual_mapping


# --- Fix Kit Generation ---

def generate_fix_kit(gap: dict, product: dict) -> dict:
    """
    Generate the appropriate fix kit based on the gap type.
    """
    gap_type = gap.get("gap_type", "")

    if gap_type == "Token Decay":
        return _build_bilingual_fix(gap, product)
    elif gap_type == "Fact Density":
        return _build_jsonld_fix(gap, product)
    elif gap_type == "Entity Trust":
        return _build_truth_clip_fix(gap, product)
    else:
        return _build_jsonld_fix(gap, product)


def _build_bilingual_fix(gap: dict, product: dict) -> dict:
    mapping = generate_bilingual_mapping(product)
    jsonld = inject_bilingual_context(product, mapping)

    return {
        "id": str(uuid.uuid4()),
        "type": "jsonLd",
        "subtype": "bilingual_context_injection",
        "brand": product.get("brand_name", ""),
        "product": product.get("name_en", ""),
        "status": "ready",
        "payload": {
            "jsonld": jsonld,
            "bilingual_mapping": mapping,
            "target_protocols": ["UCP", "ACP"],
        },
        "impact": f"Expected +{_estimate_impact('Token Decay')}% reasoning parity for French queries",
    }


def _build_jsonld_fix(gap: dict, product: dict) -> dict:
    jsonld = inject_bilingual_context(product)

    return {
        "id": str(uuid.uuid4()),
        "type": "jsonLd",
        "subtype": "high_density_attributes",
        "brand": product.get("brand_name", ""),
        "product": product.get("name_en", ""),
        "status": "ready",
        "payload": {
            "jsonld": jsonld,
            "target_protocols": ["UCP", "ACP"],
        },
        "impact": f"Expected +{_estimate_impact('Fact Density')}% fact density score",
    }


def _build_truth_clip_fix(gap: dict, product: dict) -> dict:
    certs = product.get("certifications", "[]")
    if isinstance(certs, str):
        try:
            certs = json.loads(certs)
        except json.JSONDecodeError:
            certs = []

    return {
        "id": str(uuid.uuid4()),
        "type": "truthClip",
        "subtype": "multimodal_verification",
        "brand": product.get("brand_name", ""),
        "product": product.get("name_en", ""),
        "status": "ready",
        "payload": {
            "clip_metadata": generate_truth_clip_metadata(product),
            "certifications_to_prove": certs,
            "target_protocols": ["UCP"],
        },
        "impact": f"Expected +{_estimate_impact('Entity Trust')}% entity trust for verification queries",
    }


def _estimate_impact(gap_type: str) -> int:
    """Heuristic impact estimation based on gap type."""
    return {"Token Decay": 35, "Fact Density": 25, "Entity Trust": 45}.get(gap_type, 30)


# --- JSON-LD Builder ---

def build_product_jsonld(product: dict) -> dict:
    """Build high-density Schema.org Product JSON-LD."""
    return inject_bilingual_context(product)


# --- Truth Clip Metadata ---

def generate_truth_clip_metadata(product: dict) -> dict:
    """
    Generate VideoObject schema metadata for a 15s technical proof clip.
    Designed for Gemini's multimodal fact-extraction engine.
    """
    certs = product.get("certifications", "[]")
    if isinstance(certs, str):
        try:
            certs = json.loads(certs)
        except json.JSONDecodeError:
            certs = []

    cert_text = ", ".join(certs) if certs else "product verification"

    return {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": f"Truth Clip: {product.get('name_en', '')} — {cert_text}",
        "description": (
            f"15-second technical proof video demonstrating verified attributes for "
            f"{product.get('name_en', '')} by {product.get('brand_name', '')}. "
            f"Shows {cert_text} certification proof."
        ),
        "duration": "PT15S",
        "uploadDate": datetime.utcnow().isoformat(),
        "contentUrl": f"https://visimind.ai/truth-clips/{product.get('id', 'unknown')}.mp4",
        "thumbnailUrl": f"https://visimind.ai/truth-clips/{product.get('id', 'unknown')}-thumb.jpg",
        "encodingFormat": "video/mp4",
        "publisher": {
            "@type": "Organization",
            "name": "VisiMind",
            "url": "https://visimind.ai",
        },
        "hasPart": [
            {
                "@type": "Clip",
                "name": "Certification Close-Up",
                "startOffset": 0,
                "endOffset": 5,
                "description": f"Close-up of {cert_text} certification badge",
            },
            {
                "@type": "Clip",
                "name": "Material Verification",
                "startOffset": 5,
                "endOffset": 10,
                "description": f"Material detail: {product.get('material', 'premium materials')}",
            },
            {
                "@type": "Clip",
                "name": "Technical Specs",
                "startOffset": 10,
                "endOffset": 15,
                "description": f"Specs overlay: {product.get('thermal_rating', '')} {product.get('fill_power', '')}",
            },
        ],
        # C2PA Content Credentials placeholder
        "creditText": "Verified by VisiMind AI Remediation Layer. Non-synthetic media.",
    }


# --- UCP Manifest ---

async def build_ucp_manifest(brand: dict = None) -> dict:
    """
    Build the /.well-known/ucp manifest for Google Universal Commerce Protocol.
    This must be served at the root domain level.
    """
    return {
        "schema_version": "1.0",
        "organization": {
            "name": "VisiMind",
            "url": "https://visimind.ai",
            "description": "AI Remediation Layer for Canadian Luxury Retail",
            "contact_email": "ucp@visimind.ai",
        },
        "data_feeds": [
            {
                "feed_id": "mackage-products-fw2026",
                "brand": "Mackage",
                "type": "product_catalog",
                "format": "application/ld+json",
                "url": "https://visimind.ai/feeds/mackage/products.jsonld",
                "update_frequency": "PT15M",
                "item_count": 342,
            },
            {
                "feed_id": "ssense-products-ss2026",
                "brand": "SSENSE",
                "type": "product_catalog",
                "format": "application/ld+json",
                "url": "https://visimind.ai/feeds/ssense/products.jsonld",
                "update_frequency": "PT10M",
                "item_count": 1205,
            },
            {
                "feed_id": "aldo-products-fw2026",
                "brand": "Aldo",
                "type": "product_catalog",
                "format": "application/ld+json",
                "url": "https://visimind.ai/feeds/aldo/products.jsonld",
                "update_frequency": "PT10M",
                "item_count": 891,
            },
        ],
        "capabilities": [
            "product_catalog",
            "real_time_inventory",
            "bilingual_content",
            "truth_clips",
            "structured_specs",
        ],
        "llms_txt": "https://visimind.ai/llms.txt",
        "contact": {
            "technical": "eng@visimind.ai",
            "business": "partnerships@visimind.ai",
        },
    }


# --- ACP Feed Formatting ---

def format_acp_feed(products: list[dict]) -> dict:
    """Format product data for OpenAI ACP (Agentic Commerce Protocol) discovery feed."""
    items = []
    for p in products:
        items.append({
            "id": p.get("id", ""),
            "title": p.get("name_en", ""),
            "title_fr": p.get("name_fr", ""),
            "brand": p.get("brand_name", ""),
            "category": p.get("category", ""),
            "price": {"amount": p.get("price_cad", 0), "currency": "CAD"},
            "description": p.get("description_en", ""),
            "description_fr": p.get("description_fr", ""),
            "attributes": {
                "thermal_rating": p.get("thermal_rating"),
                "fill_power": p.get("fill_power"),
                "material": p.get("material"),
                "certifications": json.loads(p.get("certifications", "[]")) if isinstance(p.get("certifications"), str) else p.get("certifications", []),
            },
            "availability": "in_stock",
            "shipping": {"same_day": True, "regions": ["CA", "US"]},
        })

    return {
        "protocol": "acp",
        "version": "1.0",
        "publisher": "VisiMind",
        "updated_at": datetime.utcnow().isoformat(),
        "items": items,
    }
