# VisiMind Day 1 Action Plan: Thursday, April 9, 2026
## Alejandro's Execution Playbook (4-6 hours of focused time)

**Goal:** 10-15 genuine outreach touches. Quality over quantity.
**Mindset:** You are not selling. You are a student founder sharing real research with people who need it.

---

# MORNING BLOCK (2 hours, 9:00 - 11:00 AM)

---

## Step 1: Gmail App Password Setup (5 min | 9:00 - 9:05)

You need this before sending any cold emails from a tool or script.

1. Go to https://myaccount.google.com/security
2. Make sure 2-Step Verification is ON (required for App Passwords)
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" as the app, "Windows Computer" as the device
5. Click "Generate" and copy the 16-character password
6. Save it somewhere secure (you will need it if you use any email automation tool from `RESOURCES-LEAD-GEN.md`, Section 2, "Cold Email Tools")

If you already have this set up, skip to Step 2.

---

## Step 2: Review and Refine Your Top 5 Brand Emails (30 min | 9:05 - 9:35)

Open `MASTER-OUTREACH-READY.md`, section "PRIORITY 1: BRAND CONTACTS (Design Partners)."

Your 5 emails are already written. Your job is to personalize and approve them, not rewrite them.

**For each email, spend 5-6 minutes doing this:**

### Email 1: Gregoire Baret, VP Consumer Experience, ALDO GROUP
- File: `MASTER-OUTREACH-READY.md`, lines 12-39
- Quick check: Search LinkedIn for Gregoire Baret. Confirm he is still VP at Aldo. Look at his last 2-3 posts. If he posted about anything relevant, add a one-line reference to the email opening.
- The email subject "Aldo's new Shopify stack has an AI blind spot" is strong. Keep it.
- Confirm the audit claim: Aldo scored 5/10. Cross-reference with `brand-audit-results.md` if needed.

### Email 2: Kelly Cochrane, Global Director eCommerce, MACKAGE
- File: `MASTER-OUTREACH-READY.md`, lines 43-69
- Quick check: Search LinkedIn for Kelly Cochrane at Mackage. Confirm role.
- The subject "Mackage's homepage is missing a meta description" is specific and attention-grabbing. Keep it.
- Verify the meta description claim is still true: open mackage.com, right-click, View Source, search for `<meta name="description"`. If it is still missing, the email is good to go. If they fixed it, adjust the email hook.

### Email 3: Fadi Farha, VP Growth Marketing, SSENSE
- File: `MASTER-OUTREACH-READY.md`, lines 73-101
- Quick check: Fadi's LinkedIn link in the file points to a LeadAFI post, not his direct profile. Search LinkedIn directly for "Fadi Farha SSENSE Montreal."
- The 403 error finding is dramatic and verifiable. Before sending, quickly test: open a terminal and run `curl -A "ChatGPT-User" https://ssense.com`. If it still returns 403, the email stands.

### Email 4: Jasmine Bouchard, Director eCommerce, RUDSAK
- File: `MASTER-OUTREACH-READY.md`, lines 105-127
- This is your WARMEST lead. Rudsak already has an llms.txt file. They are already thinking about AI.
- Quick check: Visit rudsak.com/llms.txt to confirm it still exists and is still a raw product dump.
- Note: Jasmine's contact is from ZoomInfo, not LinkedIn. You may need to find her email via Apollo.io (see Step 11).

### Email 5: Maxime Boyer, Chief Digital Officer, GROUPE DYNAMITE
- File: `MASTER-OUTREACH-READY.md`, lines 130-151
- Quick check: Search LinkedIn for Maxime Boyer Groupe Dynamite. Confirm CDO role.
- Contact is from ZoomInfo. Same as Jasmine, you will need to find the email address later.

**Output of this step:** 5 approved, lightly personalized emails saved in a Google Doc or text file, ready to send once you have email addresses.

---

## Step 3: Send First 3 LinkedIn Connection Requests (15 min | 9:35 - 9:50)

