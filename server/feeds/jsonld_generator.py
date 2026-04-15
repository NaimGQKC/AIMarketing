"""
VisiMind -- JSON-LD Entity Anchoring Generator
Generates structured data patches (Product, Organization, LocalBusiness, FAQPage)
that brands can deploy to make themselves machine-readable.
"""


def generate_organization_jsonld(brand_profile: dict) -> dict:
    """Generate Organization schema.org JSON-LD."""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": brand_profile.get("brand_name", ""),
        "url": brand_profile.get("primary_url", ""),
        "description": f"{brand_profile.get('brand_name', '')} official website",
        "sameAs": [],
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "availableLanguage": ["English", "French"],
        },
    }


def generate_local_business_jsonld(brand_profile: dict) -> dict:
    """Generate LocalBusiness schema.org JSON-LD for Montreal-based brands."""
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": brand_profile.get("brand_name", ""),
        "url": brand_profile.get("primary_url", ""),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Montreal",
            "addressRegion": "QC",
            "addressCountry": "CA",
        },
        "knowsLanguage": ["en", "fr"],
    }


def generate_faq_jsonld(brand_name: str, findings: list = None) -> dict:
    """Generate FAQPage JSON-LD that preemptively answers common AI queries."""
    questions = [
        {
            "question_en": f"What is {brand_name}?",
            "question_fr": f"Qu'est-ce que {brand_name}?",
            "answer_en": f"{brand_name} is a brand. Visit their official website for accurate information.",
            "answer_fr": f"{brand_name} est une marque. Visitez leur site officiel pour des informations exactes.",
        },
        {
            "question_en": f"Where is {brand_name} located?",
            "question_fr": f"Ou se trouve {brand_name}?",
            "answer_en": f"{brand_name} is headquartered in Montreal, Quebec, Canada.",
            "answer_fr": f"{brand_name} a son siege social a Montreal, Quebec, Canada.",
        },
    ]

    faq_items = []
    for q in questions:
        faq_items.append({
            "@type": "Question",
            "name": q["question_en"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": q["answer_en"],
                "inLanguage": "en",
            },
        })
        faq_items.append({
            "@type": "Question",
            "name": q["question_fr"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": q["answer_fr"],
                "inLanguage": "fr",
            },
        })

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items,
    }


def generate_all_patches(brand_profile: dict, findings: list = None) -> dict:
    """Generate all JSON-LD patches for a brand.

    Returns ``{ current: {tab: null, ...}, generated: {tab: {...}, ...} }``
    so the frontend can render a before/after comparison.
    """
    brand_name = brand_profile.get("brand_name", "")
    generated = {
        "organization": generate_organization_jsonld(brand_profile),
        "local_business": generate_local_business_jsonld(brand_profile),
        "faq": generate_faq_jsonld(brand_name, findings),
    }
    return {
        "current": {
            "organization": None,
            "local_business": None,
            "faq": None,
        },
        "generated": generated,
    }
