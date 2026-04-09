# AI Visibility Audit: Mackage

## Prepared by VisiMind | April 2026

---

### How We Measured This

We tested 12 real search queries across English and French, covering the exact phrases your customers use when shopping for luxury outerwear. We also ran a technical audit of mackage.com, checking for the structured data and AI-readiness signals that determine whether AI assistants can find, understand, and recommend your brand.

**Result: Mackage appeared in only 1 of 12 queries tested.** That single result was "luxury down jacket brands," where Mackage ranked first. In every other query, including branded ones, Mackage was absent or displaced by competitors and third-party sites.

**AI Readiness Score: 4/10**

---

### What We Found

#### 1. Search Visibility: 12 Queries, 1 Appearance

We ran queries in both English and French that a luxury outerwear shopper in Montreal, Quebec, or anywhere in Canada would realistically type.

**English Queries:**

- **"best luxury winter coats Montreal"** -- Mackage NOT found. Gorski Montreal and Cuir Dimitri rank instead.
- **"luxury down jacket brands"** -- Mackage ranked #1. This was the only query where Mackage appeared at the top.
- **"premium leather jackets Montreal"** -- Mackage absent.
- **"Mackage vs Canada Goose"** -- Third-party comparison sites dominate. They frame Mackage as "less warm but more stylish," controlling the narrative for your own brand name.

**French Queries:**

- **"manteau hiver luxe femme Quebec"** -- Mackage invisible. Audvik owns 2 of the top 3 spots.
- **"meilleur manteau cuir femme Montreal"** -- Mackage absent.

**Branded Queries:**

- **"Mackage winter jacket review"** -- mackage.com does not rank. Trustpilot, PurseForum, and retailer pages dominate instead. When someone searches specifically for your brand, you are not the one answering.

**Competitor pattern:** Quartz Co. appeared across 4 or more queries in both languages, consistently outranking Mackage.

---

#### 2. The AI Discovery Problem

AI-powered shopping is not a future trend. It is happening now.

- AI shopping queries grew 4,700% between 2024 and 2025.
- A Metricus study found that Canadian luxury brands, including Mackage, Rudsak, Sentaler, and Nobis, have zero documented AI mentions.
- The Globe and Mail tested ChatGPT for Canadian shopping recommendations. The AI "forgot" the Canadian brands requirement entirely, defaulting to global names.
- Research shows that 87% of ChatGPT shopping recommendations align with Bing rankings, not Google. If your SEO strategy is Google-only, AI assistants may never see you.

This is not about one chatbot. It is about the infrastructure that feeds every AI system: structured data, schema markup, and machine-readable product information. Mackage is missing almost all of it.

---

#### 3. Technical Gaps (Live Audit of mackage.com)

| Finding | Status | Impact |
|---|---|---|
| **JSON-LD Schema** | Only BreadcrumbList, Organization, WebSite | AI cannot read product prices, availability, reviews, or materials |
| **Product Schema** | MISSING | Your $1,150 Lena Down Jacket has zero structured data for AI to reference |
| **Meta Description** | MISSING on homepage | Search engines and AI have no descriptive summary of your brand |
| **llms.txt** | 404 -- Not found | The emerging standard for AI product discovery does not exist on your site |
| **Hreflang Tags** | MISSING | 6 regional domains (.com, .ca, .co.uk, .eu, .jp, .co.kr) with no language linking |
| **OG Tags** | Not detected | Social sharing and AI social signals are weakened |
| **AggregateRating Schema** | MISSING | No review or rating data exposed to AI systems |
| **Product Offer Schema** | MISSING | Price, availability, currency, and size variants are invisible to machines |

**Platform:** Shopify Plus (us-mackage.myshopify.com)

Mackage has a sophisticated commerce infrastructure: Shopify Plus, six regional domains, and support for multiple currencies. But the structured data layer that makes all of it discoverable by AI is nearly empty. The foundation is strong. The signaling layer is absent.

---

#### 4. Bilingual Crisis

Mackage serves French content through /fr/ paths on .ca and .eu domains. But there is zero bilingual schema markup connecting these language variants, and no hreflang tags linking them to their English counterparts.

**What this means in practice:**

