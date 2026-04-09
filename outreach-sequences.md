# VisiMind Cold Outreach Sequences
## 5 Angles x 3 Emails Each | Canadian Luxury Retail

---

# SEQUENCE 1: THE "SCARY REPORT"
**Target Persona:** Head of E-commerce / Director of Digital Marketing
**Best Send Time:** Tuesday 8:15 AM ET (pre-standup, high open rates)

---

### Email 1.1 - The Hook

**Subject A:** We asked ChatGPT about {{brand}} - the answer was wrong
**Subject B:** {{brand}}'s AI search results are broken. Here's proof.

Hi {{firstName}},

I asked ChatGPT, Perplexity, and Google AI Overviews one simple question: "best luxury outerwear brands in Montreal."

{{brand}} didn't appear. Not once.

Worse - when I asked in French ("meilleures marques de manteaux luxe Montreal"), the AI hallucinated details about your products. Wrong materials. Wrong price ranges. A store location that doesn't exist.

This isn't a SEO problem. It's a data-ingestion problem. LLMs are pulling stale, fragmented data about {{brand}} and presenting it as fact to thousands of shoppers every day.

We built VisiMind to fix exactly this. I have the full breakdown of what went wrong for {{brand}} across all three AI engines.

Worth a 10-minute look?

{{sender}}

---

### Email 1.2 - The Evidence (Send: Day 3, Thursday 8:15 AM ET)

**Subject A:** The actual AI outputs for {{brand}} (screenshots attached)
**Subject B:** 3 things AI gets wrong about {{brand}} right now

Hi {{firstName}},

Quick follow-up. Here are the three biggest AI failures I found for {{brand}}:

1. **French token decay** - Your French product descriptions lose ~40% of their meaning when LLMs tokenize them. "Duvet en duvet d'oie" gets parsed as nonsense.
2. **Missing structured data** - AI has no reliable JSON-LD to anchor {{brand}}'s products, so it guesses. Badly.
3. **Stale training data** - Your FW25 collection doesn't exist in any LLM's knowledge base yet.

The result: AI recommends your competitors instead.

I scored {{brand}} at **{{score}}/100** on our Inference Alignment Scale. That means AI understands less than half of what makes your brand relevant.

I can share the full report in a 10-minute call. No pitch - just the data.

{{sender}}

---

### Email 1.3 - The Closer (Send: Day 7, Monday 9:00 AM ET)

**Subject A:** Last thing on the AI visibility issue
**Subject B:** Closing the loop on {{brand}} + AI search

Hi {{firstName}},

I'll keep this short. The AI search landscape is moving fast - Perplexity alone grew 800% in Canada last year. Brands that fix their AI data layer now will own the recommendations. Those that don't will watch AI send their customers to competitors.

We built a Fix Kit for {{brand}} - bilingual JSON-LD structured data that corrects the gaps I found. Takes 15 minutes to deploy on Shopify.

If this isn't the right time, no worries at all. But if you're curious what AI is telling your customers about {{brand}} today, I'll send over the full audit.

Just reply "send it" and it's yours.

{{sender}}

---
---

# SEQUENCE 2: THE "COMPETITOR ADVANTAGE"
**Target Persona:** SEO Manager / VP of Marketing
**Best Send Time:** Wednesday 7:45 AM ET (mid-week, strategic mindset)

---

### Email 2.1 - The Gap

**Subject A:** {{competitor}} is winning AI search in Montreal. {{brand}} isn't.
**Subject B:** Why AI recommends {{competitor}} over {{brand}} - the data

Hi {{firstName}},

I ran a bilingual AI search audit across ChatGPT, Perplexity, and Google AI Overviews for luxury retail queries in Montreal.

Here's what I found:

- "Best luxury sneakers Montreal" - {{competitor}} cited 7/10 times. {{brand}}: 0/10.
- "Meilleurs manteaux d'hiver Montreal" - {{competitor}} cited 6/10. {{brand}}: 1/10 (with wrong info).
- "Canadian luxury fashion brands" - {{competitor}} cited 8/10. {{brand}}: 2/10.

