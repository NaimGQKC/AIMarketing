import sqlite3
import json

def check_db():
    conn = sqlite3.connect('visimind.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print("=== VISIMIND DATABASE AUDIT ===\n")

    # 1. Brands
    c.execute("SELECT id, name FROM brands")
    brands = c.fetchall()
    print(f"--- BRANDS ({len(brands)}) ---")
    for b in brands[:5]:
        print(f"  [ID: {b['id']}] Name: {b['name']}")
    if len(brands) > 5: print(f"  ... and {len(brands)-5} more")

    # 2. Probe Results (The raw AI responses you ingested)
    c.execute("SELECT COUNT(*) as count FROM probe_results")
    probes_count = c.fetchone()[0]
    print(f"\n--- PROBE RESULTS ({probes_count}) ---")
    c.execute("SELECT query, lang, brand_mentioned FROM probe_results LIMIT 3")
    for p in c.fetchall():
        mention = "YES" if p['brand_mentioned'] else "NO"
        print(f"  [{p['lang']}] Query: {p['query'][:50]}... | Mentioned: {mention}")

    # 3. Signal Gaps (The hallucinations diagnosed)
    c.execute("SELECT COUNT(*) as count FROM signal_gaps")
    gaps_count = c.fetchone()[0]
    print(f"\n--- SIGNAL GAPS ({gaps_count}) ---")
    c.execute("SELECT brand_id, query, severity, gap_type FROM signal_gaps LIMIT 3")
    for g in c.fetchall():
        print(f"  [{g['severity'].upper()}] Brand: {g['brand_id']} | Type: {g['gap_type']} | Q: {g['query'][:30]}...")

    # 4. Fix Kits (The remediations)
    c.execute("SELECT COUNT(*) as count FROM fix_kits")
    kits_count = c.fetchone()[0]
    print(f"\n--- FIX KITS ({kits_count}) ---")
    
    conn.close()

if __name__ == "__main__":
    check_db()
