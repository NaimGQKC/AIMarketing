# VisiMind Resource Library: Tools, Communities, and Channels for Outreach & Lead Generation

Compiled April 2026. Each section includes tools/resources, links, and how VisiMind can leverage them.

---

## 1. Claude Code Skills & Extensions

### Public Skill Repositories

| Resource | Link | Description |
|----------|------|-------------|
| Anthropic Official Skills | https://github.com/anthropics/skills | Official Claude Code skills maintained by Anthropic |
| awesome-claude-skills (ComposioHQ) | https://github.com/ComposioHQ/awesome-claude-skills | Curated list of skills, resources, and workflow automation tools |
| awesome-claude-skills (travisvn) | https://github.com/travisvn/awesome-claude-skills | Curated list focusing on Claude Code customization |
| alirezarezvani/claude-skills | https://github.com/alirezarezvani/claude-skills | 220+ skills and agent plugins for marketing, product, compliance, and more |
| glebis/claude-skills | https://github.com/glebis/claude-skills | Collection of Claude Code skills for enhanced AI workflows |
| SkillsMP Marketplace | https://skillsmp.com/ | Agent Skills Marketplace for Claude, Codex, and ChatGPT |

**How VisiMind uses these:** Install sales-messaging and outreach skills directly into your Claude Code environment. The `alirezarezvani/claude-skills` repo includes marketing and sales-specific skills. You can also publish your own "AI Brand Audit" skill to the marketplace for visibility.

### MCP Servers for Sales & Lead Generation

| Resource | Link | Description |
|----------|------|-------------|
| Apollo MCP Server | https://mcpmarket.com/tools/skills/apollo-automation | Search leads, enrich contacts, create CRM records, add to sequences |
| Crustdata MCP | https://crustdata.com/blog/best-mcp-servers-for-sales-teams-in-2026 | 60M+ companies, 1B+ people profiles, 95+ filters |
| Amplemarket MCP | https://www.amplemarket.com/blog/how-i-built-an-ai-agent-with-claude-step-by-step-guide-for-2026 | Compress a full morning of prospecting into 90 seconds |
| HubSpot Official MCP | Via HubSpot developer docs | OAuth-authenticated read access to contacts, companies, deals |
| Sales Messaging Frameworks Skill | https://mcpmarket.com/tools/skills/sales-messaging-frameworks | Pre-built sales messaging templates for Claude Code |
| Clearcue + Claude Code | https://clearcue.ai/blog/clearcue-claude-code-lead-gen-workflow | AI-powered lead gen workflow builder |
| Top GTM MCPs | https://syncgtm.com/blog/top-gtm-mcps-claude-code-2026 | 7 go-to-market MCP servers that work with Claude Code |

**How VisiMind uses these:** Connect Apollo MCP or Crustdata MCP to Claude Code to search for Montreal e-commerce brand decision-makers, enrich them with verified emails, and generate personalized outreach - all in a single Claude conversation. Use the dual-pass approach: Claude Haiku for initial ICP filtering, Claude Sonnet for deep evaluation.

---

## 2. Open Source Lead Gen & Outreach Tools

### Cold Email Tools

| Tool | Link | Description |
|------|------|-------------|
| Email-automation (PaulleDemon) | https://github.com/PaulleDemon/Email-automation | Schedule, personalize, and send cold emails with templates and follow-ups |
| Meteor Emails | https://github.com/catin-black/meteor-emails | Free cold email tool with LinkedIn retry and CRM export |
| ColdEmailer | https://github.com/Olshansk/ColdEmailer | Large-scale cold email automation with stats and follow-ups |
| Listmonk | https://listmonk.app/ | Self-hosted newsletter and mailing list manager (AGPLv3) |
| Inbox Zero | https://github.com/elie222/inbox-zero | Open source email management with analytics |

**How VisiMind uses these:** Use Listmonk for the "Bilingual Crisis Report" newsletter distribution. Use Email-automation or ColdEmailer for systematic outreach to Montreal brand marketing directors with personalized audit results.

### Email Finding Tools (Hunter.io Alternatives)

| Tool | Link | Description |
|------|------|-------------|
| Apollo.io | https://www.apollo.io | 210M contacts, 30M companies - free tier available |
| Snov.io | https://snov.io | Email discovery + verification + cold email automation |
| VoilaNorbert | https://www.voilanorbert.com | 98% accuracy email finding |
| Nymeria | https://www.nymeria.io | 500M+ contacts, LinkedIn/GitHub integration |
| Dropcontact | https://www.dropcontact.com | GDPR-first enrichment, good for Canadian compliance |

