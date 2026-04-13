# VisiMind Scary Report Templates
## Lead Magnet & Outreach Toolkit

---

# TEMPLATE 1: "The AI Visibility Audit" (1-Page PDF)

## Structure

### Header Bar
- VisiMind logo (left)
- "AI VISIBILITY AUDIT" in caps, bold
- Brand logo + name (right)
- Date of audit
- Confidential / Prepared exclusively for [Brand Name]

### Section 1: Inference Alignment Score (Hero Metric)
> The Inference Alignment Score measures how accurately AI systems represent your brand across languages, using methodology adapted from GEO visibility research (Princeton, 2024).
Large circular gauge, 0-100, color-coded:
- 0-30: Red ("Invisible")
- 31-55: Orange ("At Risk")
- 56-75: Yellow ("Underperforming")
- 76-100: Green ("Optimized")

**Example for Mackage:**
> **Inference Alignment Score: 34 / 100**
> Your brand is functionally invisible in 2 of 3 major AI engines.
> When consumers ask AI to recommend luxury outerwear, Mackage appears in only 1 out of 6 tested queries.

### Section 2: LLM Response Matrix (3-Column Table)

| Query: "Best luxury winter coat Canada" | ChatGPT | Perplexity | Google AI |
|----------------------------------------|---------|------------|-----------|
| Mackage mentioned?                     | No      | No         | Yes (3rd) |
| Position                               | --      | --         | #3        |
| Competitors mentioned instead          | Canada Goose, Moose Knuckles, Nobis | Canada Goose, Moose Knuckles, Arc'teryx | Canada Goose, Moose Knuckles |
| Key attributes cited                   | --      | --         | "Montreal-based" only |
| Product-level detail                   | --      | --         | None (no model names, no specs) |

### Section 3: Bilingual Decay Panel (Side-by-Side)

**Left column (English):**
> Query: "Best luxury down jacket for extreme cold"
> ChatGPT response: "Canada Goose Expedition Parka... Moose Knuckles 3Q..."
> **Mackage: NOT MENTIONED**

**Right column (French):**
> Query: "Meilleur manteau de duvet de luxe pour le froid extreme"
> ChatGPT response: "Canada Goose... Kanuk..."
> **Mackage: NOT MENTIONED**
> Token Fertility: FR description uses 1.73x more tokens than EN -- the AI literally reads your French content 73% less efficiently.

Visual: A red "decay arrow" showing the fertility gap. FR column has a faded/degraded visual treatment to convey signal loss.

### Section 4: Signal Gaps Found (Bullet List with Icons)

- **CRITICAL** -- "800-fill power" and "RDS Certified" never appear in any AI response about Mackage. Your key differentiators are invisible.
- **CRITICAL** -- No AI engine cites mackage.com as a source. They cite retailers (Nordstrom, SSENSE) instead. You have zero citation authority.
- **WARNING** -- French product descriptions tokenize into 38% more fragments. The AI reconstructs "duvet d'oie de facteur de gonflement 800" as 11 tokens vs. 6 for the English equivalent. Semantic signal decays at every fragment boundary.
- **WARNING** -- No structured data (JSON-LD) detected on product pages. AI engines cannot extract specs programmatically.

### Section 5: Competitor Benchmark (Mini-Table)

| Brand           | AI Mention Rate | Avg Position | Citation Authority | Structured Data |
|-----------------|----------------|--------------|-------------------|-----------------|
| Canada Goose    | 6/6 queries    | #1           | Brand.com cited   | Yes (Schema.org)|
| Moose Knuckles  | 4/6 queries    | #2           | Brand.com cited   | Yes             |
| **Mackage**     | **1/6 queries**| **#3**       | **Not cited**     | **No**          |

### Section 6: CTA Block

> **Your competitors are being recommended. You are not.**
> VisiMind fixes this in 14 days.
>
> [BOOK YOUR FIX CALL] -- 20-minute session. We show you exactly what to change.
>
> Or reply to this email -- I will send you the full 12-page technical breakdown.

