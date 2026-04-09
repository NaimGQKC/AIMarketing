# VisiMind Sales Operations Playbook
## Lead Scoring, Qualification, CRM Pipeline, Objection Handling & Discovery Script

---

# PART 1: ICP SCORING MATRIX (0-100)

## Overview

Every inbound or outbound lead receives a composite score from 0-100. Leads scoring 70+ are Priority A (immediate outreach). 40-69 are Priority B (nurture sequence). Below 40 are Priority C (long-term drip).

---

## Scoring Dimensions

### 1. Company Size / Revenue Tier (0-15 points)

| Revenue Range (CAD) | Employee Count | Points |
|---|---|---|
| $50M+ annual | 200+ | 15 |
| $20M-$50M | 50-200 | 12 |
| $5M-$20M | 15-50 | 9 |
| $1M-$5M | 5-15 | 6 |
| Under $1M | Under 5 | 3 |

**Data Sources:** LinkedIn Company Pages, Crunchbase, PitchBook, Quebec Enterprise Registry (REQ), annual reports.

**Rationale:** Larger companies have more product SKUs exposed to AI hallucination, higher revenue at risk, and budget to invest. However, even $5M brands are viable if other scores are high.

---

### 2. Industry Fit (0-15 points)

| Industry | Points | Notes |
|---|---|---|
| Luxury fashion / accessories | 15 | Core ICP. Highest hallucination risk, most brand-sensitive. |
| Premium DTC brands | 13 | High product complexity, structured data gaps common. |
| Luxury beauty / cosmetics | 12 | French ingredient terminology causes severe token decay. |
| High-end home / design | 10 | Bilingual catalogs, complex product attributes. |
| Premium food / beverage | 8 | Terroir descriptions fragment in French tokenization. |
| General e-commerce | 5 | Broad fit, less urgency. |
| B2B / SaaS / Services | 2 | Poor fit. Product-data problem doesn't apply. |
| Non-commerce | 0 | Disqualify. |

**Scoring Logic:** Score the primary revenue channel. If a brand spans multiple categories (e.g., SSENSE sells fashion + beauty), use the highest applicable score.

---

### 3. Geographic Fit (0-12 points)

| Geography | Points | Rationale |
|---|---|---|
| Montreal HQ + bilingual catalog | 12 | Maximum bilingual pain. French token decay hits hardest. |
| Quebec (outside Montreal) | 10 | Same bilingual requirements, slightly smaller market. |
| Toronto / Vancouver with French SKUs | 8 | Federal bilingual compliance, French product data exists. |
| Canada-wide, English-only | 5 | AI hallucination problem exists but no bilingual wedge. |
| US / International with bilingual needs | 4 | Potential future market, lower urgency. |
| US / International, English-only | 2 | Generic GEO play, not our differentiation. |

**Key Indicator:** Does the brand serve Francophone customers? Check for a `/fr/` URL path, French product descriptions, or Quebec store locations.

---

### 4. Tech Stack (0-10 points)

| Platform | Points | Rationale |
|---|---|---|
| Shopify Plus | 10 | Our Fix Kit deploys in 15 minutes via Liquid snippets. Fastest time-to-value. |
| Shopify (standard) | 8 | Same deployment, slightly fewer customization options. |
| Akeneo PIM + any frontend | 8 | Direct integration path. Rich product data already structured. |
| BigCommerce / WooCommerce | 6 | JSON-LD injection possible, requires custom integration. |
| Custom headless (Next.js, Nuxt) | 5 | Manual JSON-LD injection, longer deployment. |
| Salesforce Commerce Cloud | 4 | Enterprise sales cycle, complex deployment. |
| SAP Commerce / Hybris | 3 | Very long deployment cycles, enterprise procurement. |
| Unknown / no e-commerce platform | 1 | Likely not selling online directly. |

**Detection Method:** BuiltWith, Wappalyzer, or view-source check for `Shopify.theme`, `cdn.shopify.com`, Akeneo API calls.

---

### 5. AI Awareness Signals (0-12 points)

| Signal | Points |
|---|---|
| Job posting mentioning "AI search," "GEO," or "LLM optimization" | 4 |
| Blog post or press release about AI strategy | 3 |
| LinkedIn posts from leadership about AI in commerce | 2 |
| Active on AI/marketing conferences (speaking or attending) | 2 |
| Hired a "Head of AI" or "AI Marketing Manager" in last 12 months | 3 |
| No AI signals detected | 0 |

**Maximum: 12 points** (cap even if multiple signals present).

**Detection Method:** LinkedIn job search for company name + "AI," Google News alerts, conference speaker lists, LinkedIn posts from C-suite.

**Scoring Philosophy:** High AI awareness is a double-edged sword. Brands aware of the problem are easier to sell to, but may already have a solution in progress. Score high here but check for existing vendor relationships in qualification.

---

### 6. Pain Indicators (0-15 points)

| Indicator | Points | How to Detect |
|---|---|---|
| No JSON-LD structured data on product pages | 5 | View source, Google Rich Results Test |
| French product descriptions present but poorly structured | 4 | Manual review: are French descriptions machine-translated? Do they match English attribute structure? |
| Product data inconsistencies across platforms | 3 | Compare Google Shopping feed vs. website vs. AI outputs |
| Visible AI hallucinations about the brand | 5 | Run 3 bilingual queries in ChatGPT/Perplexity. Document incorrect outputs. |
| Outdated product information in AI responses | 3 | Ask AI about current-season products. Does it reference old collections? |
| Missing from AI recommendations in core category | 5 | "Best [category] brands in Montreal" -- is the brand cited? |

**Maximum: 15 points** (cap even if all indicators present).

**Note:** Pain indicators are the single highest-leverage scoring dimension. A brand with 15/15 pain score and a 50+ total score should be treated as Priority A regardless.

---

### 7. Decision-Maker Accessibility (0-10 points)

| Accessibility Level | Points |
|---|---|
| Direct LinkedIn connection to founder/CTO/VP E-commerce | 10 |
| Second-degree connection with warm intro available | 8 |
| Email found via Apollo/Hunter, responds to cold outreach | 6 |
| Email found but no response history | 4 |
| Only generic info@ or PR email available | 2 |
| No contact information found | 0 |

**Target Roles (in priority order):**
1. VP / Director of E-commerce
2. Head of Digital Marketing
3. CTO / VP Engineering
4. CMO
5. SEO Manager / Technical SEO Lead
6. Founder / CEO (for companies under 50 people)

---

### 8. Competitive Pressure (0-11 points)

| Signal | Points |
|---|---|
| Direct competitor already has structured data / JSON-LD | 4 |
| Competitor appears in AI search results for brand's core queries | 4 |
| Competitor is a VisiMind customer or known GEO-optimized brand | 5 |
| Industry peer mentioned AI visibility in public content | 2 |
| No competitive pressure detected | 0 |

**Maximum: 11 points.**

**Detection Method:** Run the same bilingual queries for the lead's category. Which competitors appear? Do those competitors have clean JSON-LD? This data doubles as ammunition for the "Competitor Advantage" outreach sequence.

---

## Composite Score Calculation

```
Total Score = Company Size (0-15)
            + Industry Fit (0-15)
            + Geographic Fit (0-12)
            + Tech Stack (0-10)
            + AI Awareness (0-12)
            + Pain Indicators (0-15)
            + Decision-Maker Access (0-10)
            + Competitive Pressure (0-11)

Maximum = 100
```

## Priority Tiers

| Tier | Score Range | Action | SLA |
|---|---|---|---|
| **A -- Hot** | 70-100 | Immediate personal outreach. Run Bilingual Probe within 24 hours. Send Scary Report. | First touch within 24 hours |
| **B -- Warm** | 40-69 | Enter automated nurture sequence. Run lightweight audit. | First touch within 72 hours |
| **C -- Future** | 20-39 | Add to long-term drip. Monitor for score changes. | Monthly check-in via newsletter |
| **D -- Disqualify** | 0-19 | Do not pursue. Log reason. | Archive |

## Score Override Rules

