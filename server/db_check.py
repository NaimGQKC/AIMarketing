import sqlite3

conn = sqlite3.connect("visimind.db")
c = conn.cursor()

with open("db_report2.txt", "w", encoding="utf-8") as f:
    # Signal gaps per brand
    f.write("--- SIGNAL_GAPS per brand ---\n")
    c.execute("SELECT brand_id, COUNT(*) as cnt FROM signal_gaps GROUP BY brand_id")
    for r in c.fetchall():
        f.write(f"  brand_id={r[0]}, gaps={r[1]}\n")

    # Probe results per task
    f.write("\n--- PROBE_RESULTS per task ---\n")
    c.execute("SELECT task_id, COUNT(*) as cnt, GROUP_CONCAT(DISTINCT query) as queries FROM probe_results GROUP BY task_id")
    for r in c.fetchall():
        f.write(f"  task={r[0][:12]}..., probes={r[1]}, queries={r[2][:80] if r[2] else 'N/A'}\n")

    # Tasks: which brand names were used?
    f.write("\n--- TASKS with results ---\n")
    c.execute("SELECT id, status, progress, total, result FROM tasks WHERE type='ingest' ORDER BY rowid DESC LIMIT 5")
    for r in c.fetchall():
        f.write(f"  id={r[0][:12]}..., status={r[1]}, progress={r[2]}/{r[3]}, result_preview={str(r[4])[:200] if r[4] else 'None'}\n")

    # Fix kits per brand
    f.write("\n--- FIX_KITS per brand ---\n")
    c.execute("SELECT brand_id, COUNT(*) as cnt FROM fix_kits GROUP BY brand_id")
    for r in c.fetchall():
        f.write(f"  brand_id={r[0]}, kits={r[1]}\n")

    # All signal gaps with brand
    f.write("\n--- ALL SIGNAL_GAPS ---\n")
    c.execute("SELECT id[:12], brand_id, query, lang, gap_type, severity FROM signal_gaps")
    for r in c.fetchall():
        f.write(f"  {r}\n")

conn.close()
print("Done - check db_report2.txt")