**How VisiMind uses these:** Apollo.io's free tier is the best starting point - it combines email finding with a basic CRM. Dropcontact is worth considering for PIPEDA/privacy compliance when dealing with Canadian brands.

### Open Source CRMs

| CRM | Link | Best For |
|-----|------|----------|
| Twenty | https://twenty.com/ | Tech-forward startups, developer-first, clean UI |
| EspoCRM | https://www.espocrm.com/ | Lightweight, low hosting cost, easy setup |
| SuiteCRM | https://suitecrm.com/ | Full-featured (contacts, pipelines, reporting, email) |
| Odoo Community | https://www.odoo.com/ | 40+ business apps beyond CRM |

**How VisiMind uses these:** Start with Twenty - it is designed for developer-led startups and has the cleanest interface. Move to SuiteCRM when you need full pipeline tracking. All are free and self-hostable, saving $15K-$30K/year vs. paid alternatives.

---

## 3. AI-Powered Prospecting Tools

### Web Scraping for Brand Data

| Tool | Link | Description |
|------|------|-------------|
| Firecrawl | https://github.com/firecrawl/firecrawl | Converts web pages to clean Markdown/JSON for LLMs. Open source. |
| Crawl4AI | https://github.com/unclecode/crawl4ai | #1 trending open-source LLM-friendly web crawler. Apache 2.0. |
| Scrapeless | https://www.scrapeless.com | Superior anti-detection, enterprise-grade, Firecrawl alternative |
| Browser-Use | https://browser-use.com | AI-powered browser automation for scraping |

**How VisiMind uses these:** Use Crawl4AI (free, Apache 2.0) to crawl Montreal e-commerce brand websites and extract structured data. Feed the Markdown output directly to Claude for "Bilingual Crisis" analysis - checking if brands have proper French/English structured data, schema markup, and AI-readable content. Firecrawl is better for cleaner output but has credit-based pricing.

### LinkedIn Research (Legal Approaches)

| Tool/Approach | Link | Notes |
|---------------|------|-------|
| LinkedIn public profile scraping | https://sociavault.com/blog/linkedin-scraping-legal-guide-2026 | Legal per hiQ v. LinkedIn ruling, but respect ToS |
| Claude Cowork + LinkedIn | https://connectsafely.ai/articles/claude-cowork-linkedin-lead-generation-guide-2026 | Find decision-makers via ConnectSafely MCP |
| Apify LinkedIn Actors | https://apify.com | Open-source-based, feature-rich LinkedIn data extraction |

**How VisiMind uses these:** Use Claude Cowork's LinkedIn integration to identify marketing directors and e-commerce leads at target Montreal brands. Keep it to 1 request per 2-5 seconds, scrape only public data, and focus on research rather than automation spam.

### AI Prospecting Workflows

| Resource | Link | Description |
|----------|------|-------------|
| Amplemarket Prospecting Prompts | https://www.amplemarket.com/blog/ai-sales-prospecting-prompts-claude-chatgpt | 5 prompts for list building, call prep, account mapping |
| Stormy AI Sales Assets | https://stormy.ai/blog/scaling-outreach-claude-code-sales-assets-2026 | Using Claude Code for high-conversion sales assets |
| Clay GTM Platform | https://www.clay.com/blog/ai-sales-prospecting | AI-powered prospect research and enrichment |
| Syntora B2B Automation | https://syntora.io/solutions/can-claude-co-work-realistically-automate-b2b-prospecting-workflows-end-to-end | End-to-end B2B prospecting with Claude |

**How VisiMind uses these:** Implement the dual-pass model: Haiku filters 500 Montreal brands down to 50 high-fit targets, then Sonnet generates personalized "Bilingual Crisis" reports for each. Use Clay or Amplemarket prompts to structure the workflow.

---

## 4. Content Distribution Channels

### Communities (Discord, Slack, Forums)

| Community | Platform | Focus | Link |
|-----------|----------|-------|------|
| Online Geniuses | Slack | 53K+ members, SEO/marketing/growth | https://onlinegeniuses.com/ |
| Traffic Think Tank | Slack | Paid, high-level SEO and growth | https://trafficthinktank.com/ |
| The SEO Community | Slack | Dedicated SEO practitioners | https://theseocommunity.com/ |
| Marketing Discord servers | Discord | 15+ active communities | https://whop.com/blog/marketing-discord-servers/ |
| Reddit r/SEO, r/bigseo | Reddit | LLMs pull heavily from Reddit | https://reddit.com/r/SEO |
| Reddit r/ecommerce | Reddit | E-commerce practitioners | https://reddit.com/r/ecommerce |

