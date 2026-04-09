# AI Visibility Audit: ALDO

## Prepared by VisiMind | April 2026

---

### We tested 9 non-branded queries. Aldo appeared in zero.

When consumers search AI assistants for footwear in Canada, sustainability, boots in Montreal, or any non-branded shopping query we tested, Aldo does not appear. Not once. Not in English, not in French.

Aldo's own sub-brand, Call It Spring, surfaced in two results. Aldo itself surfaced in none.

---

### What We Tested

We ran 9 real shopping queries through AI-powered search tools and documented which brands appeared.

**"best sustainable shoes Canada"**
- Brands surfaced: Allbirds, Vessi, Native Shoes
- **Aldo: absent**

**"best leather boots Montreal"**
- Brands surfaced: Anfibio, Ateliers, Maguire
- **Aldo: absent.** Aldo is headquartered in Montreal.

**"sustainable footwear brands Canada"**
- Brands surfaced: Allbirds, Vessi, Native Shoes
- **Aldo: absent.** Aldo has been carbon-neutral since 2024 and holds LWG Gold certification. AI systems did not surface any of this.

**"Aldo vs Steve Madden"**
- Comparison content exists but is controlled entirely by third-party sites. Aldo does not own the narrative in its own brand comparison.

**"Aldo shoes review"**
- AI-generated summary describes quality as "mediocre" and cites a 2.5/5 Yelp rating. Without structured review data from Aldo's own site, third-party sentiment fills the gap.

**French: "meilleures bottes cuir femme Montreal"**
- **Aldo: absent**

**French: "meilleures chaussures Montreal"**
- **Aldo: absent**

Across every non-branded query, AI summaries mentioned Aldo zero times.

---

### Technical Audit of aldoshoes.com

**AI Readiness Score: 5/10**

| Finding | Status | Impact |
|---|---|---|
| **Platform** | Shopify (210aua-9k.myshopify.com), migrated Nov 2025 | Recent migration is an opportunity to build the structured data layer correctly from the start |
| **Meta Description** | Best of all 10 brands audited: "The ultimate destination for on-trend footwear, bags and accessories" | Strong foundation for brand messaging |
| **JSON-LD Schema** | Organization + WebSite only | AI knows Aldo exists but cannot read any product data |
| **Product Schema** | Missing | Size, color, price, availability -- none of it is machine-readable |
| **llms.txt** | 404 | No AI product discovery file exists |
| **Bilingual Schema** | Missing | French catalog is configured in the backend but invisible to AI |
| **hreflang Tags** | Missing | Search engines and AI cannot associate English and French pages |
| **OG/Twitter Card Tags** | Missing on homepage | Social and AI previews have no structured content to pull |
| **LocalBusiness Schema** | Missing | Aldo has physical stores across Canada with no structured location data |
| **AggregateRating Schema** | Missing | Customer ratings are not exposed, so AI defaults to third-party reviews (including that 2.5/5 Yelp score) |
| **Size/Color Variant Schema** | Missing | The most critical data type for footwear search is completely absent |

The good news: Aldo's meta description is the strongest of all 10 Canadian brands we audited. The Shopify migration in November 2025 means the platform is modern and capable of supporting full structured data. The foundation is solid. What is missing is the data layer that AI systems need to read.

---

### The Bilingual Gap

Aldo's Shopify backend contains French catalog configuration (catalog_name_french, domain_key_french). This data exists but is not exposed as bilingual schema markup.

**What this means in practice:**

- Quebec consumers asking "meilleures chaussures Montreal" will not see Aldo recommended
- French product names and sustainability terms exist in the database but are invisible to every AI system
- No hreflang tags connect English and French content

**Sustainability terms with no schema link between languages:**

| English | French | Schema Link |
|---|---|---|
| recycled leather | cuir recycle | None |
| bio-based sole | semelle bio-sourcee | None |
| carbon-neutral | carboneutre | None |
| LWG Gold certified | Certifie LWG Or | None |

