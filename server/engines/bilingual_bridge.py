"""
VisiMind — Engine 2: Bilingual Bridge (The Montreal Moat)
Token fertility analysis using tiktoken for real tokenization.
Bilingual JSON-LD context injection.
"""
import json
import tiktoken


# --- Tokenizer ---
# Use cl100k_base (GPT-4/ChatGPT tokenizer) as representative
_encoder = None


def _get_encoder():
    global _encoder
    if _encoder is None:
        _encoder = tiktoken.get_encoding("cl100k_base")
    return _encoder


# --- Token Fertility Analysis ---

def calculate_fertility(text: str, lang: str = "en") -> dict:
    """
    Calculate the Token Fertility Score: Tokens / Words.
    A fertility > 1.5 indicates the tokenizer is "Scrabble-tiling" the text.

    Returns detailed breakdown for CMO-level proof.
    """
    enc = _get_encoder()

    words = text.split()
    tokens = enc.encode(text)
    token_strings = [enc.decode([t]) for t in tokens]

    word_count = len(words)
    token_count = len(tokens)
    fertility = round(token_count / word_count, 2) if word_count > 0 else 0

    # Per-word token analysis (find the "Scrabble-tiled" words)
    fragmented_words = []
    for word in words:
        word_tokens = enc.encode(word)
        if len(word_tokens) > 2:  # More than 2 tokens = fragmented
            fragmented_words.append({
                "word": word,
                "tokens": [enc.decode([t]) for t in word_tokens],
                "token_count": len(word_tokens),
            })

    return {
        "text": text[:200],  # Preview
        "lang": lang,
        "word_count": word_count,
        "token_count": token_count,
        "fertility": fertility,
        "is_fragmented": fertility > 1.5,
        "fragmented_words": sorted(fragmented_words, key=lambda x: x["token_count"], reverse=True)[:10],
        "severity": _fertility_severity(fertility),
    }


def _fertility_severity(fertility: float) -> str:
    if fertility <= 1.2:
        return "healthy"
    elif fertility <= 1.5:
        return "warning"
    elif fertility <= 2.0:
        return "degraded"
    else:
        return "critical"


def compare_fertility(text_en: str, text_fr: str) -> dict:
    """
    Compare token fertility between EN and FR versions of the same content.
    This is the core "Montreal Wedge" metric.
    """
    en_result = calculate_fertility(text_en, "en")
    fr_result = calculate_fertility(text_fr, "fr")

    # The "Tokenization Premium" — how many extra tokens French costs
    token_tax = fr_result["token_count"] - en_result["token_count"]
    tax_percentage = round(
        (token_tax / en_result["token_count"]) * 100, 1
    ) if en_result["token_count"] > 0 else 0

    return {
        "en": en_result,
        "fr": fr_result,
        "token_tax": token_tax,
        "tax_percentage": tax_percentage,
        "parity_gap": round(en_result["fertility"] - fr_result["fertility"], 2),
        "recommendation": _get_recommendation(fr_result["fertility"], tax_percentage),
    }


def _get_recommendation(fr_fertility: float, tax_pct: float) -> str:
    if fr_fertility > 2.0:
        return "CRITICAL: French content is heavily fragmented. Immediate context injection required."
    elif fr_fertility > 1.5:
        return f"WARNING: French tokenization is {tax_pct}% heavier. Bilingual mapping recommended."
    else:
        return "Healthy: French token fertility is within acceptable range."


# --- Bilingual Mapping ---

# Common technical terms in Canadian luxury retail
DEFAULT_BILINGUAL_MAP = {
    # Outerwear
    "800-fill power": "Facteur de gonflement 800",
    "goose down": "duvet d'oie",
    "seam-sealed": "coutures scellées",
    "thermal rating": "indice thermique",
    "wind-resistant": "résistant au vent",
    "water-repellent": "hydrofuge",
    "breathable": "respirant",
    # Leather
    "full-grain leather": "cuir pleine fleur",
    "lambskin": "peau d'agneau",
    "nappa leather": "cuir nappa",
    "vegetable-tanned": "tannage végétal",
    # Sustainability
    "carbon-neutral": "carboneutre",
    "recycled materials": "matériaux recyclés",
    "ethically sourced": "approvisionnement éthique",
    "LWG certified": "certifié LWG",
    "RDS certified": "certifié RDS",
    # Commerce
    "same-day delivery": "livraison le jour même",
    "free returns": "retours gratuits",
    "price match": "alignement des prix",
    "in-stock": "en stock",
    "limited edition": "édition limitée",
}


def generate_bilingual_mapping(product: dict) -> dict:
    """
    Generate EN↔FR high-density term mappings for a product.
    Combines default mappings with product-specific terms.
    """
    mapping = dict(DEFAULT_BILINGUAL_MAP)

    # Add product-specific terms from attributes
    if product.get("bilingual_mapping"):
        if isinstance(product["bilingual_mapping"], str):
            try:
                extra = json.loads(product["bilingual_mapping"])
                mapping.update(extra)
            except json.JSONDecodeError:
                pass
        elif isinstance(product["bilingual_mapping"], dict):
            mapping.update(product["bilingual_mapping"])

    return mapping


# --- Context Injection (JSON-LD) ---

def inject_bilingual_context(product: dict, mapping: dict = None) -> dict:
    """
    Generate bilingual JSON-LD that improves entity recognition and
    fact density for AI extraction in Quebec-market queries.
    """
    if mapping is None:
        mapping = generate_bilingual_mapping(product)

    # Build bilingual description
    desc_en = product.get("description_en", "")
    desc_fr = product.get("description_fr", "")

    # Enrich French description with mapped terms
    enriched_fr = desc_fr
    for en_term, fr_term in mapping.items():
        if en_term.lower() in desc_en.lower() and fr_term not in enriched_fr:
            enriched_fr += f" | {fr_term}"

    # Parse certifications
    certs = product.get("certifications", "[]")
    if isinstance(certs, str):
        try:
            certs = json.loads(certs)
        except json.JSONDecodeError:
            certs = []

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.get("name_en", ""),
        "alternateName": product.get("name_fr", ""),
        "description": desc_en,
        "inLanguage": ["en", "fr"],
        "brand": {
            "@type": "Brand",
            "name": product.get("brand_name", ""),
        },
        "offers": {
            "@type": "Offer",
            "price": str(product.get("price_cad", "")),
            "priceCurrency": "CAD",
            "availability": "https://schema.org/InStock",
        },
        "additionalProperty": [],
    }

    # Add hard attributes
    if product.get("thermal_rating"):
        jsonld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "thermalRating",
            "value": product["thermal_rating"],
            "alternateName": mapping.get("thermal rating", "indice thermique"),
        })

    if product.get("fill_power"):
        jsonld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "fillPower",
            "value": product["fill_power"],
            "alternateName": mapping.get("800-fill power", "Facteur de gonflement"),
        })

    if product.get("material"):
        jsonld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "material",
            "value": product["material"],
        })

    # Add certifications
    for cert in certs:
        jsonld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "certification",
            "value": cert,
        })

    # Bilingual annotations for agentic indexing
    jsonld["workTranslation"] = {
        "@type": "Product",
        "inLanguage": "fr",
        "name": product.get("name_fr", ""),
        "description": enriched_fr,
    }

    return jsonld