**How VisiMind uses these:** Post "Bilingual Crisis" case studies in Online Geniuses and The SEO Community Slack. Reddit is critical since LLMs train on it - write detailed posts about GEO for Canadian brands in r/SEO and r/bigseo to build authority that feeds back into AI recommendations.

### Newsletters to Pitch or Advertise In

| Newsletter | Focus | Link |
|------------|-------|------|
| Search Engine Land Daily | SEO/GEO/AI search news | https://searchengineland.com/ |
| Search Engine Journal | SEO breaking news and updates | https://www.searchenginejournal.com/ |
| EMARKETER Daily | Marketing insights and trends | https://www.emarketer.com/ |
| Position.Digital | GEO/AEO/AI SEO specific | https://www.position.digital/ |
| GenOptima | AI search marketing | https://www.gen-optima.com/ |

**How VisiMind uses these:** Subscribe to all of these for market intelligence. Pitch guest articles about the "Bilingual Crisis" to Search Engine Land (they have a dedicated GEO section). Position.Digital and GenOptima are niche enough to accept contributor posts about Canadian AI search gaps.

### Podcasts to Pitch As a Guest

| Podcast | Focus | Link |
|---------|-------|------|
| AI-Driven Marketer | AI marketing skills, interviews with founders | https://podcasts.apple.com/us/podcast/ai-driven-marketer-master-ai-marketing-to-stand-out-in-2026/id1719663520 |
| Decoding AI for Marketing (DAM) | AI marketing for all skill levels | https://www.decodingaiformarketing.com/ |
| AI for Marketers | AI in marketing applications | https://www.youreverydayai.com/ai-for-marketers-podcast/ |
| Ecommerce Coffee Break | DTC and retail, AI tools | https://ecommercecoffeebreak.com/ |