Open `MASTER-OUTREACH-READY.md`. Each brand contact has a pre-written LinkedIn connection request under "LinkedIn Connection Request (300 chars)."

**Send in this order (warmest to coldest):**

### Connection 1: Gregoire Baret (ALDO)
- LinkedIn: https://ca.linkedin.com/in/gregoirebaret
- Message: `MASTER-OUTREACH-READY.md`, lines 18-19
- Copy the message exactly. It is already under 300 characters.

### Connection 2: Kelly Cochrane (MACKAGE)
- LinkedIn: https://www.linkedin.com/in/kellycochrane/
- Message: `MASTER-OUTREACH-READY.md`, lines 48-49
- Copy exactly as written.

### Connection 3: Fadi Farha (SSENSE)
- Search LinkedIn for "Fadi Farha SSENSE" (the link in the file is indirect)
- Message: `MASTER-OUTREACH-READY.md`, lines 78-79
- Copy exactly as written.

**Do NOT send to Jasmine (RUDSAK) or Maxime (Dynamite) yet.** Their LinkedIn profiles need to be found first. Save them for Day 2.

**Important:** LinkedIn limits you to ~100 connection requests per week. 3 per day is safe and sustainable.

---

## Step 4: Post First Shopify Community Reply (10 min | 9:50 - 10:00)

Open `MASTER-OUTREACH-READY.md`, section "SHOPIFY COMMUNITY (Highest priority, most active)."

**Post to this thread first:**

- Target: Geoffy
- Thread: https://community.shopify.com/t/are-shopify-stores-losing-visibility-to-ai-search-sge-chatgpt-etc/599726
- Message: `MASTER-OUTREACH-READY.md`, lines 186-189
- Why this one first: Geoffy shared data (the 12% stat). This is a knowledge-exchange reply, not a sales pitch. It positions you as someone who has built tooling for a problem they care about.

**Before posting:**
1. Create a Shopify Community account if you do not have one (use your real name)
2. Read the thread to make sure the conversation is still active
3. Paste the pre-written message. Adjust the stat reference if the thread has evolved since the message was written.
4. Do NOT include a link to VisiMind in the first post. Just engage. Links in first posts get flagged as spam.

---

## Step 5: Send First Cold Email If Email Address Found (10 min | 10:00 - 10:10)

If during Step 2 you already found a direct email for any of your top 5 contacts, send ONE email now.

**Priority order for first email:**
1. Jasmine Bouchard (RUDSAK) - warmest lead, llms.txt signal
2. Gregoire Baret (ALDO) - freshest Shopify migration
3. Kelly Cochrane (MACKAGE) - specific meta description finding

**How to find emails quickly (skip if no luck in 5 min):**
- Try `firstname.lastname@company.com` pattern
- Try Hunter.io free lookup: https://hunter.io (50 free searches/month)
- Try Apollo.io: https://apollo.io (free tier, see Step 11 for full setup)

**If you find an email:**
- Copy the approved email from Step 2
- Send from your personal Gmail (not a mass tool)
- Subject line matters most. Use the ones from `MASTER-OUTREACH-READY.md`
- Add a 1-line PS: "PS: I'm a student at [your university] in Montreal. This is a genuine research project, not a sales blast."

**If you cannot find any email in 5 min:** Move on. You will do a proper email-finding session in Step 11.

---

## Step 6: Buffer / Catch-Up (50 min | 10:10 - 11:00)

If steps 1-5 took less time, use the remaining time to:
- Send one more Shopify Community reply (pick ella1234 or Lyros from `MASTER-OUTREACH-READY.md`, lines 167-177)
- OR read 2-3 recent posts on r/shopify or r/ecommerce about AI visibility to find new threads to reply to (reference `reddit-outreach-targets.md` for pain-point categories to search for)

---

# MIDDAY BLOCK (1.5 hours, 11:30 AM - 1:00 PM)