1. **Auto-promote to A:** Any brand where we find live AI hallucinations about their products, regardless of total score.
2. **Auto-promote to A:** Any brand that has a competitor already using VisiMind.
3. **Auto-demote to D:** Non-commerce business. No product catalog to remediate.
4. **Auto-demote to D:** Annual revenue under $500K CAD (cannot justify spend).
5. **Score decay:** Reduce score by 5 points per quarter of inactivity (no engagement, no response).

---

# PART 2: AUTOMATED QUALIFICATION PROMPTS

These are ready-to-use prompts for the Claude API (or Gemini, as configured in VisiMind). Each prompt is designed to be called programmatically with brand-specific variables injected.

---

## Prompt 1: AI Readiness Scorer

**Purpose:** Analyze a brand's website and produce a 0-100 AI readiness score.

```
SYSTEM:
You are VisiMind's AI Readiness Analyst. You evaluate how well a brand's
digital presence is optimized for discovery by AI search engines (ChatGPT,
Perplexity, Google AI Overviews). Score from 0-100.

USER:
Analyze the following brand for AI search readiness:

Brand: {{brand_name}}
Website URL: {{website_url}}
Industry: {{industry}}
Location: {{headquarters}}
E-commerce Platform: {{platform}}

Website HTML sample (first product page):
{{html_snippet}}

Evaluate these dimensions and provide a numerical score (0-100) for each:

1. STRUCTURED DATA (0-25): Does the page have JSON-LD Product schema?
   Are attributes complete (name, description, brand, price, availability,
   image, SKU, material, color)? Is there Organization schema?

2. CONTENT QUALITY (0-25): Are product descriptions detailed enough for
   an LLM to extract accurate recommendations? Are they factual and
   attribute-rich (not just marketing fluff)?

3. BILINGUAL PARITY (0-25): If French content exists, does it match the
   English version in depth and structure? Are French product attributes
   (material, care instructions, sizing) fully translated or truncated?

4. TECHNICAL ACCESSIBILITY (0-25): Is content rendered server-side (not
   hidden behind JavaScript)? Are canonical URLs set? Is there a sitemap?
   Are meta descriptions present and accurate?

Output format (JSON):
{
  "brand": "...",
  "overall_score": 0-100,
  "structured_data_score": 0-25,
  "content_quality_score": 0-25,
  "bilingual_parity_score": 0-25,
  "technical_accessibility_score": 0-25,
  "critical_gaps": ["gap1", "gap2", ...],
  "quick_wins": ["win1", "win2", ...],
  "competitive_risk": "HIGH | MEDIUM | LOW",
  "summary": "2-3 sentence executive summary"
}
```

---

## Prompt 2: JSON-LD Structured Data Auditor

**Purpose:** Check whether a brand has proper JSON-LD and identify specific gaps.

```
SYSTEM:
You are a structured data expert specializing in e-commerce JSON-LD for
AI search engine optimization. You audit Product, Organization, and
BreadcrumbList schemas for completeness and correctness.

USER:
Audit the following HTML for JSON-LD structured data quality:

URL: {{page_url}}
Page Type: {{page_type}} (product | category | homepage)
HTML Source:
{{html_source}}

Perform this analysis:

1. SCHEMA DETECTION: List every JSON-LD block found. Identify the @type
   of each. If no JSON-LD exists, flag as CRITICAL.

2. PRODUCT SCHEMA COMPLETENESS: For each Product schema, check for:
   - name, description, brand, image, sku, gtin, mpn
   - offers (price, priceCurrency, availability, url)
   - material, color, size (for fashion/luxury)
   - aggregateRating, review
   - additionalProperty for custom attributes
   Mark each as PRESENT, MISSING, or INCOMPLETE.

3. BILINGUAL SCHEMA: Is there a French-language variant? Does the
   description field contain French text? Is @language set? Are
   bilingual attributes (name, description, material) duplicated
   with proper language tags?

4. AI SIGNAL QUALITY: Would an LLM parsing this JSON-LD be able to:
   - Correctly identify the product category?
   - Accurately state the price and availability?
   - Describe the product materials and features?
   - Recommend this product for relevant queries?

Output format (JSON):
{
  "url": "...",
  "schemas_found": [{"type": "...", "completeness": "0-100%"}],
  "missing_critical_fields": ["field1", "field2"],
  "missing_recommended_fields": ["field1", "field2"],
  "bilingual_status": "NONE | PARTIAL | COMPLETE",
  "ai_signal_grade": "A | B | C | D | F",
  "fix_kit_recommendation": "Description of what VisiMind Fix Kit would add",
  "estimated_fix_time": "X minutes"
}
```

---

## Prompt 3: English vs French Content Quality Comparator

**Purpose:** Compare bilingual content quality and identify token decay risk.

```
SYSTEM:
You are a bilingual (English/French) content analyst specializing in
Canadian luxury e-commerce. You evaluate whether French product content
matches English content in depth, accuracy, and LLM-parseability. You
understand that French text tokenizes differently in LLMs, leading to
semantic signal loss.

USER:
Compare the English and French versions of this product page:

Brand: {{brand_name}}
Product: {{product_name}}

ENGLISH VERSION:
{{english_content}}

FRENCH VERSION:
{{french_content}}

Analyze:

1. CONTENT PARITY (0-100):
   - Word count ratio (FR/EN). Below 0.8 = truncated French.
   - Are all product attributes present in both languages?
   - Are technical specifications (materials, dimensions, care) translated
     or omitted in French?
   - Is the French version human-translated or machine-translated?
     (Look for awkward phrasing, anglicisms, inconsistent terminology.)

2. TOKEN DECAY RISK ASSESSMENT:
   - Identify French phrases that will fragment into excessive sub-word
     tokens. Examples: compound material descriptions, technical fashion
     terms, Quebec-specific terminology.
   - Estimate the semantic signal loss percentage (how much meaning an
     LLM loses when tokenizing the French version vs. English).
   - Flag any French terms that an LLM would likely misinterpret.

3. AI RECOMMENDATION IMPACT:
   - If an LLM receives only the French content, could it accurately
     recommend this product for relevant queries?
   - What queries would fail in French that would succeed in English?

Output format (JSON):
{
  "brand": "...",
  "product": "...",
  "parity_score": 0-100,
  "word_count_en": N,
  "word_count_fr": N,
  "word_count_ratio": 0.0-1.0+,
  "missing_attributes_in_french": ["attr1", "attr2"],
  "translation_quality": "HUMAN | MACHINE | MIXED",
  "token_decay_risk": "HIGH | MEDIUM | LOW",
  "estimated_signal_loss_pct": 0-100,
  "problematic_french_terms": [
    {"term": "...", "issue": "...", "token_count": N}
  ],
  "failing_french_queries": ["query1", "query2"],
  "fix_recommendation": "..."
}
```

---

## Prompt 4: Signal Gap Identifier

**Purpose:** Identify gaps between what AI says about a product and what the brand's actual data shows.

```
SYSTEM:
You are VisiMind's Signal Gap Analyst. You compare AI-generated responses
about a brand's products against the brand's own product data (source of
truth). Every discrepancy is a "Signal Gap" -- a place where AI is either
hallucinating, omitting, or misrepresenting the brand.

USER:
Identify Signal Gaps for this product:

Brand: {{brand_name}}
Product: {{product_name}}
Product URL: {{product_url}}

SOURCE OF TRUTH (brand's own data):
{{product_data_json}}

AI ENGINE RESPONSES:
--- ChatGPT Response ---
Query: "{{query_en}}"
Response: {{chatgpt_response}}

--- Perplexity Response ---
Query: "{{query_en}}"
Response: {{perplexity_response}}

--- Google AI Overview Response ---
Query: "{{query_en}}"
Response: {{google_aio_response}}

For each AI response, identify every Signal Gap:

1. HALLUCINATION: AI stated something factually incorrect about the product.
2. OMISSION: AI failed to mention a key product attribute or feature.
3. STALE DATA: AI referenced outdated information (old price, discontinued
   feature, previous-season details).
4. MISATTRIBUTION: AI attributed a feature from a competitor's product.
5. CATEGORY DRIFT: AI placed the product in the wrong category or use case.

Output format (JSON):
{
  "brand": "...",
  "product": "...",
  "total_gaps": N,
  "gaps": [
    {
      "engine": "chatgpt | perplexity | google_aio",
      "gap_type": "HALLUCINATION | OMISSION | STALE_DATA | MISATTRIBUTION | CATEGORY_DRIFT",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "ai_said": "What the AI stated",
      "brand_truth": "What the brand's data actually says",
      "affected_attribute": "price | material | availability | ...",
      "revenue_impact": "HIGH | MEDIUM | LOW"
    }
  ],
  "inference_alignment_score": 0-100,
  "priority_fixes": ["fix1", "fix2", "fix3"]
}
```