**How VisiMind uses these:** Pitch the "Bilingual Crisis" angle - it is a unique story (Canadian luxury brands invisible to AI). AI-Driven Marketer and Ecommerce Coffee Break are the best fits. Prepare a 3-minute pitch: problem (70% of Quebec luxury brands get zero AI recommendations), solution (VisiMind's remediation layer), proof (before/after data).

### Product Hunt Launch

| Resource | Link | Key Insight |
|----------|------|-------------|
| Complete PH Launch Guide 2026 | https://blazonagency.com/post/how-to-launch-on-product-hunt | Self-posting works fine in 2026, no need for a hunter |
| B2B PH Launch Guide | https://dowhatmatter.com/guides/product-hunt-launch-guide-b2b | Top-5 = 2K-5K visitors, 10-15% trial conversion |
| PH Day-of Checklist | https://dowhatmatter.com/guides/product-hunt-launch-strategy | 6-9 AM PT is the critical window |

**How VisiMind uses these:** Launch on Product Hunt with the "AI Brand Visibility Audit" as the free hook. Set KPI as demo requests, not upvotes. Build a Ship page now to gather pre-launch subscribers. Target the "AI" and "Marketing" categories. Aim for 30+ upvotes/hour in the 6-9 AM PT window.

---

## 5. n8n Automation Workflows

### Ready-Made Templates

| Template | Link | Description |
|----------|------|-------------|
| B2B Lead Gen with Scrapeless + Claude | https://n8n.io/workflows/5297-intelligent-b2b-lead-generation-workflow-using-scrapeless-and-claude/ | Search automation + website crawling + Claude AI analysis |
| Business Automation ROI Reports | https://n8n.io/workflows/9546-generate-business-automation-opportunities-and-roi-reports-with-claude-ai/ | Generate audit reports with ROI calculations in 60 seconds |
| Lead Magnets with OpenAI + Claude | https://n8n.io/workflows/10489-generate-complete-lead-magnets-with-openai-claude-and-google-docs-automation/ | Auto-generate lead magnets and export to Google Docs |
| 620+ Lead Gen Templates | https://n8n.io/workflows/categories/lead-generation/ | Full library of lead generation workflows |
| Claude + n8n Integrations | https://n8n.io/integrations/claude/ | All available Claude integration patterns |

### Custom Workflow Ideas for VisiMind

| Workflow | Components | Purpose |
|----------|------------|---------|
| Brand Discovery Pipeline | Crawl4AI + Claude Haiku + n8n | Automatically crawl Montreal e-commerce sites, score bilingual readiness |
| Audit Report Generator | n8n + Claude Sonnet + Google Docs | Generate personalized "Bilingual Crisis" PDF reports per brand |
| Outreach Sequencer | n8n + Listmonk + Claude | Send audit results, follow up in 3/7/14 day cadence |
| LinkedIn Monitoring | n8n + LinkedIn API + Slack | Alert when target brands post about AI, search, or expansion |

### Supporting Resources

| Resource | Link |
|----------|------|
| awesome-n8n-templates (280+) | https://github.com/enescingoz/awesome-n8n-templates |
| n8n Lead Gen Automation Guide | https://ai.exoticaitsolutions.com/blog/how-to-automate-lead-generation-with-n8n-the-complete-2026-guide/ |
| Claude Building n8n Workflows | https://www.roborhythms.com/claude-n8n-workflow-2026/ |

**How VisiMind uses these:** Start with the "B2B Lead Gen with Scrapeless + Claude" template and customize it for Montreal e-commerce brands. The "Business Automation ROI Reports" template can be adapted to auto-generate "Bilingual Crisis" audit PDFs. Use Claude Code to describe your automation goal in plain English and it will architect the entire n8n workflow.

---

## 6. Free Tools for Building Credibility

### Website Audit / Lead Magnet Tools (Inspiration)

| Tool | Link | How It Works |
|------|------|--------------|
| SEOptimer | https://www.seoptimer.com/ | White-label audit widget, embeddable on your site, generates PDF reports |
| My Web Audit | https://www.mywebaudit.com/ | Done-for-you landing pages showing partial audit, requires consultation for full results |
| SEO Tester Online | https://www.seotesteronline.com/lead-generation-tool/ | 50+ optimization checks, auto-generated reports |
| Lead Magnet Examples Database | https://www.leadmagnetexamples.com | 200K+ free tool keyword ideas |
| LogicBalls Lead Magnet Generator | https://logicballs.com/tools/lead-magnet-generator | AI-powered lead magnet creation, no signup required |

### "Scary Report" Lead Magnet Strategy

The most effective lead magnets for VisiMind follow this pattern:

1. **Free Audit Tool on Website** - Embed a "Check Your AI Brand Visibility" widget (inspired by SEOptimer). User enters their brand URL, gets a partial report showing how many LLMs fail to recommend them.

2. **Gated Full Report** - The full report (with competitor comparison, remediation steps, estimated revenue impact) requires an email or demo booking.

3. **Personalized Outreach** - For high-value targets, send unsolicited "scary reports" showing their competitors are AI-visible and they are not.

**Key stats that make audits effective as lead magnets:**
- Leads who complete audits are already pre-qualified and aware they have problems
- Website audits naturally filter for businesses that need your services
- Every lead understands they have issues to fix before they even talk to you

### What VisiMind Should Build

| Asset | Description | Effort |
|-------|-------------|--------|
| AI Brand Visibility Checker | Enter a URL, see which LLMs recommend the brand (and which don't) | Medium - use existing Claude API + simple frontend |
| Bilingual Crisis Score | 0-100 score showing French/English AI readiness | Low - wrap existing EEE logic in a public endpoint |
| Competitor Comparison Report | Side-by-side: "Brand X gets recommended by 4/5 LLMs, you get 0/5" | Medium - batch the checker across competitors |
| Revenue Impact Calculator | "You're losing $X/month in AI-referred traffic" | Low - simple formula with industry benchmarks |

---

## 7. Recommended Priority Actions

### Week 1: Foundation
- [ ] Install Claude Code sales skills from `alirezarezvani/claude-skills`
- [ ] Set up Apollo.io free tier for contact enrichment
- [ ] Set up Twenty CRM for pipeline tracking
- [ ] Subscribe to Search Engine Land, Position.Digital, EMARKETER newsletters

### Week 2: Automation
- [ ] Deploy the n8n "B2B Lead Gen with Scrapeless + Claude" template
- [ ] Set up Crawl4AI to crawl top 50 Montreal e-commerce sites
- [ ] Connect Apollo MCP to Claude Code for prospect research
- [ ] Set up Listmonk for email distribution

### Week 3: Content & Community
- [ ] Write "Bilingual Crisis" post for r/SEO and r/bigseo
- [ ] Join Online Geniuses Slack and The SEO Community
- [ ] Pitch guest article to Search Engine Land GEO section
- [ ] Pitch AI-Driven Marketer podcast

### Week 4: Lead Magnet & Launch Prep
- [ ] Build "AI Brand Visibility Checker" free tool on VisiMind website
- [ ] Create Product Hunt Ship page
- [ ] Generate "scary reports" for top 20 Montreal luxury brands
- [ ] Begin personalized outreach sequence via Listmonk

---

## Sources

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [awesome-claude-skills (ComposioHQ)](https://github.com/ComposioHQ/awesome-claude-skills)
- [awesome-claude-skills (travisvn)](https://github.com/travisvn/awesome-claude-skills)
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- [Best Claude Skills GitHub Repos 2026](https://medium.com/all-about-claude/i-found-the-best-claude-skills-github-repos-heres-what-s-actually-worth-installing-in-2026-506aacd22ee5)
- [Top GitHub Repositories for Claude Code Skills](https://www.analyticsvidhya.com/blog/2026/03/github-repositories-to-get-free-claude-code-skills/)
- [SkillsMP Marketplace](https://skillsmp.com/)
- [Best MCP Servers for Sales Teams 2026](https://crustdata.com/blog/best-mcp-servers-for-sales-teams-in-2026)
- [Top MCP Servers for Marketing & Prospecting](https://use-apify.com/blog/mcp-servers-marketing-business-2026)
- [Clearcue + Claude Code Lead Gen](https://clearcue.ai/blog/clearcue-claude-code-lead-gen-workflow)
- [Amplemarket MCP Guide](https://www.amplemarket.com/blog/how-i-built-an-ai-agent-with-claude-step-by-step-guide-for-2026)
- [Top GTM MCPs for Claude Code](https://syncgtm.com/blog/top-gtm-mcps-claude-code-2026)
- [Claude Cowork LinkedIn Integration](https://connectsafely.ai/articles/claude-cowork-linkedin-lead-generation-guide-2026)
- [Email-automation](https://github.com/PaulleDemon/Email-automation)
- [Meteor Emails](https://github.com/catin-black/meteor-emails)
- [ColdEmailer](https://github.com/Olshansk/ColdEmailer)
- [Listmonk](https://listmonk.app/)
- [Inbox Zero](https://github.com/elie222/inbox-zero)
- [Hunter.io Alternatives](https://www.findymail.com/blog/hunter-io-alternatives/)
- [Open Source CRM Benchmark 2026](https://marmelab.com/blog/2026/01/09/open-source-crm-benchmark-2026.html)
- [Twenty CRM](https://twenty.com/)
- [Firecrawl](https://github.com/firecrawl/firecrawl)
- [Crawl4AI](https://github.com/unclecode/crawl4ai)
- [Scrapeless vs Firecrawl](https://www.scrapeless.com/en/wiki/firecrawl-alternatives)
- [LinkedIn Scraping Legal Guide 2026](https://sociavault.com/blog/linkedin-scraping-legal-guide-2026)
- [AI Sales Prospecting Prompts](https://www.amplemarket.com/blog/ai-sales-prospecting-prompts-claude-chatgpt)
- [Clay AI Prospecting](https://www.clay.com/blog/ai-sales-prospecting)
- [B2B Lead Gen with Scrapeless + Claude (n8n)](https://n8n.io/workflows/5297-intelligent-b2b-lead-generation-workflow-using-scrapeless-and-claude/)
- [n8n Lead Generation Templates](https://n8n.io/workflows/categories/lead-generation/)
- [n8n Claude Integrations](https://n8n.io/integrations/claude/)
- [awesome-n8n-templates](https://github.com/enescingoz/awesome-n8n-templates)
- [GEO and AEO FAQ 2026](https://www.emarketer.com/content/faq-on-geo-aeo--where-ai-search-seo-overlap-2026)
- [Search Engine Land GEO Coverage](https://searchengineland.com/library/ai-seo/generative-engine-optimization)
- [Online Geniuses Slack](https://onlinegeniuses.com/)
- [The SEO Community](https://theseocommunity.com/)
- [Marketing Discord Servers](https://whop.com/blog/marketing-discord-servers/)
- [Product Hunt B2B Launch Guide](https://dowhatmatter.com/guides/product-hunt-launch-guide-b2b)
- [Product Hunt Launch Strategy](https://blazonagency.com/post/how-to-launch-on-product-hunt)
- [SEOptimer](https://www.seoptimer.com/)
- [My Web Audit](https://www.mywebaudit.com/)
- [Lead Magnet Examples Database](https://www.leadmagnetexamples.com)
- [AI-Driven Marketer Podcast](https://podcasts.apple.com/us/podcast/ai-driven-marketer-master-ai-marketing-to-stand-out-in-2026/id1719663520)
- [Decoding AI for Marketing Podcast](https://www.decodingaiformarketing.com/)
- [Ecommerce Coffee Break Podcast](https://ecommercecoffeebreak.com/)