## Design Notes
- **Colors:** Dark navy background (#0B1120), white text, red/amber for danger metrics, green only for competitor scores (to sting).
- **Typography:** Inter or DM Sans. Score number in 72pt bold.
- **Layout:** Single page, portrait, dense but scannable. Every metric should hit in under 5 seconds of scanning.
- **File format:** PDF, also embeddable as an image in email body.

## Personalization
- Brand name, logo, product category inserted dynamically.
- LLM queries customized to brand's actual product category (outerwear, footwear, fashion platform).
- Competitor set pulled from seed data or manually curated per vertical.
- Signal gaps generated from actual VisiMind probe data (inference_lab.py + bilingual_bridge.py).

## Follow-Up Strategy
- Day 0: Send PDF via email + LinkedIn DM with a single-line hook.
- Day 2: Follow up with "Did you see the French decay number? That one surprised us too."
- Day 5: Send Template 3 (video) if no response.
- Day 10: Send Template 2 (technical deep dive) if the prospect opened but did not reply.

---

# TEMPLATE 2: "The Bilingual Probe Results" (Technical Deep Dive)

## Structure (2-3 Pages)

### Page 1: Token Fertility Analysis

**Header:** "Why AI Engines Read Your French Content 73% Less Efficiently"

**Visualization: Token Fragmentation Heatmap**
Show the actual French product description with each word color-coded by token count:
- 1 token = white (normal)
- 2 tokens = light yellow
- 3+ tokens = red (fragmented / "Scrabble-tiled")

**Example for Mackage Lena Down Jacket:**

EN: `"800-fill power responsibly-sourced goose down, rated to -30C"`
- Tokens: `["800", "-fill", " power", " respons", "ibly", "-sourced", " goose", " down"]` = 8 tokens, 7 words
- Fertility: **1.14** (healthy)

FR: `"Duvet d'oie de facteur de gonflement 800, resistant jusqu'a -30C"`
- Tokens: `["Du", "vet", " d", "'", "o", "ie", " de", " fact", "eur", " de", " g", "onf", "lement"]` = 13 tokens, 8 words
- Fertility: **1.63** (degraded)

**The Scrabble Problem:** The tokenizer literally tiles "gonflement" into 3 pieces. Each fragment boundary is a point where semantic meaning can be lost or hallucinated.

### Page 2: Self-Consistency & Contradiction Analysis

**Header:** "How Often AI Contradicts Itself About Your Brand"

**Self-Consistency Score Table:**

| Query (asked 5 times each)                        | Consistency Score | Contradictions Found |
|---------------------------------------------------|-------------------|---------------------|
| "Is Mackage a luxury brand?"                      | 3/5 (60%)         | 2x called "premium" not "luxury" |
| "What is Mackage's warmest jacket?"               | 2/5 (40%)         | 3x cited wrong model or no model |
| "Is Mackage ethical/sustainable?"                  | 1/5 (20%)         | 4x omitted RDS certification     |
| "Quel est le meilleur manteau Mackage?" (FR)      | 1/5 (20%)         | 4x defaulted to generic answer   |

**Methodology Note:**
> We probe each LLM 5 times at temperature=0.7 (VisiMind's Golden Set protocol). A consistency score below 60% means the AI has no stable representation of your brand -- it is guessing.

**Contradiction Rate:**
> **Overall: 65% contradiction rate**
> In 13 out of 20 probes, the AI either omitted key facts, cited incorrect specs, or gave conflicting answers about your products. This is not a branding problem. This is a data infrastructure problem.

### Page 3: Knowledge Graph Gap Analysis

**Header:** "What AI Knows vs. What It Should Know"

**Visual: Two-Column Knowledge Graph**

Left: "What AI currently knows about Mackage"
- Mackage -> is_a -> "outerwear brand" (low confidence)
- Mackage -> located_in -> "Canada" (medium confidence)
- Mackage -> sells -> "coats" (low confidence)

Right: "What AI should know"
- Mackage -> is_a -> "luxury outerwear brand" (with price-point proof)
- Mackage -> headquartered_in -> "Montreal, QC" (with address)
- Mackage -> signature_product -> "Lena Down Jacket" (with specs)
- Mackage Lena -> thermal_rating -> "-30C" (with certification)
- Mackage Lena -> fill_power -> "800-fill" (with RDS certification)
- Mackage -> certification -> "RDS Certified, Bluesign Approved"
- Mackage -> price_range -> "$990-$1,150 CAD"

**Gap count: 14 missing triples** that competitors have filled.

### CTA Block

> **Your knowledge graph has 14 gaps. Your competitors have zero.**
> VisiMind builds the missing triples, injects bilingual structured data, and verifies uptake across all 3 engines.
>
> [SEE THE 14-DAY FIX PLAN] -- Personalized for Mackage's product catalog.

## Design Notes
- **Colors:** White background, dark text, code blocks in monospace with subtle gray backgrounds.
- **Typography:** Monospace for token breakdowns (JetBrains Mono). Sans-serif for everything else.
- **Layout:** More "technical report" feel. Numbered sections, clear data tables.
- **Audience:** This goes to the head of digital / e-commerce / SEO team, not the CMO.

## Personalization
- Token fertility computed live per brand using bilingual_bridge.py's `calculate_fertility()` and `compare_fertility()` functions.
- Self-consistency scores from actual Golden Set probes (inference_lab.py).
- Knowledge graph gaps generated from the delta between `kg_triples` in the DB and the full product PIM data.

## Follow-Up Strategy
- Only send after the prospect has engaged with Template 1.
- Frame as: "You mentioned wanting to understand the technical side -- here is the full probe data."
- CTA leads to a live demo (Template 5).

---

# TEMPLATE 3: "The 30-Second Video Script" (Loom-Style)

## Script (Under 60 Seconds)

```
[SCREEN: ChatGPT open in browser. Cursor visible.]

VOICEOVER (founder, conversational tone):

"Hey [First Name] -- quick 30-second thing I wanted to show you.

[TYPES into ChatGPT: "What are the best luxury winter coats from Canadian brands?"]

So I just asked ChatGPT to recommend luxury Canadian outerwear.

[RESPONSE LOADS. Canada Goose, Moose Knuckles, Nobis, Kanuk appear. No Mackage.]

Canada Goose... Moose Knuckles... Nobis... no Mackage anywhere.

[SCROLLS DOWN to confirm.]

Not mentioned. Not even as an also-ran.

Now watch what happens in French:

[TYPES: "Quels sont les meilleurs manteaux d'hiver de luxe canadiens?"]

[RESPONSE LOADS. Still no Mackage.]

Same thing. Actually worse -- it didn't even get the category right in French.

[SWITCHES TO BROWSER TAB showing a quick bar chart: "Mackage: 1/6 queries. Canada Goose: 6/6."]

We ran this across ChatGPT, Perplexity, and Google AI. Mackage showed up in 1 out of 6 queries. Canada Goose? Six for six.

The fix is actually straightforward. It is a data structure problem, not a brand awareness problem. We have fixed this for [similar brand] in 14 days.

I made a one-page report for you -- it shows exactly where the gaps are. Want me to send it over?

[SCREEN: Shows the Template 1 PDF briefly.]

Just reply to this message. Takes 20 minutes to walk through."
```

## Timing Breakdown
- 0:00-0:05 -- Hook ("quick 30-second thing")
- 0:05-0:15 -- English query demo (the scare)
- 0:15-0:25 -- French query demo (the twist)
- 0:25-0:40 -- Data summary (the proof)
- 0:40-0:55 -- The reframe + CTA

## Design Notes
- **Recording:** Loom, clean desktop, dark mode browser.
- **Thumbnail:** Screenshot of ChatGPT response with a red circle around where the brand should be but is not. Text overlay: "Where is [Brand]?"
- **Length:** Target 45 seconds. Never exceed 60.
- **Tone:** Not salesy. Genuinely curious, slightly surprised. "Huh, that is interesting" energy.

## Personalization
- Record a fresh video for each prospect (or each vertical batch).
- Use the prospect's exact product category in the query.
- If possible, show a competitor from the prospect's actual competitive set.
- For SSENSE: "What is the best place to buy designer fashion online in Canada?"
- For Aldo: "What are the most sustainable shoe brands?"

## Follow-Up Strategy
- Send via LinkedIn DM or email with subject: "Found something weird about [Brand] + ChatGPT"
- If opened but no reply in 48h, send the Template 1 PDF.
- If replied, book the 20-minute call immediately.

---

# TEMPLATE 4: "The Twitter/X Thread Template"

## Thread (7 Tweets)

### Tweet 1 (Hook)
```
I asked ChatGPT, Perplexity, and Google AI to recommend luxury Canadian outerwear.

Canada Goose was mentioned every time.
Moose Knuckles was mentioned 4/6 times.
Mackage? Once. In last place.

Mackage is a $500M+ brand. AI does not know it exists.

Here is why (and what it means for your brand): [thread emoji]
```

### Tweet 2 (The Bilingual AI Gap)
```
Canada has a hidden AI problem that nobody is talking about:

French content gets tokenized 40-70% less efficiently than English.

The word "gonflement" (fill power) gets split into 3 tokens.
The English "fill-power" is 2 tokens.

Every extra token = less semantic signal = worse AI recommendations.
```

### Tweet 3 (Real Example -- SSENSE)
```
I asked: "Where should I buy designer fashion online in Canada?"

ChatGPT recommended: Farfetch, Net-a-Porter, MatchesFashion.

SSENSE -- literally headquartered in Montreal, 350+ designer brands -- was not mentioned.

A Montreal-born platform losing to European competitors on a Canadian query.
```

### Tweet 4 (Real Example -- Aldo)
```
Aldo has been carbon-neutral since 2024. LWG Gold certified. Recycled leather products.

I asked AI: "What are the most sustainable shoe brands?"

Aldo? Nowhere.
Allbirds, Veja, and Nisolo took every slot.

The sustainability data exists. AI just cannot find it.
```

### Tweet 5 (The Root Cause)
```
This is NOT a brand awareness problem. All 3 brands have massive consumer recognition.

The root cause:
- No structured data (JSON-LD) on product pages
- No bilingual knowledge graph
- French product descriptions fragment into semantic noise
- AI citations point to retailers, not brand.com

The brand loses control of its own narrative.
```

### Tweet 6 (The Fix Preview)
```
The fix is boring but effective:

1. Inject bilingual JSON-LD structured data
2. Build a product knowledge graph with verified triples
3. Fix French tokenization (semantic compression)
4. Establish citation authority (brand.com as primary source)

We measured: 14 days from "invisible" to "recommended."
```

### Tweet 7 (CTA)
```
We built a free audit that runs your brand through the same test.

It shows:
- Your Inference Alignment Score (how visible you are to AI)
- English vs French decay rate
- Which competitors are beating you and why
- The specific data gaps to fix

DM me your brand name. I will send it.
```

## Design Notes
- **Images:** Each tweet should have a visual. Tweet 1: bar chart. Tweet 2: token fragmentation heatmap. Tweets 3-4: screenshots of actual AI responses. Tweet 5: diagram. Tweet 6: before/after. Tweet 7: preview of the audit PDF.
- **Colors for graphics:** Dark background, VisiMind teal (#00D4AA) for highlights, red for danger metrics. Consistent visual language across all images.
- **Timing:** Post Tweet 1 at peak hours (9am ET or 12pm ET). Reply-chain the rest over 15 minutes.

## Personalization
- Swap brand examples based on the vertical you are targeting that week.
- For fashion: Mackage / SSENSE examples.
- For footwear: Aldo examples.
- For beauty: Substitute with relevant Canadian luxury beauty brands.
- Always keep the bilingual angle -- it is the unique hook that no one else is talking about.

## Follow-Up Strategy
- Pin Tweet 1 to profile.
- When someone DMs their brand name, run the actual VisiMind probe and send Template 1 within 24 hours.
- Quote-tweet the thread weekly with a new brand example from fresh probes.
- Turn high-engagement replies into case study threads later.

---

# TEMPLATE 5: "The Interactive Demo Pitch" (5-Minute Live Flow)

## Demo Flow

### Minute 0:00-0:30 -- Hook
**Script:** "I am going to show you something in real-time. This is not a deck -- this is your actual data. Type your brand name."

**Screen:** VisiMind dashboard, brand selector visible. Prospect types or selects their brand.

### Minute 0:30-1:30 -- The Scare (Inference Alignment Score)
**Screen:** Dashboard loads. The Inference Alignment Score gauge animates from 0 to their actual score (e.g., 34/100).

**Script:** "That number -- 34 -- means that when someone asks AI to recommend [their category], your brand appears in about 1 out of 6 queries. Your competitor [competitor name] scores 78. Let me show you what that looks like."

**Action:** Click into the Signal Gaps view. Show the actual LLM responses side-by-side.

### Minute 1:30-2:30 -- The Bilingual Twist
**Screen:** Navigate to the Montreal Moat / Bilingual Bridge panel.

**Script:** "Now here is the part that is unique to Canadian brands. Watch what happens when we run the same query in French."

**Action:** Show the token fertility comparison. EN fertility: 1.14. FR fertility: 1.63.

**Script:** "Your French product descriptions use 43% more tokens. The AI is literally processing 43% more noise to extract the same meaning. That is why your French visibility drops -- look at this chart."

**Screen:** Show the EN vs FR alignment trend chart from the dashboard.

### Minute 2:30-3:30 -- The Knowledge Graph Gap
**Screen:** Navigate to the KG stats view (Verify > KG).

**Script:** "This is what AI currently knows about your brand. [Show sparse graph.] And this is what it should know. [Show full graph with missing triples highlighted in red.] Those red nodes are gaps -- facts about your products that exist in your PIM but that AI engines cannot access. Your competitors have filled these gaps. You have not."

**Action:** Show the competitor benchmark from Template 1 data.

### Minute 3:30-4:30 -- The Fix (E-Score Roadmap)
**Screen:** Navigate to the EEE Roadmap panel.

**Script:** "Here is the roadmap. We take your E-Score from where it is now to 1.4 -- that is the threshold where AI engines consistently recommend you. It takes 14 days. Week 1 is structured data injection. Week 2 is bilingual knowledge graph and citation authority. Week 3 is verification -- we re-probe all three engines and confirm uptake."

**Action:** Show the RAFT cadence schedule with cycle dates.

### Minute 4:30-5:00 -- The Close
**Script:** "The audit you just saw is free. The full fix is what we charge for. But here is the thing -- every day you wait, your competitors are getting recommended and you are not. That is real revenue going to Canada Goose instead of to you. Can we schedule a 30-minute deep dive this week to walk through the fix plan?"

**Action:** Show the CTA screen with calendar booking link.

## Screen Flow Summary
1. Brand selector (prospect types name)
2. Inference Alignment Score (big scary number)
3. LLM Response Matrix (they are not there)
4. Bilingual Tokenization Premium (the twist)
5. Knowledge Graph Gaps (the technical proof)
6. E-Score Roadmap (the fix)
7. Booking CTA

## Design Notes
- **The dashboard must be real.** No mockups. Pull live data from the VisiMind backend via the existing API endpoints.
- **Animation matters.** The score gauge should animate. The token heatmap should highlight in sequence. Movement holds attention.
- **Dark mode.** Navy/black background, teal accents, red for danger. The aesthetic should feel like a mission control center, not a marketing dashboard.
- **Prospect's brand in the header at all times.** Make it feel custom-built for them.

## API Endpoints Used in Demo
- `/api/dashboard/metrics?brand_id={id}` -- Inference Alignment Score
- `/api/dashboard/alerts?brand_id={id}` -- Signal Gaps
- `/api/dashboard/trend` -- EN/FR alignment trend
- `/api/eee/moat?brand_id={id}` -- Montreal Moat bilingual split
- `/api/verify/kg?brand_id={id}` -- Knowledge Graph stats
- `/api/eee/roadmap?brand_id={id}` -- E-Score roadmap
- `/api/verify/efficiency` -- E-Score breakdown
- `/api/verify/raft?brand_id={id}` -- RAFT cadence

## Personalization
- Pre-load the prospect's brand into the database before the demo.
- Run probes 24 hours before the call so real data populates.
- If the brand is not in the seed data, use the DataIngester (Connect page) to import their product catalog from Shopify/PIM before the demo.
- Have 2-3 competitors pre-loaded for comparison.

## Follow-Up Strategy
- Record the demo with Loom during the call (ask permission).
- Send the recording + Template 1 PDF + Template 2 technical report within 2 hours of the call.
- Subject line: "Your AI Visibility Audit + the recording from today"
- Follow up at Day 3 with a proposal if they showed buying signals.

---

# CROSS-TEMPLATE STRATEGY

## Outreach Sequence (Cold Prospect)

| Day | Action | Template |
|-----|--------|----------|
| 0   | LinkedIn connect request + 1 line hook | -- |
| 1   | Send Video (Template 3) via LinkedIn DM | T3 |
| 3   | If opened: Send 1-page audit (Template 1) via email | T1 |
| 5   | If no reply: Follow up on the bilingual number | -- |
| 7   | If opened T1: Send technical deep dive (Template 2) | T2 |
| 10  | Offer live demo (Template 5) | T5 |
| 14  | Final follow-up: "Your competitor just signed up" | -- |

## Outreach Sequence (Warm / Inbound via Thread)

| Day | Action | Template |
|-----|--------|----------|
| 0   | They DM from the thread (Template 4) | T4 |
| 0   | Send 1-page audit within 24h | T1 |
| 1   | If opened: Send video walkthrough | T3 |
| 2   | Offer live demo | T5 |
| 3   | Send technical deep dive before the demo | T2 |

## Key Metrics to Track
- **Template 1:** Open rate, time spent on PDF (use a tracked link), reply rate
- **Template 2:** Only track if sent after T1 engagement; measure demo booking rate
- **Template 3:** Video view rate, watch completion %, reply rate
- **Template 4:** Impressions, DMs received, thread saves/bookmarks
- **Template 5:** Demo completion rate, proposal sent rate, close rate

## Tone Guidelines
- **Scary but honest.** Every number must be real and reproducible. Never fabricate probe results.
- **Clinical, not aggressive.** Frame as "we found something interesting" not "you are failing."
- **Technical credibility.** Use real terminology (token fertility, self-consistency, knowledge triples) but always explain it in one plain sentence.
- **Urgency without manipulation.** The urgency is real -- every day without AI visibility is a day competitors capture the recommendation. State the fact without inflating it.

## Brand Voice for All Templates
- First person singular (founder voice)
- Short sentences
- No exclamation marks
- Data first, opinion second
- Always end with a specific, low-commitment CTA (reply, DM, 20-minute call)
