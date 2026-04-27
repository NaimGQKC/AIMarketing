"""
VisiMind — Database Seed Data
Seeds ONLY ground truth: brands, products, and PIM connections.
All metrics, gaps, audits, and scores are populated by real engine runs.
"""
import json


async def seed_database(db):
    """Seed brands, products, and PIM connections. Everything else comes from real probes."""
    # --- Daily Probe Counter (Simulate 3 spots used to show 7 left) ---
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    await db.execute(
        "INSERT OR REPLACE INTO daily_probe_counter (date, count) VALUES (?, ?)",
        (today, 3)
    )

    cursor = await db.execute("SELECT COUNT(*) FROM brands")
    count = (await cursor.fetchone())[0]
    if count > 0:
        await db.commit()
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

    # --- Products (PIM Ground Truth) ---
    products = [
        {
            "id": "mack-lena-001",
            "brand_id": "mackage",
            "name_en": "Mackage Lena Down Jacket",
            "name_fr": "Manteau en duvet Mackage Lena",
            "category": "Outerwear > Premium Down > Arctic-Rated",
            "description_en": "800-fill power responsibly-sourced goose down, rated to -30C, seam-sealed construction, removable fur hood. Canadian-designed luxury outerwear.",
            "description_fr": "Duvet d'oie de facteur de gonflement 800, resistant jusqu'a -30C, construction a coutures scellees, capuchon amovible en fourrure. Vetements de luxe concus au Canada.",
            "price_cad": 1150.00,
            "thermal_rating": "-30C",
            "fill_power": "800-fill",
            "material": "Goose down, nylon shell",
            "certifications": json.dumps(["RDS Certified", "Bluesign Approved"]),
            "bilingual_mapping": json.dumps({
                "800-fill power": "Facteur de gonflement 800",
                "seam-sealed": "coutures scellees",
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
            "description_fr": "Cuir d'agneau pleine fleur, certifie LWG Argent, doublure en soie amovible, fabrication ethique.",
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
            "description_fr": "Tige en cuir Nappa italien, semelle en caoutchouc Margom, numero de serie estampe en or. Fabrique a la main en Italie.",
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
            "name_fr": "Botte en cuir recycle Aldo Pilier",
            "category": "Footwear > Boots > Sustainable",
            "description_en": "Recycled leather upper, bio-based sole, carbon-neutral production. LWG Gold certified.",
            "description_fr": "Tige en cuir recycle, semelle bio-sourcee, production carboneutre. Certifie LWG Or.",
            "price_cad": 165.00,
            "thermal_rating": None,
            "fill_power": None,
            "material": "Recycled leather",
            "certifications": json.dumps(["LWG Gold", "Carbon Neutral"]),
            "bilingual_mapping": json.dumps({
                "recycled leather": "cuir recycle",
                "bio-based sole": "semelle bio-sourcee",
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
        ("shopify", "Shopify", "pim", "shopify", "connected", None, 0, 0, 0),
        ("akeneo", "Akeneo", "pim", "akeneo", "disconnected", None, 0, 0, 0),
        ("peec", "Peec AI", "monitoring", "peec", "connected", None, 0, 0, 0),
        ("otterly", "Otterly", "monitoring", "otterly", "connected", None, 0, 0, 0),
    ]
    for c in connections:
        await db.execute(
            """INSERT INTO pim_connections
               (id, name, type, provider, status, last_sync, items_synced, queries_tracked, errors)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            c,
        )

    await db.commit()
    print("[OK] Database seeded with brand ground truth")