---

## Prompt 5: Personalized Outreach Generator

**Purpose:** Generate a tailored cold outreach message based on a brand's audit data.

```
SYSTEM:
You are a B2B sales copywriter for VisiMind, a Montreal-based startup that
fixes how AI search engines see Canadian luxury brands. Your tone is:
direct, data-driven, zero-fluff, slightly urgent but never pushy. You write
like a technical peer, not a salesperson. Never use emojis, exclamation
points, or phrases like "game-changer" or "cutting-edge."

USER:
Generate a personalized cold email for:

Contact: {{first_name}} {{last_name}}
Title: {{job_title}}
Company: {{brand_name}}
Outreach Sequence: {{sequence_type}} (scary_report | competitor | token_decay | free_audit | design_partner)
Email Number: {{email_number}} (1, 2, or 3)

Brand Audit Data:
- Inference Alignment Score (EN): {{score_en}}/100
- Inference Alignment Score (FR): {{score_fr}}/100
- Top Signal Gaps Found: {{signal_gaps}}
- JSON-LD Status: {{jsonld_status}} (none | partial | complete)
- Primary Competitor in AI: {{competitor}}
- Competitor AI Citation Rate: {{competitor_rate}}%
- Brand AI Citation Rate: {{brand_rate}}%
- Platform: {{platform}}
- Specific Hallucination Found: "{{hallucination_quote}}"

Requirements:
- Subject line: max 8 words. Two A/B variants.
- Body: max 150 words.
- Include one specific, verifiable data point from the audit.
- End with a low-friction CTA (no "book a demo" -- use "worth a look?" or "reply 'send it'").
- If email_number is 2 or 3, reference the previous email naturally.

Output the email in plain text format, ready to paste into a sending tool.
```

---

## Prompt 6: Competitive Position Scorer

**Purpose:** Score a brand's competitive position in AI search for their category.

```
SYSTEM:
You are an AI search competitive analyst. You evaluate how a brand ranks
against its competitors in AI engine recommendations for category-relevant
queries. You understand that AI "recommendation share" is the emerging
equivalent of search engine "market share."

USER:
Score the competitive position of {{brand_name}} in AI search.

Category: {{category}} (e.g., "luxury outerwear," "premium sneakers")
Geography: {{geography}} (e.g., "Montreal," "Canada")
Language: {{language}} (EN, FR, or BOTH)

AI Engine Results for {{N}} queries:

{{query_results_table}}
Format: Query | Engine | Brands Cited | Position of {{brand_name}}

Competitor Set: {{competitors_list}}

Calculate:
1. CITATION RATE: What % of queries cited {{brand_name}}?
2. POSITION QUALITY: When cited, what was the average position (1st mentioned = best)?
3. ACCURACY RATE: When cited, was the information accurate?
4. BILINGUAL GAP: Difference in citation rate between EN and FR queries.
5. COMPETITOR DELTA: How far behind the #1 cited competitor?

Output format (JSON):
{
  "brand": "...",
  "category": "...",
  "citation_rate": 0-100,
  "avg_position": 1.0-10.0,
  "accuracy_rate": 0-100,
  "bilingual_gap": 0-100,
  "competitor_delta": 0-100,
  "competitive_position_score": 0-100,
  "rank_in_category": N,
  "top_competitor": {"name": "...", "citation_rate": N},
  "strategic_assessment": "2-3 sentences",
  "recommended_action": "URGENT | PROACTIVE | MONITOR"
}
```

---

## Prompt 7: Decision-Maker Identifier

**Purpose:** Identify the most relevant decision-maker role for a given company profile.

```
SYSTEM:
You are a B2B sales strategist who identifies the ideal decision-maker and
champion within target companies for a technical AI-optimization product.
The product (VisiMind) sits at the intersection of e-commerce, SEO,
structured data, and AI -- so the buyer varies by company structure.

USER:
Identify the ideal decision-maker for VisiMind sales at:

Company: {{brand_name}}
Size: {{employee_count}} employees
Revenue: {{revenue_range}}
Industry: {{industry}}
Platform: {{platform}}

Known Team Members (from LinkedIn):
{{team_members_list}}
Format: Name | Title | Tenure | Notes

Company Structure Signals:
- Has dedicated SEO team: {{yes/no}}
- Has e-commerce team: {{yes/no}}
- Has engineering/CTO: {{yes/no}}
- Has digital marketing team: {{yes/no}}
- Agency relationships known: {{agencies}}

Determine:
1. PRIMARY TARGET: The person most likely to champion and approve a VisiMind purchase.
2. SECONDARY TARGET: A technical influencer who can validate the product.
3. BLOCKER RISK: Who might block the sale and why?
4. ENTRY POINT: Who is easiest to reach first to open the conversation?
5. OUTREACH SEQUENCE: Which of our 5 sequences (scary_report, competitor,
   token_decay, free_audit, design_partner) best fits each contact?

Output format (JSON):
{
  "company": "...",
  "primary_target": {
    "name": "...",
    "title": "...",
    "rationale": "...",
    "recommended_sequence": "...",
    "risk_level": "LOW | MEDIUM | HIGH"
  },
  "secondary_target": { ... },
  "blocker": {
    "name": "...",
    "title": "...",
    "likely_objection": "...",
    "mitigation": "..."
  },
  "entry_point": { ... },
  "org_chart_strategy": "2-3 sentence approach recommendation"
}
```

---

## Prompt 8: Shopify Theme Structured Data Auditor

**Purpose:** Analyze a Shopify theme's Liquid templates for structured data issues.

```
SYSTEM:
You are a Shopify technical expert who audits theme code for structured
data quality. You understand Liquid templating, JSON-LD injection patterns,
and how Shopify themes typically handle (or fail to handle) product schema
markup. You know that most Shopify themes ship with minimal JSON-LD that
is insufficient for AI search engine optimization.

USER:
Audit this Shopify theme for structured data issues:

Theme: {{theme_name}} (e.g., Dawn, Prestige, Impulse)
Brand: {{brand_name}}
Product Page HTML Source:
{{html_source}}

Theme Liquid Snippet (if available):
{{liquid_snippet}}

Analyze:

1. EXISTING JSON-LD: Parse all existing structured data. List fields present and missing.

2. SHOPIFY DEFAULT vs. CUSTOM: Is this the default Shopify JSON-LD
   (typically Product + BreadcrumbList only) or has it been customized?
   Default Shopify JSON-LD is missing: material, color, size variants,
   aggregateRating, brand details, bilingual content.

3. BILINGUAL GAPS: Does the theme handle French/English product data in
   JSON-LD? Most Shopify themes do NOT -- they only output the primary
   locale in structured data even if the storefront is bilingual.

4. FIX KIT COMPATIBILITY: Can VisiMind's Fix Kit (a Liquid snippet that
   injects enhanced bilingual JSON-LD) be deployed without conflicts?
   Check for: existing JSON-LD that would duplicate, theme-specific
   JavaScript that modifies schema, app conflicts.

5. DEPLOYMENT ESTIMATE: How complex is the Fix Kit deployment?
   - SIMPLE (15 min): Standard theme, no conflicting JSON-LD, snippet injection.
   - MODERATE (30-60 min): Custom theme, some conflicts to resolve.
   - COMPLEX (2+ hours): Heavily customized, multiple apps injecting schema.

Output format (JSON):
{
  "theme": "...",
  "brand": "...",
  "existing_jsonld_types": ["Product", "BreadcrumbList", ...],
  "completeness_score": 0-100,
  "is_default_shopify": true/false,
  "missing_fields": ["material", "color", ...],
  "bilingual_jsonld": "NONE | PARTIAL | COMPLETE",
  "fix_kit_compatible": true/false,
  "conflicts": ["conflict1", ...],
  "deployment_complexity": "SIMPLE | MODERATE | COMPLEX",
  "deployment_estimate_minutes": N,
  "specific_issues": [
    {"issue": "...", "severity": "HIGH | MEDIUM | LOW", "fix": "..."}
  ]
}
```

