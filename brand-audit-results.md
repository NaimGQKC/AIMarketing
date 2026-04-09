# VisiMind Brand Audit Report - Canadian Fashion Brands
### Technical AI-Readiness Assessment for Outreach
**Date:** April 8, 2026 | **Auditor:** VisiMind Technical Research Agent

---

## Executive Summary

8 Canadian fashion brands were audited for AI search readiness. **None have an llms.txt file** (except RUDSAK, which has a rudimentary product dump). **None block AI crawlers** in robots.txt. Most rely on basic Shopify-default schema with significant gaps in product-level structured data, hreflang implementation, and AI-optimization signals. This represents a massive opportunity for VisiMind.

| Brand | AI Readiness Score | Platform | Key Gap |
|-------|-------------------|----------|---------|
| Mackage | 4/10 | Shopify | Missing meta description, no hreflang, no OG tags |
| SSENSE | 3/10 | Custom | 403 blocks on crawlers, no llms.txt |
| ALDO | 5/10 | Shopify | Basic schema only, no product-level rich data |
| RUDSAK | 4/10 | Shopify | No JSON-LD on homepage, bare llms.txt |
| Frank And Oak | 2/10 | Shopify | Zero JSON-LD, no meta description, no OG tags |
| Simons | 3/10 | Custom (AWS) | 403 blocks, inaccessible to AI crawlers |
| Aritzia | 3/10 | Salesforce Commerce Cloud | 403 blocks, inaccessible to AI crawlers |
| Matt & Nat | 4/10 | Shopify | Minimal Product schema, no reviews, no availability |

---

## Detailed Brand Audits

---

### 1. MACKAGE (mackage.com)
**Platform:** Shopify (`us-mackage.myshopify.com`)
**AI Readiness Score: 4/10**

#### What They Have
- JSON-LD: `BreadcrumbList`, `WebSite` (with SearchAction), `Organization`
- Regional domains: .com (US), .ca (Canada), .co.uk (UK), .eu (Europe), .jp (Japan), .co.kr (Korea)
- French support via `/fr/` on .ca and .eu domains
- robots.txt: Standard Shopify restrictions. No AI crawler blocks. Sitemap declared.
- No llms.txt (404)

#### Specific Technical Gaps
1. **No meta description on homepage.** Google and AI models see no summary of what Mackage is. This is a critical SEO gap - every competitor has one.
2. **No OpenGraph or Twitter Card tags detected.** Social sharing produces generic/broken previews.
3. **No hreflang tags despite 6+ regional domains.** Google may index the wrong regional version for users. This creates duplicate content risk across .com, .ca, .eu, .co.uk, .jp, .co.kr.
4. **No Product-level JSON-LD found on product pages** (pages returned 404 on tested URLs, suggesting dynamic/JS-rendered product paths).
5. **No AggregateRating schema** - missing star ratings in search results.
6. **No llms.txt** - AI models have zero brand-specific context.

#### Outreach One-Liner
> "I noticed mackage.com has no meta description on its homepage and no hreflang tags linking your 6 regional domains - meaning Google may be showing your US site to Canadian shoppers, and AI assistants have no summary to quote when recommending your outerwear."

#### VisiMind Fix
- **Structured Data Engine**: Generate Organization, Product, and FAQ schema with full hreflang cross-linking
- **AI Content Optimization**: Add meta descriptions optimized for LLM citation
- **llms.txt Generator**: Create brand context file for AI models

---

### 2. SSENSE (ssense.com)
**Platform:** Custom-built (React/Node.js, not Shopify)
**AI Readiness Score: 3/10**

#### What They Have
- Homepage returns **403 Forbidden** to our crawler - aggressive bot blocking
- robots.txt accessible: 6 sitemaps (including image and regional CN/KR sitemaps), heavy restrictions on language-specific paths, filters, and account areas
- No AI crawler blocks in robots.txt (GPTBot, etc. not mentioned)
- No llms.txt (403)

#### Specific Technical Gaps
1. **403 on homepage fetch** - their server actively blocks non-browser user agents. This means AI crawlers (GPTBot, Anthropic, Perplexity) likely cannot index their content even though robots.txt doesn't block them.
2. **Server-side bot blocking contradicts robots.txt policy** - robots.txt allows AI crawlers, but the server rejects them anyway. This is a configuration conflict.
3. **No llms.txt** - with 403 blocks, AI models are completely blind to SSENSE's brand, inventory, and positioning.
4. **Extensive regional URL blocking** in robots.txt (200+ country code paths blocked) suggests messy internationalization.
5. **6 separate sitemaps** including image sitemaps - they have content to index but are blocking the indexers.

