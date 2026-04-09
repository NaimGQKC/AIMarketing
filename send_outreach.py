"""
send_outreach.py — Simple outreach email sender for VisiMind
Usage: python send_outreach.py

Reads emails from outreach_queue.json, lets you review each one,
and sends via Gmail SMTP. Logs results to sent_log.json.

HOW TO FIND EMAIL ADDRESSES:
  1. Apollo.io — Free tier gives 50 email credits/month. Search by name + company.
  2. Snov.io Chrome extension — Finds emails on LinkedIn profiles. Free tier available.
  3. Hunter.io — Enter a domain, get the email pattern (e.g. first.last@company.com).
  4. LinkedIn DM — If you can't find an email, send the LinkedIn connection request
     first (included in outreach_queue.json) and follow up there instead.
  5. Google: "Gregoire Baret Aldo email" sometimes just works.

GMAIL SETUP:
  You need a Gmail App Password, NOT your regular password.
  1. Go to myaccount.google.com > Security > 2-Step Verification (enable it)
  2. At the bottom, click "App passwords"
  3. Create one for "Mail" on "Windows Computer"
  4. Copy the 16-character password into your .env file
"""

import smtplib
import json
import os
import sys
import tempfile
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def load_env(path=".env"):
    """Read .env file into a dict. No dependencies needed."""
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def load_queue(path="outreach_queue.json"):
    """Load the outreach queue from JSON."""
    if not os.path.exists(path):
        print(f"Error: {path} not found. Create it first.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(queue, path="outreach_queue.json"):
    """Save the updated queue back to disk."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)


def load_sent_log(path="sent_log.json"):
    """Load or create the sent log."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_sent_log(log, path="sent_log.json"):
    """Save sent log to disk."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def edit_in_editor(text):
    """Open text in the default editor and return the edited version."""
    editor = os.environ.get("EDITOR", "notepad")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(text)
        tmppath = f.name
    try:
        subprocess.call([editor, tmppath])
        with open(tmppath, "r", encoding="utf-8") as f:
            return f.read()
    finally:
        os.unlink(tmppath)


def display_email(entry):
    """Print an email for review."""
    print("\n" + "=" * 60)
    print(f"  TO:      {entry['to_name']} <{entry['to_email']}>")
    print(f"  COMPANY: {entry['company']}")
    print(f"  SUBJECT: {entry['subject']}")
    if entry.get("linkedin_url"):
        print(f"  LINKEDIN: {entry['linkedin_url']}")
    if entry.get("notes"):
        print(f"  NOTES:   {entry['notes']}")
    print("-" * 60)
    print(entry["body"])
    print("=" * 60)


def send_email(smtp_conn, from_addr, entry):
    """Send a single email. Returns True on success."""
    msg = MIMEMultipart("alternative")
    msg["From"] = from_addr
    msg["To"] = entry["to_email"]
    msg["Subject"] = entry["subject"]
    msg.attach(MIMEText(entry["body"], "plain", "utf-8"))
    smtp_conn.sendmail(from_addr, entry["to_email"], msg.as_string())
    return True


def main():
    # Load credentials
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    env = load_env()
    gmail_addr = env.get("GMAIL_ADDRESS")
    gmail_pass = env.get("GMAIL_APP_PASSWORD")

    if not gmail_addr or not gmail_pass:
        print("Error: Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD in .env")
        print("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    # Load queue
    queue = load_queue()
    pending = [e for e in queue if e.get("status") == "pending"]

    if not pending:
        print("No pending emails in the queue. All done!")
        sys.exit(0)

    print(f"\nVisiMind Outreach Sender")
    print(f"Found {len(pending)} pending email(s) out of {len(queue)} total.\n")

    # Connect to Gmail
    print("Connecting to Gmail SMTP...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_addr, gmail_pass)
        print("Connected successfully.\n")
    except smtplib.SMTPAuthenticationError:
        print("Error: Gmail authentication failed.")
        print("Make sure you're using an App Password, not your regular password.")
        print("See the top of this script for setup instructions.")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to Gmail: {e}")
        sys.exit(1)

    # Process emails
    sent_log = load_sent_log()
    sent_count = 0
    skipped_count = 0
    quit_early = False

    for entry in pending:
        if entry["to_email"] == "TO_FILL":
            print(f"\n*** SKIPPING {entry['to_name']} ({entry['company']}) — email address is TO_FILL ***")
            print(f"    Find their email using Apollo.io, Snov.io, or Hunter.io")
            if entry.get("linkedin_url"):
                print(f"    Or connect on LinkedIn: {entry['linkedin_url']}")
            skipped_count += 1
            continue

        display_email(entry)

        while True:
            choice = input("\n[y] Send  [n] Skip  [e] Edit  [q] Quit > ").strip().lower()

            if choice == "y":
                try:
                    send_email(server, gmail_addr, entry)
                    entry["status"] = "sent"
                    sent_log.append({
                        "id": entry["id"],
                        "to_name": entry["to_name"],
                        "to_email": entry["to_email"],
                        "company": entry["company"],
                        "subject": entry["subject"],
                        "sent_at": datetime.now().isoformat(),
                    })
                    sent_count += 1
                    print(f"  -> Sent to {entry['to_name']}!")
                except Exception as e:
                    print(f"  -> Failed to send: {e}")
                    entry["status"] = "error"
                break

            elif choice == "n":
                entry["status"] = "skipped"
                skipped_count += 1
                print(f"  -> Skipped.")
                break

            elif choice == "e":
                entry["body"] = edit_in_editor(entry["body"])
                display_email(entry)
                # Loop back to ask again

            elif choice == "q":
                quit_early = True
                break

            else:
                print("  Type y, n, e, or q.")

        if quit_early:
            break

    # Cleanup
    try:
        server.quit()
    except Exception:
        pass

    # Save state
    save_queue(queue)
    save_sent_log(sent_log)

    # Summary
    remaining = len([e for e in queue if e.get("status") == "pending"])
    print("\n" + "=" * 60)
    print(f"  DONE")
    print(f"  Sent:      {sent_count}")
    print(f"  Skipped:   {skipped_count}")
    print(f"  Remaining: {remaining}")
    print("=" * 60)
    print(f"\nQueue saved to outreach_queue.json")
    print(f"Send log saved to sent_log.json")


if __name__ == "__main__":
    main()
