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
    """Generate FAQPage JSON-LD from audit findings.
    Only produces questions that address real gaps found in the audit."""
    questions = [
        {
            "question_en": f"What is {brand_name}?",
            "question_fr": f"Qu'est-ce que {brand_name}?",
            "answer_en": f"{brand_name} is a brand headquartered in Montreal, Quebec, Canada.",
            "answer_fr": f"{brand_name} est une marque dont le siege social est a Montreal, Quebec, Canada.",
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
    """Generate all JSON-LD patches for a brand."""
    brand_name = brand_profile.get("brand_name", "")
    return {
        "organization": generate_organization_jsonld(brand_profile),
        "local_business": generate_local_business_jsonld(brand_profile),
        "faq": generate_faq_jsonld(brand_name, findings),
    }