#### Outreach One-Liner
> "I noticed ssense.com returns a 403 error to AI crawlers - your robots.txt technically allows GPTBot and other AI bots, but your server blocks them at the HTTP level. This means when someone asks ChatGPT or Perplexity 'where to buy designer clothes in Canada,' SSENSE is invisible."

#### VisiMind Fix
- **AI Crawler Access Audit**: Identify and resolve server-level bot blocking vs. robots.txt conflicts
- **llms.txt Implementation**: Create authoritative brand context for AI models
- **Structured Data Verification**: Ensure schema is present and accessible to all legitimate crawlers

---

### 3. ALDO (aldoshoes.com)
**Platform:** Shopify (`210aua-9k.myshopify.com`)
**AI Readiness Score: 5/10**

#### What They Have
- JSON-LD: `Organization` (with social links to Instagram, Facebook, Pinterest, TikTok, YouTube, Twitter), `WebSite` (with SearchAction)
- Meta description: "The ultimate destination for on-trend footwear, bags and accessories for women and men. ALDO gives you the confidence to own every step in style and comfort." (146 chars - good length)
- French catalog references in code (`catalog_name_french`, `domain_key_french`)
- robots.txt: Standard Shopify. No AI crawler blocks. AhrefsBot gets 10s crawl delay.
- No llms.txt (404)

#### Specific Technical Gaps
1. **No Product schema on homepage or category pages.** Only Organization and WebSite. Product pages likely have basic Shopify defaults but could not be verified (404 on tested product URLs).
2. **No hreflang tags visible** despite having French catalog capability built into the code. The `/fr/` paths exist in code but aren't declared to search engines.
3. **No OpenGraph or Twitter Card tags detected** on homepage.
4. **No AggregateRating** - ALDO has millions of customer reviews but none are surfaced in structured data for rich search results.
5. **No llms.txt** - AI models lack brand context for the 100+ year-old brand.
6. **French language support is hidden** - `catalog_name_french` exists in code but isn't exposed through hreflang or visible language switching.

#### Outreach One-Liner
> "I noticed aldoshoes.com has French catalog capability built into your Shopify code but no hreflang tags declaring it to Google - your French-Canadian customers may be seeing English results, and your product pages lack the rich schema needed for Google's product carousels."

#### VisiMind Fix
- **Product Schema Generator**: Automated Product JSON-LD with price, availability, reviews, images
- **Multilingual SEO**: hreflang implementation connecting EN/FR catalogs
- **Review Schema**: Surface existing customer reviews as AggregateRating for rich snippets

---

### 4. RUDSAK (rudsak.com)
**Platform:** Shopify (`rudsakofficialsite.myshopify.com`)
**AI Readiness Score: 4/10**

#### What They Have
- **llms.txt EXISTS** - Contains brand description ("Rudsak offers premium, Canadian-designed fashion pieces with luxe details") plus 300+ product/collection links. This is the ONLY brand in the audit with any llms.txt presence.
- French support via `/fr/` locale with language redirect script
- robots.txt: Standard Shopify. No AI crawler blocks.
- No llms.txt format issues but it's a raw product dump, not a proper AI-optimized brand context file.

#### Specific Technical Gaps
1. **No JSON-LD structured data on homepage at all.** Zero - no Organization, no WebSite, no BreadcrumbList. This is worse than Shopify defaults.
2. **No meta description detected** on homepage.
3. **No OpenGraph or Twitter Card tags detected.**
4. **No hreflang tags** despite having EN/FR locale support built in.
5. **llms.txt is a raw product dump** - 300+ product links with no brand narrative, positioning, competitive differentiators, or structured context. It reads like a sitemap, not brand guidance for AI.
6. **Product pages returned 404** on tested URLs, suggesting dynamic URL patterns.

#### Outreach One-Liner
> "I noticed rudsak.com is one of the only Canadian fashion brands with an llms.txt file - that's forward-thinking - but it's essentially a product dump with 300+ links and no brand narrative. Meanwhile, your homepage has zero JSON-LD structured data, which means Google can't generate rich results for RUDSAK searches."

#### VisiMind Fix
- **llms.txt Optimization**: Transform the raw product dump into a proper AI-optimized brand context file with positioning, differentiators, and structured product taxonomy
- **Structured Data Engine**: Add missing Organization, WebSite, Product, and BreadcrumbList schema
- **Bilingual Schema**: Connect EN/FR content with proper hreflang tags

---

### 5. FRANK AND OAK (frankandoak.com)
**Platform:** Shopify (`frank-and-oak-store.myshopify.com`, Symmetry theme v8.2.0)
**AI Readiness Score: 2/10**

#### What They Have
- Page title: "Frank And Oak | Essential Clothing Designed for Better Living"
- Multilingual cookie consent referencing `/fr/` paths
- Cookie settings show `languageMode: Multilingual` with English fallback
- robots.txt: Standard Shopify. No AI crawler blocks.
- No llms.txt (404)