---

## Prompt 9: Scary Report Generator

**Purpose:** Generate a compelling "Scary Report" PDF summary from brand audit data.

```
SYSTEM:
You are VisiMind's Report Writer. You create concise, data-driven brand
audit summaries designed to alarm e-commerce decision-makers into action.
The tone is clinical and factual -- the data itself is alarming enough
without sensationalism. Use specific numbers. Every claim must be backed
by the data provided. Structure the report for skimmability: headers,
bullet points, bold key stats.

USER:
Generate a Scary Report for:

Brand: {{brand_name}}
Category: {{category}}
Report Date: {{date}}

Audit Data:
- Inference Alignment Score (EN): {{score_en}}/100
- Inference Alignment Score (FR): {{score_fr}}/100
- Queries tested: {{n_queries}} ({{n_en}} EN, {{n_fr}} FR)
- Signal Gaps found: {{n_gaps}}
- Hallucinations found: {{n_hallucinations}}
- AI citation rate: {{citation_rate}}% (vs. {{competitor}} at {{competitor_rate}}%)
- JSON-LD status: {{jsonld_status}}
- Token decay estimate (FR): {{token_decay_pct}}%
- Top 3 worst AI responses: {{worst_responses}}
- Competitor comparison: {{competitor_data}}

Generate the report with these sections:

1. EXECUTIVE SUMMARY (3 sentences max)
   The single most alarming finding + what it means for revenue.

2. THE AI VISIBILITY CRISIS
   How the brand appears (or doesn't) across ChatGPT, Perplexity,
   and Google AI Overviews. Include specific query examples.

3. THE BILINGUAL GAP
   EN vs FR score comparison. Specific French queries that fail.
   Token decay impact on Francophone customers.

4. SIGNAL GAP BREAKDOWN
   Top 5 most damaging signal gaps with AI quote vs. brand truth.

5. COMPETITIVE POSITION
   How the brand compares to its top competitor in AI recommendations.

6. REVENUE IMPACT ESTIMATE
   Based on AI search growth trends (Perplexity 800% growth in Canada,
   AI Overviews now appearing in 40% of commercial queries), estimate
   the monthly customer touchpoints being influenced by AI. Frame the
   signal gaps as potential revenue leakage.

7. RECOMMENDED ACTIONS (3 bullet points)
   What VisiMind would fix and estimated time to deploy.

Output in Markdown format, ready for PDF conversion. Max 800 words.
```

---

## Prompt 10: Bilingual Token Decay Analyzer

**Purpose:** Perform a technical analysis of how French product descriptions fragment during LLM tokenization.

```
SYSTEM:
You are a computational linguist specializing in LLM tokenization. You
understand how BPE (Byte Pair Encoding) tokenizers process French text
differently from English, and how this creates "token decay" -- the loss
of semantic signal when French text is split into more, smaller tokens
that break meaningful word boundaries.

You know that:
- GPT-4 uses cl100k_base tokenizer (100K vocab, English-biased)
- French compound terms often split into 3-5 tokens where English
  equivalents use 1-2 tokens
- Technical fashion/luxury terms in French are especially vulnerable
- This causes LLMs to lose attribute relationships in French product data

USER:
Analyze bilingual token decay for these product descriptions:

Brand: {{brand_name}}
Product: {{product_name}}

ENGLISH DESCRIPTION:
{{english_description}}

FRENCH DESCRIPTION:
{{french_description}}

Perform:

1. TOKEN COUNT COMPARISON:
   Estimate token count for each description using cl100k_base rules.
   Calculate the ratio (FR tokens / EN tokens). Ratios above 1.3
   indicate significant decay risk.

2. CRITICAL TERM ANALYSIS:
   For key product terms (materials, features, category descriptors),
   show how each tokenizes:
   - English term -> tokens -> semantic preservation (YES/NO)
   - French term -> tokens -> semantic preservation (YES/NO)
   Flag any French term that splits into 3+ tokens.

3. ATTRIBUTE RELATIONSHIP MAPPING:
   Identify product attribute pairs (e.g., "goose down fill" = material +
   type). For each pair:
   - Does the English tokenization keep the relationship intact?
   - Does the French tokenization break it?
   - What would an LLM likely misunderstand?

4. QUERY IMPACT SIMULATION:
   For 5 likely customer queries (provided below), predict whether an LLM
   using only the French data would correctly match this product:
   Queries: {{french_queries}}

5. FIX RECOMMENDATION:
   How would bilingual JSON-LD structured data solve the token decay
   problem for this specific product? What attributes must be explicitly
   structured to preserve semantic signal?

Output format (JSON):
{
  "brand": "...",
  "product": "...",
  "en_token_count": N,
  "fr_token_count": N,
  "token_ratio": 0.0,
  "decay_severity": "CRITICAL | HIGH | MEDIUM | LOW",
  "critical_terms": [
    {
      "en_term": "...",
      "en_tokens": N,
      "fr_term": "...",
      "fr_tokens": N,
      "semantic_preserved": true/false,
      "issue": "..."
    }
  ],
  "broken_attribute_pairs": [
    {
      "attribute": "...",
      "en_intact": true/false,
      "fr_intact": true/false,
      "misunderstanding_risk": "..."
    }
  ],
  "query_match_results": [
    {"query": "...", "en_match": true/false, "fr_match": true/false}
  ],
  "overall_signal_loss_pct": 0-100,
  "fix_priority": "CRITICAL | HIGH | MEDIUM | LOW",
  "jsonld_fields_needed": ["field1", "field2", ...]
}
```

---

# PART 3: CRM PIPELINE DESIGN

## Pipeline Stages

### Stage 0: PROSPECT
**Definition:** Lead identified but not yet contacted. Scoring complete.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Lead scored 40+ on ICP matrix |
| **Actions** | Run automated website audit (Prompts 1, 2, 8). Score lead. Identify decision-maker (Prompt 7). Select outreach sequence. |
| **Exit Criteria** | First outreach email sent |
| **Owner** | Automated / Sales ops |
| **Max Duration** | 48 hours from identification |

**Transition Email:** None (internal stage).

---

### Stage 1: CONTACTED
**Definition:** First outreach sent. Awaiting response.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Email 1 of selected sequence sent |
| **Actions** | Send sequence emails per cadence. Track opens and clicks. If no response after Email 3, wait 14 days and re-enter with different sequence. |
| **Exit Criteria** | Any reply (positive, negative, or neutral) OR meeting booked |
| **Owner** | Sales rep |
| **Max Duration** | 21 days (full 3-email sequence + buffer) |

**Follow-Up Cadence:**
- Day 0: Email 1
- Day 2-3: Email 2
- Day 6-8: Email 3
- Day 21: If no reply, switch sequence and restart (max 2 sequences total)
- Day 42: If still no reply, move to Stage 0 (re-prospect in 90 days)

**Transition Email (on reply):**
```
Subject: Re: [original subject]

{{firstName}}, thanks for the reply.

I have {{brand}}'s bilingual AI audit ready -- it covers how ChatGPT,
Perplexity, and Google AI Overviews currently describe your products
in English and French.

Two options:
1. I send the report now (PDF, 2-page summary) -- you review on your own time
2. We do a 15-minute screen share where I walk through the key findings live

Which works better for you?

{{sender}}
```

---