---

## Step 7: Join MTL+ECOMMERCE Community (10 min | 11:30 - 11:40)

Reference: `french-outreach.md` for Quebec-specific communities.

1. Search Facebook for "MTL+ECOMMERCE" or "Montreal Ecommerce" groups
2. Also search for "Shopify Quebec" and "E-commerce Quebec" groups
3. Request to join the most active one (look at post frequency)
4. While waiting for approval, also join:
   - Shopify Community forums (if not done in Step 4): https://community.shopify.com
   - Indie Hackers: https://www.indiehackers.com (create account if needed)

---

## Step 8: Post Intro in One Community (15 min | 11:40 - 11:55)

**Where to post:** Indie Hackers (fastest approval, no gatekeeping)

**What to post (write this yourself, but use this structure):**

Title: "Building an AI search visibility tool for Canadian luxury brands (from Montreal)"

Body structure:
- Who you are (student founder in Montreal)
- The problem (Canadian brands are invisible in ChatGPT/Perplexity)
- What you built (VisiMind - audits + fixes)
- The bilingual angle (this is your unique hook)
- Ask: "Looking for feedback from anyone working on GEO/AEO or running an ecommerce brand"

Reference `MASTER-OUTREACH-READY.md`, section "PRIORITY 3: GEO THOUGHT LEADERS" (lines 219-240) for the tone and framing to use. Keep it conversational and humble.

Do NOT link to your site unless Indie Hackers posts require it. Focus on the story.

---

## Step 9: Reply to 3 Indie Hackers / Shopify Threads (30 min | 11:55 - 12:25)

Open `MASTER-OUTREACH-READY.md`, section "INDIE HACKERS" (lines 193-206) and "SHOPIFY COMMUNITY" (lines 159-189).

**Reply 1: William Wang on Indie Hackers** (10 min)
- Thread: https://www.indiehackers.com/post/scanning-2-500-websites-taught-me-what-makes-sites-visible-to-ai-search-5178c0bd43
- Message: `MASTER-OUTREACH-READY.md`, lines 198-199
- Why: William scanned 2,500 sites. He is a fellow builder. This is a peer conversation.

**Reply 2: Mukul Sharma on Indie Hackers** (10 min)
- Thread: https://www.indiehackers.com/post/from-seo-to-aeo-why-indie-hackers-need-to-optimize-for-ai-not-just-google-PEoo6jmv48hjBrrufCGh
- Message: `MASTER-OUTREACH-READY.md`, lines 204-205
- Why: Mukul is arguing for the SEO-to-AEO shift. You are building the tool for it.

**Reply 3: Gabe_Stillwater on Shopify Community** (10 min)
- Thread: https://community.shopify.com/t/question-about-ai-visibility-for-shopify-stores/587072
- Message: `MASTER-OUTREACH-READY.md`, lines 163-165
- Why: Gabe manages 8,500+ SKUs. This is a real operational pain point. Your Self-Consistency Mining feature directly addresses it.

**For each reply:**
1. Read the thread first (2 min)
2. Adapt the pre-written message if the conversation has evolved (2 min)
3. Post (1 min)
4. Bookmark the thread so you can check for responses tomorrow

---

## Step 10: Send 3 Twitter/X DMs to GEO Thought Leaders (15 min | 12:25 - 12:40)

Open `TWITTER_OUTREACH_STRATEGY.md`, Part 2: DM Templates (lines 48-70), and `MASTER-OUTREACH-READY.md`, section "PRIORITY 3: GEO THOUGHT LEADERS" (lines 219-240).

**DM 1: Jason Barnard (@jasonmbarnard)**
- Message: `MASTER-OUTREACH-READY.md`, lines 232-234
- He invented AEO. His Knowledge Graph work directly overlaps with VisiMind's JSON-LD remediation.
- Keep it short and respectful. You are a student asking for perspective, not pitching.