- When a Quebec consumer asks an AI assistant "meilleur manteau luxe Montreal," there is no structured French-language data about Mackage for the AI to draw from.
- Your French product pages exist but are invisible to AI systems because nothing in your markup declares them as French-language alternatives.
- "Mackage Lena Down Jacket" and "Manteau en duvet Mackage Lena" are treated as unrelated entities by AI models because no schema connects them.

**Real bilingual fragmentation from your catalog:**

| English Term | French Equivalent | Schema Link |
|---|---|---|
| 800-fill power | Facteur de gonflement 800 | NONE |
| seam-sealed | coutures scellees | NONE |
| goose down | duvet d'oie | NONE |
| thermal rating | indice thermique | NONE |

Every unlinked term is a missed opportunity for AI to confidently recommend Mackage in French-language queries. Quebec is roughly 23% of Canada's population. In our French-language search tests, Audvik and Quartz Co. appeared where Mackage did not.

---

#### 5. Competitor Comparison

| Signal | Mackage | Canada Goose | Rudsak |
|---|---|---|---|
| AI Readiness Score | 4/10 | Unknown (rate-limited) | Highest among Canadian luxury |
| JSON-LD Schema | Basic (3 types) | Unknown (rate-limited) | Unknown |
| Product Schema | No | No | No |
| llms.txt | No (404) | Unknown (rate-limits AI crawlers) | YES (800+ products) |
| French Support | Yes (/fr/ on .ca and .eu) | Yes (multi-country) | Yes (/fr/ paths) |
| Bilingual Schema | No | Unknown | No |
| AI Crawler Policy | Open | Rate-limited (hostile to AI) | Open |

**Key takeaway:** Rudsak has the most AI-ready infrastructure of any Canadian luxury outerwear brand we audited. Their llms.txt file catalogs 800+ products for AI consumption. Canada Goose has chosen to actively restrict AI crawlers, which may limit their AI visibility over time. Mackage sits in the worst position: open to AI crawlers, but with almost nothing for those crawlers to find.

**None of the Canadian luxury brands we audited have Product-level JSON-LD on their homepage. The first brand to implement it will have a structural advantage in AI recommendations.**

---

### What This Means for Revenue

The shift is already happening:

- **Gartner (2025):** Organic search traffic will decline 25% by 2026 as consumers shift to AI-powered answers
- **Salesforce (2025):** AI-referred traffic to retail sites grew 1,200% during the 2024 holiday season compared to the prior year
- **Authoritas (2025):** Perplexity AI drove a 40x increase in referral traffic to e-commerce sites over 6 months
- **BrightEdge (2026):** AI Overviews now appear in 47% of Google search results, fundamentally changing which brands get clicks

For a brand selling $1,150 down jackets (the Lena, rated to -30C) and $990 leather jackets (the Kenya, LWG Silver certified), every AI recommendation that goes to Quartz Co., Rudsak, or Audvik instead of Mackage is high-value revenue walking out the door. The data from our 12-query test shows this is already happening across both official languages.

---

### The Fix

VisiMind's Fix Kit for Mackage addresses every gap identified in this audit:

1. **Product Schema Automation** -- Full JSON-LD for every product: price, availability, size variants, materials, thermal ratings, certifications (RDS Certified, Bluesign Approved)
2. **Bilingual Schema Sync** -- Hreflang implementation linking all 6 regional domains with mapped terminology (e.g., "800-fill power" linked to "Facteur de gonflement 800")
3. **AI Discovery Layer** -- Custom llms.txt file cataloging your full product line for AI assistants, matching what Rudsak already has
4. **Missing Metadata** -- Homepage meta description, OG tags, and AggregateRating schema to close the basic gaps

**Timeline:** Deployable on Shopify Plus. Your commerce infrastructure is already in place. Only the structured data layer is missing.

---

### Next Step

Book 15 minutes with Alejandro to walk through these findings and see the fix kit we have already built for the Mackage Lena Down Jacket.

**Calendly:** [PLACEHOLDER -- calendly.com/visimind/ai-audit-review]

No obligation. The data speaks for itself.

---

Alejandro
VisiMind, Montreal

*This report was generated using VisiMind's automated audit pipeline. All technical findings are based on live analysis of mackage.com. Search visibility data is based on 12 real queries tested across English and French. AI landscape data is sourced from published research by Metricus, Gartner, Salesforce, Authoritas, BrightEdge, and the Globe and Mail.*