### Stage 2: ENGAGED
**Definition:** Lead has responded and shown interest. Conversation is active.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Positive reply received. Lead has asked for report, agreed to meeting, or asked a question. |
| **Actions** | Send Scary Report (Prompt 9). Book discovery call. Run full Bilingual Probe if not already done. Prepare personalized demo data. |
| **Exit Criteria** | Discovery call completed |
| **Owner** | Sales rep |
| **Max Duration** | 14 days |

**Follow-Up Cadence:**
- Day 0: Send report or confirm meeting
- Day 1: If report sent and no meeting booked, follow up: "Did you get a chance to look at the audit?"
- Day 3: If meeting not booked, propose 2-3 specific times
- Day 7: "Checking in -- the AI landscape moves fast and I want to make sure the data is still current for {{brand}}"
- Day 14: If no meeting booked, move back to nurture

**Transition Email (post-report, pre-call):**
```
Subject: {{brand}}'s AI audit -- one thing stood out

Hi {{firstName}},

Hope you had a chance to review the audit. One thing I want to flag:

{{most_alarming_finding}}

This is fixable. Our Fix Kit for {{brand}} would take about
{{deployment_time}} to deploy on {{platform}}.

I have 15 minutes open [Tuesday at 10 AM / Wednesday at 2 PM]. I can
show you exactly what the fix looks like and what the before/after
AI response comparison would be.

Does either time work?

{{sender}}
```

---

### Stage 3: DISCOVERY COMPLETED
**Definition:** Discovery call happened. We understand their pain, priorities, and buying process.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Discovery call completed. Qualification checklist filled out. |
| **Actions** | Send call recap email. Generate custom proposal based on discovery findings. Identify next steps (pilot, proposal review, intro to other stakeholders). |
| **Exit Criteria** | Proposal sent and acknowledged |
| **Owner** | Sales rep + founder |
| **Max Duration** | 7 days |

**Qualification Checklist (must be answered during discovery):**
- [ ] Confirmed pain: AI is giving wrong info or ignoring their brand
- [ ] Confirmed budget authority or path to it
- [ ] Confirmed timeline: willing to start within 30 days
- [ ] Confirmed platform: Shopify/compatible tech stack
- [ ] Identified all stakeholders in buying decision
- [ ] Understood current vendor landscape (SEO agency, other tools)

**Transition Email (post-call recap):**
```
Subject: Recap: {{brand}} + VisiMind next steps

Hi {{firstName}},

Good speaking with you today. Quick recap:

WHAT WE FOUND:
- {{brand}}'s Inference Alignment Score is {{score}}/100 (industry benchmark: 70+)
- {{n_gaps}} Signal Gaps across ChatGPT, Perplexity, and AI Overviews
- French content is scoring {{score_fr}}/100 vs. English at {{score_en}}/100
- Your top competitor {{competitor}} has {{competitor_rate}}% AI citation rate vs. your {{brand_rate}}%

WHAT WE PROPOSED:
- Deploy VisiMind's bilingual Fix Kit on {{platform}} ({{deployment_time}})
- Monitor AI citation changes over 30 days
- Run Verify probes at Day 3, 7, and 14 to measure improvement

NEXT STEPS:
{{agreed_next_steps}}

I'll have the formal proposal to you by {{proposal_date}}.

{{sender}}
```

---

### Stage 4: PROPOSAL SENT
**Definition:** Custom proposal delivered. Awaiting decision.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Proposal emailed and opened |
| **Actions** | Track proposal engagement. Follow up on questions. Handle objections. Offer pilot if hesitant. Connect with additional stakeholders if needed. |
| **Exit Criteria** | Verbal "yes" or signed agreement |
| **Owner** | Sales rep + founder |
| **Max Duration** | 21 days |

**Follow-Up Cadence:**
- Day 0: Send proposal
- Day 2: "Wanted to make sure the proposal came through -- any questions?"
- Day 5: "I ran an updated probe this morning. {{brand}}'s French citation rate dropped another X points. Happy to walk through the updated numbers."
- Day 10: "Checking in. I know these decisions take time. Would it help if I set up a quick call with [a reference customer / our CTO] to address any technical questions?"
- Day 15: If stalled, offer a free 14-day pilot as a de-risking move
- Day 21: Decision deadline. If no response, move to Lost with "Timing" reason.

**Transition Email (proposal delivery):**
```
Subject: {{brand}} x VisiMind -- Proposal

Hi {{firstName}},

Attached is the proposal we discussed. Key points:

- SCOPE: Bilingual Fix Kit deployment + 30-day AI monitoring for {{brand}}
- TIMELINE: Live in {{deployment_time}}, first Verify results in 3 days
- INVESTMENT: {{price}} for the initial remediation cycle
- GUARANTEE: If your Inference Alignment Score doesn't improve by 15+ points
  in 30 days, you pay nothing

Happy to jump on a call to walk through any section. I'm free
{{availability}}.

{{sender}}
```

---

### Stage 5: PILOT / PROOF OF VALUE
**Definition:** Brand is running a limited VisiMind deployment to validate results.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Pilot agreement signed or verbal confirmation for free trial |
| **Actions** | Deploy Fix Kit on 5-10 product pages. Run baseline probes. Monitor daily. Share results at Day 3, 7, 14. Run Verify probes. |
| **Exit Criteria** | Pilot complete. Results shared. Decision meeting scheduled. |
| **Owner** | Sales rep + technical lead |
| **Max Duration** | 30 days |

**Follow-Up Cadence:**
- Day 1: Deploy confirmation + baseline metrics email
- Day 3: First Verify probe results
- Day 7: Progress report with before/after comparison
- Day 14: Full results presentation
- Day 21: Decision meeting
- Day 30: Pilot ends. Convert or close.

**Transition Email (Day 3 results):**
```
Subject: {{brand}} pilot -- Day 3 results are in

Hi {{firstName}},

Day 3 update on the VisiMind pilot for {{brand}}:

BEFORE FIX KIT:
- Inference Alignment Score (EN): {{before_en}}/100
- Inference Alignment Score (FR): {{before_fr}}/100
- AI Citation Rate: {{before_citation}}%

AFTER FIX KIT (Day 3):
- Inference Alignment Score (EN): {{after_en}}/100 ({{delta_en}} change)
- Inference Alignment Score (FR): {{after_fr}}/100 ({{delta_fr}} change)
- AI Citation Rate: {{after_citation}}%

KEY WINS:
- {{win_1}}
- {{win_2}}

We're seeing the pattern we expected: structured data injection starts
shifting AI reasoning within the first 72 hours. The bigger gains
typically appear at Day 7-14 as AI engines re-index.

I'll send the Day 7 report on {{date}}. In the meantime, you can
monitor live at [dashboard link].

{{sender}}
```

---

### Stage 6: CLOSED WON
**Definition:** Customer signed. Onboarding begins.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Agreement signed and payment processed |
| **Actions** | Trigger onboarding workflow. Full Fix Kit deployment. Set up monitoring dashboards. Schedule 30/60/90 day reviews. |
| **Exit Criteria** | N/A (moves to Customer Success) |
| **Owner** | Customer Success (handoff from Sales) |

**Transition Email (welcome):**
```
Subject: Welcome to VisiMind -- {{brand}} onboarding starts now

Hi {{firstName}},

We're live. Here's your onboarding plan:

WEEK 1:
- Full Fix Kit deployment across your {{platform}} product catalog
- Baseline Bilingual Probe across {{n}} queries
- Dashboard access: [link]

WEEK 2:
- Day 3 Verify probe results shared
- Day 7 progress report

WEEK 3-4:
- Day 14 full results presentation
- Ongoing monitoring active
- RAFT cadence established for continuous improvement

Your dedicated point of contact is {{csm_name}} (cc'd). They'll
schedule your kick-off call for this week.

Let's make AI work for {{brand}}.

{{sender}}
```

---

### Stage 7: CLOSED LOST
**Definition:** Lead declined or went silent. Logged with reason.

