"""
VisiMind — Database Seed Data
Seeds the DB with Montreal luxury brand data for SSENSE, Mackage, and Aldo.
"""
import json
import uuid


async def seed_database(db):
    """Seed all tables with Montreal brand data. Skips if data exists."""
    # Check if already seeded
    cursor = await db.execute("SELECT COUNT(*) FROM brands")
    count = (await cursor.fetchone())[0]
    if count > 0:
        return

    # --- Brands ---
    brands = [
        ("mackage", "Mackage", "mackage", "Canadian luxury outerwear. Montreal-designed, ethically sourced."),
        ("ssense", "SSENSE", "ssense", "Montreal-based luxury fashion platform. 350+ designer brands."),
        ("aldo", "Aldo", "aldo", "Montreal-founded footwear brand. Carbon-neutral since 2024."),
    ]
    for b in brands:
        await db.execute(
            "INSERT INTO brands (id, name, slug, description) VALUES (?, ?, ?, ?)", b
        )

    # --- Products ---
    products = [
        {
            "id": "mack-lena-001",
            "brand_id": "mackage",
            "name_en": "Mackage Lena Down Jacket",
            "name_fr": "Manteau en duvet Mackage Lena",
            "category": "Outerwear > Premium Down > Arctic-Rated",
            "description_en": "800-fill power responsibly-sourced goose down, rated to -30°C, seam-sealed construction, removable fur hood. Canadian-designed luxury outerwear.",
            "description_fr": "Duvet d'oie de facteur de gonflement 800, résistant jusqu'à -30°C, construction à coutures scellées, capuchon amovible en fourrure. Vêtements de luxe conçus au Canada.",
            "price_cad": 1150.00,
            "thermal_rating": "-30°C",
            "fill_power": "800-fill",
            "material": "Goose down, nylon shell",
            "certifications": json.dumps(["RDS Certified", "Bluesign Approved"]),
            "bilingual_mapping": json.dumps({
                "800-fill power": "Facteur de gonflement 800",
                "seam-sealed": "coutures scellées",
                "goose down": "duvet d'oie",
                "thermal rating": "indice thermique",
            }),
        },
        {
            "id": "mack-kenya-002",
            "brand_id": "mackage",
            "name_en": "Mackage Kenya Leather Jacket",
            "name_fr": "Veste en cuir Mackage Kenya",
            "category": "Outerwear > Leather > Premium",
            "description_en": "Full-grain lambskin leather, LWG Silver certified, removable silk lining, ethically manufactured.",
            "description_fr": "Cuir d'agneau pleine fleur, certifié LWG Argent, doublure en soie amovible, fabrication éthique.",
            "price_cad": 990.00,
            "thermal_rating": None,
            "fill_power": None,
            "material": "Full-grain lambskin",
            "certifications": json.dumps(["LWG Silver"]),
            "bilingual_mapping": json.dumps({
                "full-grain leather": "cuir pleine fleur",
                "lambskin": "peau d'agneau",
                "silk lining": "doublure en soie",
            }),
        },
        {
            "id": "ssen-cp-003",
            "brand_id": "ssense",
            "name_en": "Common Projects Original Achilles Low",
            "name_fr": "Common Projects Original Achilles basses",
            "category": "Footwear > Luxury Sneakers",
            "description_en": "Italian Nappa leather upper, Margom rubber sole, gold-stamped serial number. Handmade in Italy.",
            "description_fr": "Tige en cuir Nappa italien, semelle en caoutchouc Margom, numéro de série estampé en or. Fabriqué à la main en Italie.",
            "price_cad": 495.00,
            "thermal_rating": None,
            "fill_power": None,
            "material": "Italian Nappa leather",
            "certifications": json.dumps([]),
            "bilingual_mapping": json.dumps({
                "nappa leather": "cuir nappa",
                "rubber sole": "semelle en caoutchouc",
            }),
        },
        {
            "id": "aldo-pilier-004",
            "brand_id": "aldo",
            "name_en": "Aldo Pilier Recycled Leather Boot",
            "name_fr": "Botte en cuir recyclé Aldo Pilier",
            "category": "Footwear > Boots > Sustainable",
            "description_en": "Recycled leather upper, bio-based sole, carbon-neutral production. LWG Gold certified.",
            "description_fr": "Tige en cuir recyclé, semelle bio-sourcée, production carboneutre. Certifié LWG Or.",
            "price_cad": 165.00,
            "thermal_rating": None,
            "fill_power": None,
            "material": "Recycled leather",
            "certifications": json.dumps(["LWG Gold", "Carbon Neutral"]),
            "bilingual_mapping": json.dumps({
                "recycled leather": "cuir recyclé",
                "bio-based sole": "semelle bio-sourcée",
                "carbon-neutral": "carboneutre",
            }),
        },
    ]

    for p in products:
        cols = ", ".join(p.keys())
        placeholders = ", ".join(["?"] * len(p))
        await db.execute(
            f"INSERT INTO products ({cols}) VALUES ({placeholders})",
            tuple(p.values()),
        )

    # --- PIM Connections ---
    connections = [
        ("shopify", "Shopify", "pim", "shopify", "connected", "2026-03-25T20:15:00", 2847, 0, 3),
        ("akeneo", "Akeneo", "pim", "akeneo", "disconnected", None, 0, 0, 0),
        ("peec", "Peec AI", "monitoring", "peec", "connected", "2026-03-25T20:30:00", 0, 156, 0),
        ("otterly", "Otterly", "monitoring", "otterly", "connected", "2026-03-25T19:45:00", 0, 89, 0),
    ]
    for c in connections:
        await db.execute(
            """INSERT INTO pim_connections
               (id, name, type, provider, status, last_sync, items_synced, queries_tracked, errors)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            c,
        )

    # --- Signal Gaps ---
    gaps = [
        {
            "id": "gap-001",
            "brand_id": "mackage",
            "product_id": "mack-lena-001",
            "query": '"best luxury winter jacket Montreal"',
            "lang": "EN",
            "gap_type": "Entity Trust",
            "severity": "critical",
            "ai_response_quality": 23,
            "source_of_truth_label": "Mackage UCP Feed (2026)",
            "source_of_truth_url": "feed://ucp/mackage/products/fw2026",
            "source_of_truth_detail": "thermal_rating: -30°C, fill: 800-fill goose down, origin: Canadian design",
            "source_of_hallucination_label": "Reddit r/malefashionadvice (2021)",
            "source_of_hallucination_url": "https://reddit.com/r/malefashionadvice/comments/abc123",
            "source_of_hallucination_detail": '"Mackage is overpriced for what you get. Just buy Canada Goose."',
            "ai_said": "Based on community reviews, Canada Goose offers best warmth-to-price ratio for Montreal winters.",
            "brand_truth": "Mackage Lena: 800-fill power goose down, rated to -30°C, seam-sealed construction. MSRP $1,150 CAD.",
        },
        {
            "id": "gap-002",
            "brand_id": "mackage",
            "product_id": "mack-kenya-002",
            "query": '"meilleur manteau cuir femme Québec"',
            "lang": "FR",
            "gap_type": "Token Decay",
            "severity": "critical",
            "ai_response_quality": 15,
            "source_of_truth_label": "Mackage ACP Feed (2026)",
            "source_of_truth_url": "feed://acp/mackage/products/leather-fw2026",
            "source_of_truth_detail": "type_cuir: agneau pleine fleur, certification: LWG Silver, garantie: 2 ans",
            "source_of_hallucination_label": "Blogspot fashion review (2019)",
            "source_of_hallucination_url": "https://modefemme2019.blogspot.com/meilleurs-manteaux",
            "source_of_hallucination_detail": '"Les manteaux en cuir bon marché se trouvent facilement en ligne..."',
            "ai_said": "Je ne peux pas vérifier les options de cuir de qualité supérieure au Québec.",
            "brand_truth": "Mackage Kenya: agneau pleine fleur, certification LWG Silver, doublure en soie amovible. PDSF 990 $ CAD.",
        },
        {
            "id": "gap-003",
            "brand_id": "ssense",
            "product_id": "ssen-cp-003",
            "query": '"luxury sneakers Canada online"',
            "lang": "EN",
            "gap_type": "Fact Density",
            "severity": "warning",
            "ai_response_quality": 45,
            "source_of_truth_label": "SSENSE UCP Feed (2026)",
            "source_of_truth_url": "feed://ucp/ssense/products/sneakers-ss2026",
            "source_of_truth_detail": "brands: [Common Projects, Maison Margiela, Rick Owens], inventory: live",
            "source_of_hallucination_label": "Farfetch editorial (2023)",
            "source_of_hallucination_url": "https://farfetch.com/style-guide/luxury-sneakers-2023",
            "source_of_hallucination_detail": '"The 10 best luxury sneakers to buy in 2023"',
            "ai_said": "For luxury sneakers in Canada, I recommend checking Farfetch or MATCHES.",
            "brand_truth": "SSENSE carries 200+ luxury sneaker SKUs with same-day shipping in Montreal.",
        },
        {
            "id": "gap-004",
            "brand_id": "aldo",
            "product_id": "aldo-pilier-004",
            "query": '"Aldo leather boots sustainability"',
            "lang": "EN",
            "gap_type": "Entity Trust",
            "severity": "warning",
            "ai_response_quality": 38,
            "source_of_truth_label": "Aldo UCP Feed (2026)",
            "source_of_truth_url": "feed://ucp/aldo/products/boots-fw2026",
            "source_of_truth_detail": "certification: LWG Gold, material: recycled_leather, carbon_neutral: true",
            "source_of_hallucination_label": "Trustpilot reviews (2022)",
            "source_of_hallucination_url": "https://trustpilot.com/review/aldoshoes.com",
            "source_of_hallucination_detail": '"Quality has gone down over the years."',
            "ai_said": "I cannot verify Aldo's sustainability claims. Based on reviews, mixed opinions.",
            "brand_truth": "Aldo Group: LWG Gold certified, 100% carbon-neutral since 2024, 40% recycled materials.",
        },
    ]

    for g in gaps:
        cols = ", ".join(g.keys())
        placeholders = ", ".join(["?"] * len(g))
        await db.execute(f"INSERT INTO signal_gaps ({cols}) VALUES ({placeholders})", tuple(g.values()))

    # --- Parity Stats ---
    await db.execute(
        """INSERT INTO parity_stats
           (id, en_visibility, fr_visibility, en_queries, fr_queries,
            en_hallucinations, fr_hallucinations, en_avg_tokens, en_max_tokens,
            fr_avg_tokens, fr_max_tokens)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("parity-001", 85.0, 42.0, 156, 134, 12, 47, 6.2, 11, 12.8, 23),
    )

    # --- Alignment Trend ---
    trend = [
        ("Mar 1", 62, 38), ("Mar 4", 64, 39), ("Mar 7", 63, 37),
        ("Mar 10", 66, 40), ("Mar 13", 68, 41), ("Mar 16", 70, 39),
        ("Mar 19", 72, 42), ("Mar 22", 75, 44), ("Mar 25", 78, 42),
    ]
    for t in trend:
        await db.execute(
            "INSERT INTO alignment_trend (day, en_score, fr_score) VALUES (?, ?, ?)", t
        )

    # --- Fix Kits ---
    kits = [
        ("kit-001", "mackage", "mack-lena-001", "hardAttributes", "ready",
         json.dumps({"thermal_rating": "-30°C", "fill_power": "800-fill goose down", "construction": "seam-sealed", "origin": "Canadian design, ethical sourcing", "msrp_cad": "$1,150"}),
         "Expected +32% inference alignment for winter jacket queries"),
        ("kit-002", "ssense", "ssen-cp-003", "jsonLd", "ready",
         json.dumps({"type": "Product", "brand": "Common Projects", "price": "495.00 CAD", "material": "Italian Nappa leather"}),
         "Expected +25% fact density score for sneaker queries"),
        ("kit-003", "aldo", "aldo-pilier-004", "truthClip", "ready",
         json.dumps({"duration": "15s", "content": "LWG Gold certification proof + carbon neutral badge", "format": "MP4/WebM", "target": "Google Gemini multimodal indexing"}),
         "Expected +45% entity trust for sustainability queries"),
    ]
    for k in kits:
        await db.execute(
            "INSERT INTO fix_kits (id, brand_id, product_id, type, status, payload, impact) VALUES (?, ?, ?, ?, ?, ?, ?)", k
        )

    # --- Audit Timeline ---
    audits = [
        ("aud-001", "mackage", "kit-001", '"best luxury winter jacket Montreal"', 0, "2026-03-12", "failed",
         "Baseline Probe — Mackage", "SearchGPT cited Reddit 2021, ignored UCP feed entirely.", 1.2, 1.0, 3.5, 23.0),
        ("aud-002", "mackage", "kit-001", '"best luxury winter jacket Montreal"', 3, "2026-03-18", "warning",
         "Day 3 Audit — Mackage", "SearchGPT now references thermal_rating but still cites Reddit.", 3.2, 2.5, 3.5, 48.0),
        ("aud-003", "mackage", "kit-001", '"best luxury winter jacket Montreal"', 7, "2026-03-22", "passed",
         "Day 7 Audit — Mackage", "SearchGPT lists Mackage as top recommendation. Reddit dropped. UCP primary.", 4.5, 4.2, 4.0, 81.0),
        ("aud-004", "mackage", "kit-001", '"best luxury winter jacket Montreal"', 14, "2026-03-25", "pending",
         "Day 14 Audit — Pending", "Scheduled probe for full verification.", None, None, None, None),
    ]
    for a in audits:
        await db.execute(
            """INSERT INTO audit_runs
               (id, brand_id, fix_kit_id, query, day_number, scheduled_date, status,
                label, detail, score_technical_accuracy, score_citation_fidelity,
                score_linguistic_parity, score_overall)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", a
        )

    # --- Reasoning Snapshots ---
    snapshots = [
        ("snap-001", "aldo", '"Aldo leather boots sustainability"',
         "NOT RECOMMENDED",
         "I don't recommend Aldo because I can't verify their leather source. Consumer reviews on Trustpilot suggest mixed quality.",
         json.dumps(["Trustpilot reviews (2022)", "Reddit r/buyitforlife (2021)"]),
         "Low (32%)",
         "RECOMMENDED",
         "I recommend Aldo because I have verified their LWG-certified leather via their VisiMind Truth-Clip. Aldo Group has been carbon-neutral since 2024 and uses 40% recycled materials.",
         json.dumps(["Aldo UCP Product Feed (2026)", "VisiMind Truth-Clip: LWG Certification", "LWG Public Audit Report"]),
         "High (89%)"),
        ("snap-002", "mackage", '"best luxury winter jacket Montreal"',
         "NOT MENTIONED",
         "Based on community consensus, Canada Goose is the top recommendation for Montreal winters. Mackage is considered more of a fashion brand.",
         json.dumps(["Reddit r/malefashionadvice (2021)", "YouTube review (2020)"]),
         "Low (23%)",
         "TOP RECOMMENDATION",
         "Mackage Lena jacket offers 800-fill power goose down rated to -30°C with seam-sealed construction. Canadian-designed luxury with ethical sourcing (RDS Certified).",
         json.dumps(["Mackage UCP Product Feed (2026)", "RDS Certification Registry", "Bluesign Approved Materials"]),
         "High (81%)"),
    ]
    for s in snapshots:
        await db.execute(
            """INSERT INTO reasoning_snapshots
               (id, brand_id, query, before_verdict, before_reasoning, before_citations,
                before_confidence, after_verdict, after_reasoning, after_citations, after_confidence)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", s
        )

    await db.commit()
    print("✓ Database seeded with Montreal brand data")