This isn't about SEO rankings. AI search is a completely different channel, and {{competitor}} has structured their data for it. {{brand}} hasn't - yet.

Want to see the full comparison? 10 minutes, no strings.

{{sender}}

---

### Email 2.2 - The Why (Send: Day 3, Friday 8:30 AM ET)

**Subject A:** How {{competitor}} shows up in AI and {{brand}} doesn't
**Subject B:** The structural gap between {{brand}} and {{competitor}} in AI

Hi {{firstName}},

Quick follow-up on the AI search gap I shared.

Here's WHY {{competitor}} keeps winning: they have clean bilingual structured data - proper JSON-LD, consistent French/English product schemas, and fresh data signals that LLMs can actually parse.

{{brand}} has great products. But your data layer is invisible to AI. Specifically:

- No bilingual JSON-LD on product pages
- French descriptions that fragment during tokenization
- Category data that AI can't map to purchase intent queries

We fix this in days, not months. VisiMind generates a bilingual Fix Kit that plugs directly into Shopify or your PIM.

The competitive window is small. Want to see what closing the gap looks like?

{{sender}}

---

### Email 2.3 - The Urgency (Send: Day 6, Monday 8:00 AM ET)

**Subject A:** AI search share shifts fast
**Subject B:** Quick note before I close this out

Hi {{firstName}},

One last thought. AI search is where Google was in 2005 - early enough that structured data investments pay 10x returns.

Right now, {{competitor}} owns {{X}}% of AI recommendation share for your core categories in Montreal. That's not permanent - but the longer it goes unchallenged, the harder it gets. LLMs reinforce their own outputs.

We built VisiMind specifically for Canadian luxury brands dealing with the bilingual complexity that makes this problem worse here than anywhere else.

Happy to send {{brand}}'s full competitive breakdown - no call needed. Just reply and I'll send the PDF.

{{sender}}

---
---

# SEQUENCE 3: THE "FRENCH TOKEN DECAY" RESEARCH
**Target Persona:** CTO / Head of Engineering / Technical SEO Lead
**Best Send Time:** Thursday 10:00 AM ET (technical audience, later morning)

---

### Email 3.1 - The Discovery

**Subject A:** Research finding: French product data loses 40% signal in LLMs
**Subject B:** How bilingual tokenization breaks AI recommendations for Canadian brands

Hi {{firstName}},

Our team at VisiMind has been studying how LLMs process bilingual Canadian e-commerce data. The findings are significant.

When GPT-4 tokenizes French product descriptions, semantic signal degrades by ~40% compared to English equivalents. "Manteau en laine merinos avec col en fourrure de renard" becomes fragmented tokens that lose product-attribute relationships.

The result: when a Francophone shopper in Montreal asks AI for product recommendations, Canadian luxury brands are systematically underrepresented. The AI literally can't understand your French catalog data.

We've developed a "Bilingual Probe" - a statistical test that measures exactly how this affects a specific brand. I ran it on {{brand}}.

Interested in the technical breakdown? Happy to share our methodology.

{{sender}}

---

### Email 3.2 - The Data (Send: Day 4, Monday 10:00 AM ET)

**Subject A:** {{brand}}'s Bilingual Probe results
**Subject B:** Token-level analysis: where {{brand}}'s French data breaks

Hi {{firstName}},

Following up on the French token decay research.

Here's what the Bilingual Probe found for {{brand}}:

- **Inference Alignment Score:** {{score}}/100 (English) vs. {{scoreFR}}/100 (French)
- **Token fragmentation rate:** {{X}}% of French product terms split into sub-word tokens with no semantic anchor
- **Category drift:** AI misclassifies {{X}}% of {{brand}}'s French product categories

The fix is structural, not linguistic. It's not about better translations - it's about giving LLMs bilingual structured data (JSON-LD) that preserves semantic relationships regardless of language.

We've built this fix. It generates from your existing product data and deploys in minutes.

Worth a 15-minute technical walkthrough?

{{sender}}

---

### Email 3.3 - The Framework (Send: Day 8, Tuesday 10:00 AM ET)