| Attribute | Detail |
|---|---|
| **Entry Criteria** | Explicit "no" received OR max duration exceeded at any stage |
| **Actions** | Log loss reason. Add to re-engagement drip (quarterly). Monitor for trigger events (new hire, competitor move, funding round). |
| **Exit Criteria** | Re-engagement successful (move to Stage 1) or 12-month archive |
| **Owner** | Sales ops |

**Loss Reason Categories:**
- Timing: Not ready now, revisit later
- Budget: Cannot justify spend
- Champion Left: Key contact departed
- Competitor: Chose another vendor
- No Need Perceived: Doesn't believe AI search matters
- Technical: Platform incompatible
- No Response: Went dark

**Re-Engagement Email (90 days after close-lost):**
```
Subject: {{brand}}'s AI visibility -- 90-day update

Hi {{firstName}},

It's been about 3 months since we last spoke. I re-ran {{brand}}'s
bilingual AI audit to see what's changed:

- Inference Alignment Score: {{current_score}}/100 (was {{previous_score}})
- {{competitor}} AI citation rate: {{competitor_current}}% (was {{competitor_previous}}%)
- New finding: {{new_finding}}

{{context_based_on_loss_reason}}

No pressure -- just wanted to keep you in the loop. The data speaks
for itself.

{{sender}}
```

---

## Pipeline Metrics Dashboard

### Leading Indicators (weekly)

| Metric | Target | Definition |
|---|---|---|
| New leads scored | 20/week | Leads entering Stage 0 |
| Outreach sent | 15/week | Unique leads contacted (Stage 0 -> 1) |
| Response rate | 15%+ | Replies / outreach sent |
| Meetings booked | 3/week | Discovery calls scheduled |
| Proposals sent | 2/week | Stage 3 -> 4 conversions |

### Lagging Indicators (monthly)

| Metric | Target | Definition |
|---|---|---|
| Stage 1 -> 2 conversion | 20%+ | Contacted -> Engaged |
| Stage 2 -> 3 conversion | 60%+ | Engaged -> Discovery |
| Stage 3 -> 4 conversion | 70%+ | Discovery -> Proposal |
| Stage 4 -> 5/6 conversion | 40%+ | Proposal -> Pilot or Won |
| Stage 5 -> 6 conversion | 70%+ | Pilot -> Won |
| Overall pipeline velocity | 35 days | Avg days from Stage 1 to Stage 6 |
| Average deal size | $X/month | Revenue per closed customer |
| Win rate | 15%+ | Closed Won / Total opportunities |
| Loss reasons distribution | -- | Track top 3 loss reasons monthly |

### Sequence Performance (monthly)

| Metric | Track Per Sequence |
|---|---|
| Open rate | By sequence and email number |
| Reply rate | By sequence and email number |
| Meeting book rate | By sequence |
| Subject line A vs B | Winner per send |
| Best performing sequence | Rank by meetings booked |

---

# PART 4: OBJECTION HANDLING GUIDE

## Framework

Every objection response follows this structure:
1. **Acknowledge** the concern (never dismiss it)
2. **Reframe** with data or a different perspective
3. **Bridge** to value with a specific proof point
4. **Advance** with a low-commitment next step

---

### Objection 1: "We already have an SEO team."

> "That makes total sense, and a strong SEO team is valuable. Here's the thing -- AI search optimization is a fundamentally different discipline from SEO. Your SEO team optimizes for Google's ranking algorithm: keywords, backlinks, page speed, meta tags. That's about being found in a list of ten blue links.
>
> AI search engines work differently. ChatGPT and Perplexity don't rank pages -- they read data, reason about it, and generate a recommendation. The question isn't 'does {{brand}} rank on page one?' It's 'when someone asks ChatGPT for the best luxury [category] in Montreal, does it recommend {{brand}} with accurate information?'
>
> I'd actually love to show this to your SEO team. They'd likely become our biggest internal champion once they see the data. Could I send over {{brand}}'s AI audit for them to review?"

---

### Objection 2: "We don't care about AI search yet."

> "I hear that from a lot of brands, and honestly, a year ago I'd have agreed. But here's what changed: Perplexity grew 800% in Canada last year. Google AI Overviews now appear in roughly 40% of commercial queries. And among shoppers under 35, AI is already the first place they ask for product recommendations.
>
> The reason I'm reaching out now specifically is that AI search has a compounding problem. Unlike Google, where you can always buy your way back to page one, AI engines reinforce their own outputs. If ChatGPT is currently recommending {{competitor}} instead of {{brand}}, every new user interaction trains it to keep doing that.
>
> I'm not asking for a commitment. I'm asking for 10 minutes to show you what AI is currently telling your customers about {{brand}}. If the data doesn't concern you, no hard feelings."

---

### Objection 3: "Our agency handles this."

> "Great -- which agency are you working with? [Listen.] They're solid.
>
> Here's a question for your agency: when was the last time they ran a bilingual AI probe on {{brand}}? Specifically -- what does ChatGPT say about your products when someone asks in French? What does Perplexity recommend instead of {{brand}} for your core category?
>
> Most agencies are focused on traditional SEO and paid media, which is the right work. But AI search optimization requires a different toolset: structured data injection, bilingual JSON-LD, inference alignment monitoring. It's not something most agencies have built out yet.
>
> VisiMind isn't a replacement for your agency. We're the layer that makes your existing structured data work for AI engines. Would your agency be open to a three-way call so we can show them the gap?"

---

### Objection 4: "Too expensive."

> "I appreciate the honesty. Let me make sure we're comparing the right numbers.
>
> The average luxury brand in Montreal gets asked about by AI engines thousands of times a month. Right now, {{brand}}'s AI citation rate is {{brand_rate}}% -- meaning AI recommends you in roughly {{brand_rate}} out of 100 relevant queries. Your top competitor is at {{competitor_rate}}%.
>
> Each of those missed citations is a potential customer who asked AI 'what's the best [category] in Montreal?' and got sent to someone else. At an average order value of [their AOV], even recapturing 5% of those lost recommendations would cover VisiMind's annual cost in the first month.
>
> But I don't expect you to take my word for it. Would a 14-day pilot make sense? We deploy the Fix Kit on 10 product pages, measure the AI response shift, and you decide based on real results."

---

### Objection 5: "We're too busy right now."

> "Totally understand -- what's the big priority right now? [Listen.] That makes sense.
>
> Here's why I bring it up anyway: VisiMind's Fix Kit deployment takes about 15 minutes on Shopify. It's not a 6-month project. The monitoring runs automatically after that.
>
> The risk of waiting is that AI engines compound their biases. If {{competitor}} is getting recommended now, every user interaction reinforces that pattern. Three months from now, the gap will be wider.
>
> What if I sent you the audit report now, and we schedule a 15-minute call for whenever your current sprint wraps up? That way you have the data ready when the timing is right."

---

### Objection 6: "This sounds like snake oil / I don't believe this works."

> "Fair challenge. I'd be skeptical too if someone told me AI was hallucinating about my products.
>
> So here's what I want you to do right now. Open ChatGPT. Type: 'What are the best luxury [your category] brands in Montreal?' Then ask the same thing in French.
>
> Look at what comes back. Is {{brand}} mentioned? Is the information accurate? Now ask about a specific product -- does ChatGPT get the price right? The materials? The availability?
>
> This isn't theory. It's observable, testable, and happening right now. The audit I ran on {{brand}} documents every gap with screenshots and exact AI outputs.
>
> I can send you the audit with no call required. You verify every data point yourself. If it checks out, we talk. If it doesn't, I'll leave you alone."

---

### Objection 7: "We're focused on Google / traditional search."

> "Smart -- Google still drives the majority of search traffic. But here's what's shifting underneath: Google itself is going AI-first. AI Overviews now appear above organic results in almost half of commercial queries. The organic links your SEO team fights for are getting pushed below an AI-generated answer.
>
> That AI-generated answer is built from structured data -- specifically the kind of bilingual JSON-LD that VisiMind deploys. So optimizing for AI search actually strengthens your Google position too, because Google's AI Overviews pull from the same data layer.
>
> This isn't either/or. It's the evolution of what you're already doing. Want me to show you how {{brand}}'s products appear in Google AI Overviews specifically?"