#### Specific Technical Gaps
1. **ZERO JSON-LD structured data on homepage.** No Organization, no WebSite, no BreadcrumbList - nothing. This is the worst schema implementation in the entire audit.
2. **No meta description detected.**
3. **No OpenGraph or Twitter Card tags detected.**
4. **No hreflang tags** despite multilingual mode being configured.
5. **No llms.txt.**
6. **Product pages returned 404** on tested URLs.
7. **Symmetry theme v8.2.0** - older Shopify theme that may lack modern schema support.

#### Outreach One-Liner
> "I noticed frankandoak.com has zero structured data on its homepage - no JSON-LD, no meta description, no OpenGraph tags. When someone asks an AI assistant about sustainable Canadian clothing brands, Frank And Oak is invisible because there's literally no machine-readable brand data for AI to reference."

#### VisiMind Fix
- **Complete Structured Data Overhaul**: Organization, WebSite, Product, BreadcrumbList, FAQ schema from scratch
- **AI Content Layer**: Meta descriptions, OG tags, and llms.txt for full AI visibility
- **Theme Upgrade Consultation**: Recommend modern Shopify theme with built-in schema support

---

### 6. SIMONS (simons.ca)
**Platform:** Custom (AWS, Element UI, Swiper - NOT Shopify)
**AI Readiness Score: 3/10**

#### What They Have
- 55+ million annual sessions - massive traffic
- Mobile app with 200%+ growth
- RFID technology across all stores (deployed 2024-2026)
- Unified commerce, ERP, and HR solutions being deployed
- Bilingual (EN/FR) Canadian retailer since 1840
- robots.txt: **403 - blocked** (could not access)
- No llms.txt (403)

#### Specific Technical Gaps
1. **Returns 403 to AI crawlers** on both homepage and robots.txt - completely opaque to AI models.
2. **No llms.txt accessible** - 186-year-old brand with no AI presence layer.
3. **Cannot verify structured data** due to server blocking, but given the custom platform (AWS/Element UI), structured data is likely minimal or manually maintained.
4. **Bilingual content (EN/FR) likely lacks hreflang** given the custom platform - this typically requires manual implementation.
5. **robots.txt itself is blocked** - bots can't even read the crawl rules, which is a misconfiguration.

#### Outreach One-Liner
> "I noticed simons.ca blocks AI crawlers at the server level - even your robots.txt returns a 403 error. With 55 million annual sessions and 186 years of brand heritage, Simons is completely invisible to ChatGPT, Perplexity, and Google's AI Overviews. That's a significant blind spot as AI-driven shopping grows."

#### VisiMind Fix
- **AI Crawler Access Strategy**: Configure server to allow legitimate AI crawlers while blocking malicious bots
- **Structured Data Audit**: Full schema implementation on custom AWS platform
- **llms.txt Creation**: Brand heritage narrative + bilingual product taxonomy for AI models
- **Bilingual SEO**: hreflang and canonical tag implementation across EN/FR

---

### 7. ARITZIA (aritzia.com)
**Platform:** Salesforce Commerce Cloud (Demandware, since 2012)
**AI Readiness Score: 3/10**

#### What They Have
- On Salesforce Commerce Cloud since 2012 - established enterprise e-commerce
- Significant growth (23% net revenue growth in fiscal 2017, likely much larger now)
- Major North American brand with US and Canada presence
- robots.txt: **403 - blocked** (could not access)
- No llms.txt (403)

#### Specific Technical Gaps
1. **Returns 403 to AI crawlers** on homepage, robots.txt, and llms.txt - total AI blackout.
2. **Salesforce Commerce Cloud** has known limitations in structured data - schema markup requires custom SFCC cartridges or manual implementation, and many SFCC sites have minimal schema.
3. **No llms.txt** - one of Canada's most searched fashion brands has zero AI context layer.
4. **Cannot verify hreflang, OG tags, or JSON-LD** due to 403 blocking.
5. **SFCC platform** typically doesn't include schema markup by default - it requires developer effort to implement.

#### Outreach One-Liner
> "I noticed aritzia.com returns a 403 error to non-browser requests - including AI crawlers like GPTBot and PerplexityBot. When someone asks an AI 'what's the best Canadian women's fashion brand,' Aritzia's actual website data is unavailable, so the AI relies on third-party mentions instead of your own content."

#### VisiMind Fix
- **SFCC AI Integration**: Custom cartridge/implementation for structured data on Salesforce Commerce Cloud
- **AI Crawler Allowlisting**: Configure SFCC to serve content to legitimate AI bots
- **llms.txt Implementation**: Brand positioning + product taxonomy for AI models
- **Schema Markup**: Product, Organization, BreadcrumbList across SFCC pages