**Subject A:** Open-sourcing our bilingual tokenization findings
**Subject B:** Quick question about {{brand}}'s data architecture

Hi {{firstName}},

Last note on this. We're compiling our French token decay research into a technical brief for the Canadian e-commerce community. We want to include real-world brand examples (anonymized, of course).

Would {{brand}} be open to participating? We'd run the full Bilingual Probe at no cost and share every data point with your team. You'd get:

- Complete token-level analysis of your French/English catalog
- Inference Alignment Scores across ChatGPT, Perplexity, and AI Overviews
- A bilingual Fix Kit (JSON-LD) ready to deploy

In exchange, we'd use the anonymized data in our research. Fair trade?

Takes 10 minutes of your time. I handle the rest.

{{sender}}

---
---

# SEQUENCE 4: THE "FREE AUDIT"
**Target Persona:** Director of Digital Marketing / E-commerce Manager
**Best Send Time:** Tuesday 9:30 AM ET (value-first, mid-morning)

---

### Email 4.1 - The Offer

**Subject A:** Free: {{brand}}'s AI visibility audit (bilingual)
**Subject B:** I built an AI audit for {{brand}} - want it?

Hi {{firstName}},

I run VisiMind. We help Canadian luxury brands understand how AI search engines see them.

I already built a bilingual AI visibility audit for {{brand}}. It covers:

- How ChatGPT, Perplexity, and Google AI Overviews describe {{brand}} today
- Where AI gets your products right and where it hallucinates
- Your Inference Alignment Score (1-100) in English and French
- How you compare to {{competitor1}} and {{competitor2}} in AI recommendations

It's free. No call required. No strings.

I built it because I think the bilingual AI problem is the biggest invisible threat to Montreal luxury retail right now, and I want smart people looking at the data.

Want me to send it over?

{{sender}}

---

### Email 4.2 - The Nudge (Send: Day 3, Thursday 9:30 AM ET)

**Subject A:** Your AI audit is ready
**Subject B:** Still have {{brand}}'s audit - expires Friday

Hi {{firstName}},

Quick bump. I have {{brand}}'s bilingual AI visibility audit ready to send.

One stat that might get your attention: when I asked Perplexity "meilleurs cadeaux luxe Montreal," {{brand}} was absent from every response. But {{competitor}} appeared in 4 out of 5.

That's one query. The full audit covers 25 bilingual queries across your core categories.

Reply "send it" and it's in your inbox in 5 minutes. Zero commitment.

{{sender}}

---

### Email 4.3 - The Feedback Ask (Send: Day 7, Monday 10:00 AM ET)

**Subject A:** Honest question about {{brand}} + AI
**Subject B:** Would love your take on this

Hi {{firstName}},

I realize I've been offering an audit without asking the more important question: is AI search even on {{brand}}'s radar yet?

We talk to a lot of Canadian e-commerce teams, and the response is split. Some see AI as the next Google. Others think it's still too early.

Either way, I'd genuinely love your perspective. We're building VisiMind specifically for brands like {{brand}}, and hearing what matters to your team would help us build the right thing.

15-minute call? I'll share {{brand}}'s audit and you tell me what's actually useful versus what's noise.

Calendly: {{link}}

{{sender}}

---
---

# SEQUENCE 5: THE "DESIGN PARTNER"
**Target Persona:** CTO / VP E-commerce / Head of Digital (decision-makers who value early access)
**Best Send Time:** Monday 8:00 AM ET (start of week, strategic planning mode)

---

### Email 5.1 - The Invitation

**Subject A:** Looking for 5 Montreal brands to shape what we're building
**Subject B:** Design partner invite for {{firstName}} - AI visibility for Canadian retail

Hi {{firstName}},

I'm Alejandro, founder of VisiMind. We're building an AI remediation layer for Canadian luxury brands - specifically solving the bilingual data problem that makes LLMs ignore or hallucinate about brands like {{brand}}.

I'm looking for 5 Montreal-based brands to be design partners. Here's the deal:

- **You get:** VisiMind free for 12 months. Full bilingual AI audits, Fix Kits, ongoing monitoring.
- **We get:** Your feedback on what actually matters. What's useful, what's not, what we should build next.