**DM 2: Lily Ray (@lilyraynyc)**
- Message: `MASTER-OUTREACH-READY.md`, lines 238-239
- She has ~108K followers. Do NOT pitch. Ask for her perspective on what data points matter for GEO tooling.

**DM 3: Aleyda Solis (@aleyda)**
- Use DM Template 1 from `TWITTER_OUTREACH_STRATEGY.md`, lines 53-69
- She is THE expert on multilingual GEO. Your French token decay finding is exactly her domain.
- Customize the template: replace `[specific topic]` with "multilingual GEO frameworks" and reference the bilingual data specifically.

**Before sending:**
- Follow all 3 accounts first
- Like/retweet one of their recent posts (genuine, not performative)
- Then send the DM

---

# AFTERNOON BLOCK (1.5 hours, 2:00 - 3:30 PM)

---

## Step 11: Sign Up for Apollo.io Free Tier (5 min | 2:00 - 2:05)

Reference: `RESOURCES-LEAD-GEN.md`, Section 2, "Email Finding Tools" (line 56)

1. Go to https://apollo.io
2. Sign up with your Gmail
3. Free tier gives you: 10,000 contacts in database, 5 mobile credits/month, 10 export credits/month
4. This is your primary email-finding tool for now

---

## Step 12: Find Email Addresses for Top 10 Contacts (30 min | 2:05 - 2:35)

Use Apollo.io to search for these contacts. For each one, search by name + company.

**Priority contacts (from `MASTER-OUTREACH-READY.md` and `design-partner-prospecting-list.md`):**

| # | Name | Company | Role | File Reference |
|---|------|---------|------|----------------|
| 1 | Jasmine Bouchard | RUDSAK | Director eCommerce | `MASTER-OUTREACH-READY.md`, line 105 |
| 2 | Maxime Boyer | Groupe Dynamite | CDO | `MASTER-OUTREACH-READY.md`, line 130 |
| 3 | Gregoire Baret | ALDO Group | VP Consumer Experience | `MASTER-OUTREACH-READY.md`, line 12 |
| 4 | Kelly Cochrane | Mackage | Global Director eCommerce | `MASTER-OUTREACH-READY.md`, line 43 |
| 5 | Fadi Farha | SSENSE | VP Growth Marketing | `MASTER-OUTREACH-READY.md`, line 73 |
| 6 | Maxime Sincerny | Bofu Agence Marketing | Co-Founder | `MASTER-OUTREACH-READY.md`, line 245 |
| 7 | Maxence Pezzetta | My Little Big Web | Co-Founder | `MASTER-OUTREACH-READY.md`, line 250 |
| 8 | Paul Teitelman | Independent SEO | Consultant | `MASTER-OUTREACH-READY.md`, line 255 |
| 9 | Ian Bertrand | Moose Knuckles | VP Global Marketing | `design-partner-prospecting-list.md`, line 18 |
| 10 | Check LinkedIn | Frank And Oak | Head of E-Commerce | `design-partner-prospecting-list.md`, line 21 |

