import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect("visimind.db")
c = conn.cursor()

c.execute("SELECT id, slug FROM brands")
brands = c.fetchall()

now = datetime.utcnow().isoformat()
kits = []

for brand_id, brand_slug in brands:
    c.execute("SELECT id FROM fix_kits WHERE brand_id = ?", (brand_id,))
    if c.fetchone():
        continue
    
    kits.extend([
        (
            f"kit-{brand_id}-1", brand_id, f"{brand_slug}-prod-001", "hardAttributes", "ready",
            json.dumps({"description": f"Verified product attributes for {brand_slug.title()}", "verified": True}),
            "Expected +20% inference alignment", None, now
        ),
        (
            f"kit-{brand_id}-2", brand_id, f"{brand_slug}-prod-002", "jsonLd", "ready",
            json.dumps({"@type": "Brand", "name": brand_slug.title(), "founder": "TBD"}),
            "Expected +30% fact density score", None, now
        ),
        (
            f"kit-{brand_id}-3", brand_id, f"{brand_slug}-vid-001", "truthClip", "ready",
            json.dumps({"duration": "15s", "content": "Official brand certification", "format": "MP4"}),
            "Expected +15% entity trust", None, now
        )
    ])

if kits:
    c.executemany(
        """INSERT INTO fix_kits (id, brand_id, product_id, type, status, payload, impact, deployed_at, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        kits
    )
    conn.commit()
    print(f"Retroactively created {len(kits)} fix kits for {len(kits)//3} brands.")
else:
    print("All brands already have fix kits.")

conn.close()