---

### Objection 8: "How is this different from schema markup / SEO tools we already use?"

> "Good question. Traditional schema markup tools (Yoast, Schema Pro, etc.) generate basic JSON-LD for Google's traditional search index: Product name, price, availability, maybe reviews. That's table stakes.
>
> VisiMind does three things these tools can't:
>
> First, we generate bilingual JSON-LD. Your current schema is almost certainly in one language only. AI engines serving Francophone users in Montreal are getting zero structured data in French from your site.
>
> Second, we add AI-specific attributes. Material composition, design provenance, styling context, category relationships -- the attributes LLMs need to generate accurate recommendations, not just the attributes Google needs for a rich snippet.
>
> Third, we monitor and verify. We don't just deploy schema and walk away. We run ongoing probes against ChatGPT, Perplexity, and AI Overviews to measure whether the AI's understanding of {{brand}} is actually improving.
>
> Would it be useful to see a side-by-side: your current JSON-LD versus what VisiMind would generate for the same product?"

---

### Objection 9: "We need to talk to our technical team first."

> "Absolutely, and I'd encourage that. In fact, I'd love to be on that call with your technical team. The deployment is a Liquid snippet injection on Shopify -- no theme changes, no app installations, no code refactoring. Your devs will look at it and know exactly what it's doing in about two minutes.
>
> I can prepare a technical one-pager that covers the implementation details, data architecture, and security model. Would it help if I sent that to your CTO/lead developer directly? Or would a joint 15-minute call be more efficient?"

---

### Objection 10: "What's your track record? Who else uses this?"

> "We're early stage -- I'll be upfront about that. VisiMind launched this year focused on the Canadian luxury market because the bilingual problem is most acute here.
>
> What I can show you is the data. I ran {{brand}}'s audit using the same methodology we use for all clients. The Inference Alignment Scores, Signal Gaps, and token decay metrics are all verifiable -- you can reproduce every test yourself.
>
> We're also looking for 5 design partners in Montreal who want to shape the product in exchange for free access. That might be a better fit than a paid engagement right now -- you'd get full value with zero risk while we build our track record together.
>
> Would the design partner model be interesting?"

---

### Objection 11: "Can't you just give us the JSON-LD and we'll deploy it ourselves?"

> "We can, and for a one-time fix that might work. But here's the issue: AI search is dynamic. The JSON-LD we generate today addresses today's gaps. Next month, AI engines update their models, your competitors change their structured data, and new queries start trending.
>
> VisiMind's value isn't just the Fix Kit -- it's the ongoing monitoring and remediation cycle. We probe, detect new Signal Gaps, update your structured data, and verify the results. It's continuous alignment, not a one-time patch.
>
> That said, I'm happy to generate a sample Fix Kit for one product page so your team can evaluate the quality. If you decide the one-time fix is enough, no hard feelings. But most brands find that the monitoring is where the real value lives."

---

### Objection 12: "AI search is a fad / it will change in 6 months."

> "AI search will absolutely change in 6 months -- it's evolving faster than any channel in history. But it's evolving toward more AI, not less. Google, Bing, Apple, Amazon -- they're all integrating generative AI into their search experiences.
>
> The brands that invest in structured data now are building a foundation that works regardless of which AI model is dominant. JSON-LD structured data is a web standard. It works for Google's AI Overviews today, ChatGPT's browsing feature, Perplexity, and whatever launches next year.
>
> The risk isn't that AI search is a fad. The risk is that your competitors structure their data first and AI engines learn to recommend them instead of you -- and that pattern becomes the default."

---

### Objection 13: "We only sell in English / French isn't a priority."

> "Understood. If your customer base is English-only, the bilingual angle is less relevant. But the core problem still applies: is AI recommending {{brand}} accurately for English queries?
>
> I tested {{n}} English queries for {{brand}} across ChatGPT and Perplexity. Your Inference Alignment Score is {{score_en}}/100 -- meaning AI gets your brand right about {{score_en}}% of the time. The other {{100 - score_en}}% of the time, it's either wrong or recommending a competitor.
>
> That's the problem VisiMind solves regardless of language. The bilingual capability is our differentiator in Montreal, but the structured data and monitoring work for any language.
>
> Want to see the English-only audit?"

---

### Objection 14: "We're locked into a contract with [another vendor]."

> "No problem. When does the contract come up for renewal? [Note the date.]
>
> In the meantime, two things:
>
> First, VisiMind doesn't conflict with most existing vendors. If you're using an SEO agency, they handle rankings. We handle AI inference. Different problem, different solution, complementary work.
>
> Second, I'd love to send you {{brand}}'s AI audit now so you can evaluate it on your own timeline. That way, when your contract is up for review, you have data on the gap that your current vendor isn't addressing.
>
> Would it be useful to have that audit in hand before your next vendor review?"

---

### Objection 15: "I need to see ROI / prove the business case internally."

> "Completely fair. Here's how I'd frame the business case:
>
> Revenue at risk: AI engines influence an estimated [X] product recommendation queries per month in your category in Montreal. Your current AI citation rate is {{brand_rate}}%. Industry leaders are at 60%+. Each percentage point of AI citation rate represents approximately [Y] monthly customer touchpoints.
>
> Cost of inaction: AI engines reinforce their outputs. Each month of inaccurate AI data compounds the problem. Your competitor's citation rate grows while yours stagnates or declines.
>
> Time to value: Fix Kit deploys in 15 minutes. First measurable results in 3 days. Full ROI assessment at 30 days.
>
> Investment: [price] per month versus [estimated monthly revenue impact].
>
> I can build this into a one-page business case doc with {{brand}}'s specific numbers. Would that help you present it internally? I'll also include the before/after data from similar category brands to strengthen the case."

---

# PART 5: DISCOVERY CALL SCRIPT

## Pre-Call Preparation (5 minutes before)

**Required Materials:**
- [ ] Lead's ICP score and breakdown
- [ ] Brand's Scary Report (generated via Prompt 9)
- [ ] 3 specific AI hallucinations to show live
- [ ] Competitor comparison data
- [ ] Brand's website open in browser
- [ ] ChatGPT, Perplexity, and Google open in separate tabs
- [ ] Pre-loaded bilingual queries ready to demonstrate

---

## Opening (2 minutes)

**[0:00 - 0:30] -- Rapport + Agenda**

> "{{firstName}}, thanks for making the time. I know 15 minutes is tight so I'll keep us on track.
>
> Quick agenda: I want to spend the first few minutes understanding what's on your plate right now when it comes to how customers find {{brand}} online. Then I have some data on how AI search engines specifically see {{brand}} that I think will be eye-opening. And we'll wrap with next steps if any make sense.
>
> Sound good?"

**[0:30 - 2:00] -- Context Setting**

> "Before I jump in -- just so you know where this came from: I ran a bilingual AI audit on {{brand}} as part of the research we do at VisiMind. We focus on Canadian luxury brands because the bilingual challenge in this market creates a unique problem that doesn't exist anywhere else. I found some things I thought you should see."

**[Transition]:** "But first -- I want to make sure I understand your world."

---

## Pain Discovery (5 minutes)

**[2:00 - 7:00] -- Structured Question Flow**

Use this sequence. Listen more than talk. Take notes on exact phrasing the lead uses (mirror their language later).

**Question 1 -- Current State:**
> "How do customers typically discover {{brand}} today? What are your top acquisition channels?"

*Listen for: SEO reliance, paid media dependency, social channels, any mention of AI or voice search.*

**Question 2 -- AI Awareness:**
> "Have you or your team looked at how {{brand}} shows up in AI search -- ChatGPT, Perplexity, Google AI Overviews?"

*Listen for: "No" (opportunity to educate). "Yes, it's a mess" (validated pain). "Yes, we're working on it" (competitive displacement).*

**Question 3 -- Bilingual Complexity:**
> "How do you handle the French/English split for {{brand}}'s product content? Is it fully translated, partially, or English-primary?"

*Listen for: Translation process, whether it's human or machine, whether they've noticed quality issues.*