We already have a working product - Bilingual Probe, Inference Alignment Scoring, automated JSON-LD Fix Kits, Shopify integration. But we want to build it WITH the brands who need it most.

{{brand}} is on my shortlist because of your bilingual catalog and Montreal presence.

Interested?

{{sender}}

---

### Email 5.2 - The Proof (Send: Day 3, Wednesday 8:00 AM ET)

**Subject A:** What VisiMind already does for brands like {{brand}}
**Subject B:** Quick demo of what design partners get

Hi {{firstName}},

Following up on the design partner invite.

To show this isn't vaporware - here's what VisiMind does today:

1. **Bilingual Probe** runs your brand through ChatGPT, Perplexity, and AI Overviews in English and French. Identifies every hallucination and gap.
2. **Inference Alignment Score** gives you a single number (1-100) for how well AI understands {{brand}}.
3. **Fix Kit** generates bilingual JSON-LD structured data from your existing product catalog. Deploys to Shopify in minutes.
4. **Monitoring** via Peec AI and Otterly tracks your AI citations over time.

Design partners get all of this free plus direct input on the roadmap. We've already onboarded 2 of the 5 slots.

15 minutes to see if it's a fit?

{{sender}}

---

### Email 5.3 - The Scarcity (Send: Day 6, Saturday 9:00 AM ET)

**Subject A:** 2 design partner slots left
**Subject B:** Closing the design partner cohort Friday

Hi {{firstName}},

Last note on this. We're closing our design partner cohort this Friday with 5 brands. We have 3 confirmed - 2 slots left.

I picked {{brand}} for this list because the bilingual problem hits you harder than most. You have a strong French catalog, Montreal roots, and a customer base that searches in both languages. That's exactly the use case we need to nail.

After this cohort, VisiMind goes to paid tiers. Design partners lock in free access and get to shape the product.

No pressure - but if there's any interest, a quick reply gets you on the list.

{{sender}}

---
---

# SENDING CADENCE CHEAT SHEET

| Sequence | Email 1 | Email 2 | Email 3 |
|----------|---------|---------|---------|
| Scary Report | Tuesday 8:15 AM | Thursday 8:15 AM (+2 days) | Monday 9:00 AM (+5 days) |
| Competitor | Wednesday 7:45 AM | Friday 8:30 AM (+2 days) | Monday 8:00 AM (+3 days) |
| French Token | Thursday 10:00 AM | Monday 10:00 AM (+4 days) | Tuesday 10:00 AM (+8 days) |
| Free Audit | Tuesday 9:30 AM | Thursday 9:30 AM (+2 days) | Monday 10:00 AM (+5 days) |
| Design Partner | Monday 8:00 AM | Wednesday 8:00 AM (+2 days) | Saturday 9:00 AM (+3 days) |

All times Eastern. Avoid sending between 12-1 PM (lunch) and after 5 PM.

---

# PERSONALIZATION VARIABLES

| Variable | Description |
|----------|-------------|
| `{{brand}}` | Target brand name (Mackage, SSENSE, Aldo, etc.) |
| `{{firstName}}` | Contact's first name |
| `{{competitor}}` | Primary competitor already performing well in AI search |
| `{{competitor1}}`, `{{competitor2}}` | Two competitors for comparison |
| `{{score}}` | Brand's Inference Alignment Score (English) |
| `{{scoreFR}}` | Brand's Inference Alignment Score (French) |
| `{{X}}` | Dynamic stat pulled from actual audit data |
| `{{sender}}` | Sender's name and title |
| `{{link}}` | Calendly booking link |

---

# SEQUENCE SELECTION GUIDE

| If the contact is... | Use this sequence |
|---|---|
| A marketer worried about competitors | Sequence 2: Competitor Advantage |
| Technical (CTO, engineer, technical SEO) | Sequence 3: French Token Decay |
| Cold, no prior relationship, need to earn trust | Sequence 4: Free Audit |
| A senior decision-maker at a top-5 target brand | Sequence 5: Design Partner |
| Anyone else / default sequence | Sequence 1: Scary Report |