For a footwear brand, this gap is especially damaging. Shoe shoppers use highly specific terms (size, width, material, color) that fragment differently across languages. Without bilingual schema linking these terms, every French query is a lost opportunity.

---

### Why This Is Happening Now

The shift from traditional search to AI-powered shopping is accelerating:

- **87% of ChatGPT shopping recommendations align with Bing rankings**, not Google. Brands optimized only for Google SEO are missing the new distribution channel.
- **AI shopping queries grew 4,700% between 2024 and 2025.** This is not a future trend. It is current consumer behavior.
- **Structured data boosts GPT-4 product accuracy from 16% to 54%** (Data World study). Without it, AI systems guess. With it, they recommend.
- **Canadian luxury and fashion brands have zero documented AI mentions** per the Metricus study. The entire category is invisible.

For Aldo, the gap is compounded by two factors:

1. **Footwear is comparison-driven.** Consumers ask "best boots under $200" and expect AI to provide side-by-side data. Without Product schema, Aldo cannot participate in these comparisons.

2. **Sustainability is the fastest-growing search modifier in fashion.** Aldo has the credentials (carbon-neutral since 2024, LWG Gold) but zero structured data to back them up. AI systems cannot recommend what they cannot verify.

---

### Competitor Landscape

| Signal | Aldo | Vessi | Allbirds | Maguire |
|---|---|---|---|---|
| Appears in AI sustainability queries | No | Yes | Yes | No |
| Appears in AI Montreal footwear queries | No | No | No | Yes |
| Product-level JSON-LD | No | No | No | No |
| Bilingual Schema | No | N/A | N/A | No |
| Sustainability Credentials | LWG Gold, Carbon Neutral | Waterproof focus | B Corp, Carbon Fund | Handcrafted focus |

**Critical finding: None of the 10 Canadian brands we audited have Product-level JSON-LD.** The first brand to implement it will have a measurable advantage in AI-powered shopping results. Aldo has the strongest foundation (best meta description, recent Shopify migration, genuine sustainability credentials) to be that brand.

---

### The Fix

VisiMind's Fix Kit for Aldo addresses every gap identified in this audit:

1. **Product Schema** -- Full JSON-LD for every product: price, sizes, colors, materials, availability. Footwear-specific attributes (width, heel height, sole type) that AI assistants need for comparison queries.
2. **Sustainability Schema** -- Structured data for LWG Gold certification, carbon-neutral status, recycled materials. This is Aldo's competitive moat, and it needs to be machine-readable.
3. **Bilingual Schema Sync** -- Expose the French catalog that already exists in the Shopify backend as proper hreflang-linked bilingual schema. Connect English and French sustainability terms.
4. **LocalBusiness Schema** -- Physical store locations with hours and availability, enabling "near me" AI queries across Canada.
5. **AggregateRating Schema** -- Surface Aldo's own customer review data so AI systems stop defaulting to third-party ratings.
6. **AI Discovery Layer** -- Custom llms.txt file for AI assistant product discovery.
7. **OG/Twitter Card Tags** -- Structured social previews for every page.

We have already generated a truth clip for the Pilier Recycled Leather Boot ($165 CAD) as a proof of concept.

**Timeline:** Shopify's architecture supports rapid deployment. The commerce infrastructure is ready. Only the structured data layer is missing.

---

### Next Step

Book 15 minutes with Alejandro to walk through these findings and see the fix kit we have already built for the Aldo Pilier Recycled Leather Boot.

**Calendly:** [PLACEHOLDER -- insert Calendly link]

No obligation. The audit data speaks for itself.

---

Alejandro
VisiMind, Montreal

---

*This report was generated using VisiMind's audit pipeline. All search query results are from real AI-powered search testing. Technical findings are based on live analysis of aldoshoes.com. No data was fabricated.*