**Process for each (3 min per contact):**
1. Search Apollo.io by name + company
2. If found: save email, verify it with Apollo's built-in verification
3. If not found: try Hunter.io (https://hunter.io), search by domain
4. If still not found: try the pattern `firstname.lastname@companydomain.com` and verify with https://email-checker.net
5. Log the email (or "not found") in a spreadsheet

**If Apollo free tier limits you:** Use Snov.io (https://snov.io) as backup. Also referenced in `RESOURCES-LEAD-GEN.md`, line 57.

---

## Step 13: Queue Next Batch of Emails (20 min | 2:35 - 2:55)

For every contact where you found an email in Step 12:

1. Open the corresponding email template from `MASTER-OUTREACH-READY.md` (Priority 1 contacts) or `outreach-sequences.md` (for contacts not in the master file)
2. Personalize: replace any `{{variables}}` with real data
3. For agency contacts (Bofu, My Little Big Web, Paul Teitelman), use the messages from `MASTER-OUTREACH-READY.md`, lines 245-258
4. Save all personalized emails in a Google Doc titled "VisiMind Outreach Queue - April 2026"
5. Do NOT send more than 3 cold emails today. Save the rest for tomorrow and Friday.
6. Best send times from `outreach-sequences.md`: Tuesday 8:15 AM ET, Wednesday 7:45 AM ET, Thursday 8:00 AM ET. Tomorrow is Thursday, so schedule any sends for 8:00 AM ET.

**Which 3 to send today (if you have their emails):**
1. Jasmine Bouchard (RUDSAK) - warmest, already has llms.txt
2. Gregoire Baret (ALDO) - freshest migration timing
3. One agency contact (Bofu or My Little Big Web) - different category, tests a different angle

---

## Step 14: Decide on SocialNext Montreal Ticket (5 min | 2:55 - 3:00)

Reference: `MASTER-OUTREACH-READY.md`, line 264

- SocialNext Montreal is June 10-11, 2026
- Early bird discount expires April 10 (TOMORROW)
- $250 off the ticket price

**Decision framework:**
- Can you afford the ticket even with the discount? If yes, buy it. Conferences are where you meet 10+ contacts in one day.
- If the cost is a stretch, skip it. Your online outreach pipeline is strong enough without it.
- If you decide to go: buy the ticket today (before midnight April 10) at https://socialnext.com (or search for "SocialNext Montreal 2026 tickets")

---

## Step 15: Apply to One Quebec Funding Program (30 min | 3:00 - 3:30)

Reference: `MASTER-OUTREACH-READY.md`, line 267, and `french-outreach.md` for Quebec-specific funding details.

**Best option for a student founder:**

### PME MTL Fonds Jeunes Entreprises
- Up to $15,000 grant (non-dilutive, you keep 100% equity)
- Designed for young entrepreneurs in Montreal
- Website: https://pmemtl.com (search for "Fonds Jeunes Entreprises")

**What to prepare (you can do most of this in 30 min):**
1. Open the application page and read the eligibility criteria
2. Download the application form
3. Start filling in the basics: your name, VisiMind description, Montreal address, student status
4. For the "problem" section: use the opening paragraphs from any of your cold emails in `MASTER-OUTREACH-READY.md`. They describe the problem clearly.
5. For the "solution" section: describe VisiMind's core features (AI visibility audit, bilingual Fix Kits, Self-Consistency Mining)
6. You do NOT need to finish the application today. Just get it started. Finish and submit by end of week.

**Backup option:** BDC Data-to-AI Program (referenced in `MASTER-OUTREACH-READY.md`, line 267). This covers full costs but is more competitive. Apply to both if eligible.

---

# END OF DAY (15 min, 3:30 - 3:45 PM)

---

## Step 16: Log Everything in a CRM Spreadsheet (10 min)

Create a Google Sheet titled "VisiMind Outreach CRM" with these columns:

| Contact Name | Company | Channel | Message Sent | Date | Status | Next Action | File Reference |
|---|---|---|---|---|---|---|---|

Log every touch from today:
- 3 LinkedIn connection requests (Step 3)
- 1-2 Shopify Community replies (Steps 4 and 6)
- 2-3 Indie Hackers / Shopify replies (Step 9)
- 3 Twitter/X DMs (Step 10)
- Any cold emails sent (Steps 5 and 13)

**Target for today: 10-15 touches total.**

If you want a more robust CRM later, reference `RESOURCES-LEAD-GEN.md`, Section 2, "Open Source CRMs" (lines 66-73). Twenty (https://twenty.com) is recommended for solo founders.

---

## Step 17: Plan Day 2 (5 min)

**Day 2 priorities (Friday, April 10):**
1. Check for responses to today's outreach (LinkedIn, Shopify Community, Indie Hackers, Twitter, email)
2. Send 3 more cold emails from the queue built in Step 13 (use Thursday 8:00 AM send time from `outreach-sequences.md`)
3. Send 2 more LinkedIn connection requests (Jasmine Bouchard at RUDSAK, Maxime Boyer at Dynamite, once you find their profiles)
4. Post 1 more Shopify Community reply (pick ScentedAromas from `MASTER-OUTREACH-READY.md`, lines 179-183)
5. Reply to any Indie Hackers or Reddit threads where people responded to your Day 1 posts
6. Start the French outreach: send 1 French email using templates from `french-outreach.md`, Sequence 1 or Sequence 2
7. Submit the PME MTL funding application if started in Step 15
8. Buy SocialNext ticket if decided in Step 14 (deadline is today)

---

# DAILY OUTREACH CADENCE (Ongoing After Day 1)

| Channel | Daily Target | File Reference |
|---------|-------------|----------------|
| LinkedIn connection requests | 2-3 | `linkedin-outreach-playbook.md`, Part 2 |
| Cold emails (EN) | 2-3 | `outreach-sequences.md` + `MASTER-OUTREACH-READY.md` |
| Cold emails (FR) | 1 | `french-outreach.md`, Partie 1 |
| Shopify Community replies | 1-2 | `MASTER-OUTREACH-READY.md`, Shopify section |
| Indie Hackers / Reddit replies | 1-2 | `MASTER-OUTREACH-READY.md`, Indie Hackers section + `reddit-outreach-targets.md` |
| Twitter/X engagement | 2-3 likes/replies + 1 DM | `TWITTER_OUTREACH_STRATEGY.md` |
| Community posts | 1 per week | Various community forums |

**Weekly target: 50-75 outreach touches.**
**Monthly target: 200-300 touches, aiming for 5-10 warm conversations and 2-3 design partner commitments.**

---

# QUICK REFERENCE: ALL FILES AND WHAT IS IN THEM

| File | Contents | When You Need It |
|------|----------|-----------------|
| `MASTER-OUTREACH-READY.md` | 5 personalized brand emails, 8 community reply messages, 7 thought leader messages, 3 agency messages, time-sensitive actions | Every day |
| `outreach-sequences.md` | 5 email sequences x 3 emails each (15 templates total) with follow-up timing | When sending follow-ups on Day 3, Day 6, Day 7 |
| `outreach-queue.md` | Generic templates for Reddit, LinkedIn, Twitter, email (5 each) | When you need a template for a new contact not in the master file |
| `linkedin-outreach-playbook.md` | 18 target roles, 5 connection request variants, 5 follow-up variants, LinkedIn group strategy | For all LinkedIn outreach |
| `TWITTER_OUTREACH_STRATEGY.md` | 18 real Twitter accounts, 5 DM templates, content strategy | For all Twitter/X outreach |
| `reddit-outreach-targets.md` | 15 pain-point patterns from Reddit/Shopify forums with suggested DMs | When prospecting on Reddit |
| `french-outreach.md` | French email sequences, LinkedIn messages, Quebec communities, funding sources | When reaching out to francophone contacts |
| `design-partner-prospecting-list.md` | 24 Montreal brands + 17 Canadian brands + 14 agencies with details | When you need new targets beyond the top 5 |
| `brand-audit-results.md` | Technical audit scores for 8 brand websites | When personalizing emails with specific findings |
| `earned-media-outreach-strategy.md` | 18 podcast targets, PR pitches, conference strategy | Week 2+ when you start earned media |
| `RESOURCES-LEAD-GEN.md` | Tools (Apollo, Hunter, CRMs), MCP servers, automation workflows | When setting up tools and infrastructure |
| `geo-thought-leaders.md` | 35 GEO/AEO thought leaders with handles and pre-written messages | When expanding thought leader outreach |

---

**Remember:** You have 91 contacts, 18 files of materials, and personalized messages ready. The hard work is done. Tomorrow is about pressing "send" and showing up in conversations. Do not overthink. Do not rewrite. Execute.**