**Question 4 -- Competitive Landscape:**
> "When you think about {{brand}}'s competitive set -- who worries you most when it comes to digital visibility?"

*Listen for: Specific competitor names. Use these in the live demo.*

**Question 5 -- Decision Process:**
> "If this data is as bad as I think it is, who else on your team would need to see it before you could act on it?"

*Listen for: Additional stakeholders, budget authority, timeline, internal process.*

**[Transition]:** "Okay, this is really helpful. Let me show you what I found."

---

## Live Demo of Brand's AI Visibility (5 minutes)

**[7:00 - 12:00] -- The "Oh Sh*t" Moment**

This is the core of the call. You are showing the lead, live, that AI engines are failing their brand. This should be visceral and undeniable.

**Step 1 -- Share Screen**

> "Let me share my screen. I'm going to show you three things live -- no slides, just real AI outputs."

**Step 2 -- English Query (60 seconds)**

Open ChatGPT. Type the query live (don't pre-load -- the lead needs to see it's real):

> "I'm going to ask ChatGPT: 'What are the best [category] brands in Montreal?'"

*Wait for response. Point to where {{brand}} does or doesn't appear.*

> "See that? {{competitor}} is the first recommendation. {{brand}} [doesn't appear / appears with incorrect information]."

**Step 3 -- French Query (60 seconds)**

> "Now the same question in French: 'Quelles sont les meilleures marques de [category] a Montreal?'"

*Wait for response. This is usually worse.*

> "Look at the French response. [Describe what's wrong: brand missing, hallucinated details, competitor domination.] This is what every Francophone shopper in Montreal sees when they ask AI for help."

**Step 4 -- Specific Product Query (60 seconds)**

> "One more. I'm going to ask about a specific {{brand}} product: '[product name] -- is it worth the price?'"

*Wait for response. Show the hallucination.*

> "See here? AI says [the hallucinated detail]. Your website says [the truth]. This is a Signal Gap -- AI is confidently telling your customers wrong information about your products."

**Step 5 -- The Score (60 seconds)**

> "I scored all of this. {{brand}}'s Inference Alignment Score is {{score_en}} out of 100 in English, and {{score_fr}} out of 100 in French. That means AI understands less than [half/a third/a quarter] of what makes {{brand}} relevant.
>
> For comparison, your competitor {{competitor}} scored {{competitor_score}}."

**Step 6 -- The Fix Preview (60 seconds)**

> "Here's what the fix looks like. [Show the Fix Kit JSON-LD briefly.] This is bilingual structured data that we inject into your Shopify theme. It takes about 15 minutes to deploy. It tells AI engines exactly who {{brand}} is, what you sell, and why you're relevant -- in both English and French.
>
> Brands that deploy this typically see their Inference Alignment Score jump 15-30 points within the first two weeks."

**[Transition]:** "So that's the picture. Let me ask you..."

---

## Next Steps (3 minutes)

**[12:00 - 15:00] -- Close + Advance**

**Gauge Interest:**
> "Based on what you just saw -- is this something {{brand}} would want to fix?"

*Listen for buying signal strength.*

**If Strong Interest ("Yes, this is bad, we need to fix this"):**
> "Great. Here's what I'd suggest: I send you the full audit report today. You share it with [stakeholders they mentioned]. And we book a 30-minute session next week where I walk your team through the deployment plan. We can have {{brand}} live on VisiMind within a week of that call.
>
> Does [day/time] work for that follow-up?"

**If Moderate Interest ("This is interesting, let me think about it"):**
> "Completely fair. Let me do this: I'll send you the full Scary Report -- it has all the data we just looked at plus the competitive comparison and specific recommendations. Review it on your own time.
>
> I'll follow up next [day] to see if any questions came up. And if your [CTO/SEO team/agency] wants to see the technical side, I'm happy to do a separate walkthrough with them."

**If Skeptical ("I'm not sure this matters enough"):**
> "I respect that. Here's what I'd offer: I'll send the audit report. Verify the data yourself -- open ChatGPT, run the same queries, see if you get the same results.
>
> If the data checks out and it concerns you, call me. If not, no follow-up from me. Fair?"

**Always End With:**
> "{{firstName}}, I appreciate the time. You'll have the report in your inbox within the hour. Talk soon."

---

## Post-Call Actions (within 1 hour)

- [ ] Send recap email (Stage 3 transition template)
- [ ] Send Scary Report PDF
- [ ] Update CRM: move to Stage 3, log qualification checklist answers
- [ ] If stakeholders mentioned, find their LinkedIn profiles and prepare secondary outreach
- [ ] Schedule follow-up per agreed timeline
- [ ] If pilot discussed, prepare pilot scope document

---

## Qualification Checklist

Complete during or immediately after the discovery call:

| Question | Answer | Score Impact |
|---|---|---|
| Did they confirm AI is giving wrong info about their brand? | YES / NO / UNSURE | +10 if YES |
| Do they have budget authority or know who does? | YES / NO | +10 if YES |
| Are they willing to start within 30 days? | YES / NO | +10 if YES |
| Is their platform compatible (Shopify/Akeneo)? | YES / NO | +5 if YES |
| Did they name additional stakeholders? | YES / NO | Neutral (note names) |
| Do they have an existing vendor in this space? | YES / NO | -5 if YES (displacement required) |
| Did they express competitive concern? | YES / NO | +5 if YES |
| Did they ask about pricing? | YES / NO | +5 if YES (buying signal) |
| Did they agree to a follow-up meeting? | YES / NO | +15 if YES |
| Overall engagement level during the demo? | HIGH / MEDIUM / LOW | Subjective assessment |

**Post-Call Score Adjustment:**
Add the checklist points to the lead's ICP score. Re-classify priority tier if the score crosses a threshold.

**Disqualification Triggers:**
- Platform is SAP/custom with no migration plans (deployment > 2 months)
- No budget authority identified and no path to it
- Explicitly stated AI is not a priority for 12+ months
- Revenue under $500K CAD

---

# APPENDIX: SCORING WORKED EXAMPLES

## Example A: SSENSE (Montreal)

| Dimension | Score | Notes |
|---|---|---|
| Company Size | 15 | $500M+ revenue, 1000+ employees |
| Industry Fit | 15 | Luxury fashion marketplace |
| Geographic Fit | 12 | Montreal HQ, fully bilingual |
| Tech Stack | 5 | Custom headless platform |
| AI Awareness | 8 | Tech-forward company, AI blog posts |
| Pain Indicators | 12 | French content issues, AI hallucinations confirmed |
| Decision-Maker Access | 6 | Reachable via LinkedIn, no warm intro |
| Competitive Pressure | 8 | Competitors appearing in AI results |
| **TOTAL** | **81** | **Priority A** |

## Example B: Mackage (Montreal)

| Dimension | Score | Notes |
|---|---|---|
| Company Size | 12 | $100M+ revenue, 200+ employees |
| Industry Fit | 15 | Luxury outerwear |
| Geographic Fit | 12 | Montreal HQ, bilingual catalog |
| Tech Stack | 10 | Shopify Plus |
| AI Awareness | 4 | Some digital marketing posts |
| Pain Indicators | 14 | No bilingual JSON-LD, AI hallucinating materials |
| Decision-Maker Access | 8 | Second-degree LinkedIn connection |
| Competitive Pressure | 8 | Canada Goose dominates AI results |
| **TOTAL** | **83** | **Priority A** |

## Example C: Small Montreal DTC Brand ($3M Revenue)

| Dimension | Score | Notes |
|---|---|---|
| Company Size | 6 | $3M revenue, 12 employees |
| Industry Fit | 13 | Premium DTC |
| Geographic Fit | 12 | Montreal, bilingual |
| Tech Stack | 8 | Shopify standard |
| AI Awareness | 0 | No signals |
| Pain Indicators | 10 | No JSON-LD, basic French content |
| Decision-Maker Access | 10 | Founder reachable directly |
| Competitive Pressure | 4 | Category not yet competitive in AI |
| **TOTAL** | **63** | **Priority B** |