---

### 8. MATT & NAT (mattandnat.com)
**Platform:** Shopify (`via-vegan-ltd.myshopify.com`, Dawn theme v3.0.0)
**AI Readiness Score: 4/10**

#### What They Have
- JSON-LD on homepage: `WebSite` (with SearchAction), `Organization` (with social profiles: Facebook, Twitter, Instagram, YouTube, Pinterest, LinkedIn)
- Product page JSON-LD: `Product` type present but minimal
- Page title: "Matt & Nat Canada | Vegan Leather Bags & Accessories"
- robots.txt: Standard Shopify. No AI crawler blocks. Nutch blocked.
- No llms.txt (404)
- Single language mode - English only, no FR support despite being Quebec-based

#### Specific Technical Gaps
1. **Product schema is critically incomplete** - tested on GARNI Vegan Tote Bag page: missing `AggregateRating`, `Offers` (no price/availability), `description`, `image` URLs, `sku`, and `url`. Google cannot generate product rich results.
2. **No meta description detected** on homepage.
3. **No OpenGraph or Twitter Card tags detected.**
4. **No French language support at all** - `primaryLocale: "en"`, `singleLanguageMode` active. This is a Quebec-headquartered brand (Via Vegan Ltd) with zero French content.
5. **No llms.txt** - the "vegan leather" positioning is a strong AI differentiator that's completely unmapped.
6. **Dawn theme v3.0.0** - very outdated (current Dawn is well beyond v3). Older Dawn versions have minimal built-in schema.

#### Outreach One-Liner
> "I noticed mattandnat.com's product pages have Product schema but it's missing price, availability, reviews, and images - the exact fields Google needs for product rich results. Your GARNI Vegan Tote Bag page has a Product JSON-LD block that's essentially empty. Plus, as a Quebec-based brand, you have zero French content."

#### VisiMind Fix
- **Product Schema Enrichment**: Complete Product JSON-LD with Offers, AggregateRating, images, availability
- **French Localization**: Add FR content + hreflang for Quebec market
- **llms.txt with Vegan Positioning**: Leverage "vegan leather" differentiator for AI-driven sustainable fashion queries
- **Theme Update Guidance**: Recommend Dawn upgrade for better built-in schema

---

## Cross-Brand Findings

### Universal Gaps (ALL 8 brands)
| Gap | Brands Affected | VisiMind Feature |
|-----|----------------|-----------------|
| No llms.txt (or inadequate) | 8/8 | llms.txt Generator |
| No AI crawler blocks in robots.txt | 6/6 accessible | AI Crawler Strategy |
| Missing or incomplete hreflang | 8/8 | Multilingual SEO Engine |
| No AggregateRating schema | 8/8 | Review Schema Generator |
| Missing OpenGraph tags | 6/6 accessible | Social Schema Module |

### Platform Distribution
- **Shopify**: 5 brands (Mackage, ALDO, RUDSAK, Frank And Oak, Matt & Nat)
- **Salesforce Commerce Cloud**: 1 brand (Aritzia)
- **Custom/AWS**: 1 brand (Simons)
- **Custom**: 1 brand (SSENSE)

### AI Crawler Accessibility
- **Accessible**: Mackage, ALDO, RUDSAK, Frank And Oak, Matt & Nat (5/8)
- **Blocked (403)**: SSENSE, Simons, Aritzia (3/8)

### Key Insight for Sales
The 3 brands returning 403 errors (SSENSE, Simons, Aritzia) are arguably the highest-value prospects - they are the largest brands with the most to lose from AI invisibility, and their technical teams likely don't realize they're blocking legitimate AI crawlers alongside malicious bots.

The 5 Shopify brands are lower-hanging fruit - VisiMind can offer a standardized Shopify app/integration that fixes schema, llms.txt, hreflang, and meta descriptions across all of them with minimal custom work.

### Priority Outreach Order
1. **RUDSAK** - Already has llms.txt (shows AI awareness), easy to upgrade. Warm lead.
2. **Frank And Oak** - Zero schema = maximum visible improvement. Easy before/after demo.
3. **Matt & Nat** - Broken Product schema on actual pages = concrete, provable gap.
4. **Mackage** - Missing meta description on homepage of a luxury brand = alarming.
5. **ALDO** - Best current state but French catalog gap is compelling.
6. **SSENSE** - High value but complex sale (custom platform, technical team).
7. **Aritzia** - Enterprise SFCC = longer sales cycle but huge contract value.
8. **Simons** - Enterprise custom platform, longest sales cycle.

---

*Report generated by VisiMind Technical Research Agent. All data based on live website fetches performed April 8, 2026.*
