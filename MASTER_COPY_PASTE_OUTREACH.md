# MASTER OUTREACH - COPY PASTE AND GO
**Last updated: April 11, 2026**

Everything below is ready to copy, paste, and post. Replies are varied in length and angle so they dont look like the same person copy pasting the same thing everywhere.

---

## SHOPIFY COMMUNITY REPLIES

---

### 1. Are Shopify stores losing visibility to AI search (SGE, ChatGPT, etc)?
**URL:** https://community.shopify.com/t/are-shopify-stores-losing-visibility-to-ai-search-sge-chatgpt-etc/599726
**Pain point:** general AI visibility anxiety

**REPLY:**
```
yeah im actually working on this for a research project right now. been testing how canadian ecommerce brands show up on chatgpt and perplexity and its bad. like brands with solid google rankings that just dont exist on ai search.

the biggest surprise for me was that chatgpt pulls from bing not google. so all that google seo work doesnt transfer the way you'd think. also found that a lot of stores are blocking ai crawlers at the CDN level without realizing it, like the bots cant even read the pages.

still digging into this but if anyone has a store and is curious how it shows up on ai search i could use more test cases for my research honestly
```

---

### 2. Why your store doesn't show up on ChatGPT, Claude, Perplexity searches and what to fix
**URL:** https://community.shopify.com/t/why-your-store-doesnt-show-up-on-chatgpt-claude-perplexity-searches-and-what-to-fix/593006
**Pain point:** technical fixes for AI invisibility

**REPLY:**
```
one thing i keep running into that nobody mentions: bilingual stores get hit way harder by this. im based in montreal and a lot of the brands i look at run fr/en pages. the llms literally cant figure out which version to cite so they just skip both.

also worth checking if your CDN is returning 403s to GPTBot and PerplexityBot. your robots.txt can be totally fine but cloudflare or whatever is blocking them at a different level. found this on like half the sites ive checked
```

---

### 3. Why do some Shopify products appear in ChatGPT / AI shopping results and others don't?
**URL:** https://community.shopify.com/t/why-do-some-shopify-products-appear-in-chatgpt-ai-shopping-results-and-others-don-t/579646
**Pain point:** inconsistent AI recommendations

**REPLY:**
```
been trying to figure this out too for a school project. from testing a bunch of brands, the pattern i see is:

chatgpt shopping is tied to bing way more than google. like the overlap is crazy high. so if a brand isnt showing up well on bing, chatgpt wont recommend them either.

the other thing is structured data. stores with full json-ld (not just the default theme stuff but reviews, faq, brand info) seem to get picked up more consistently. and then theres the basic one of just making sure the ai crawlers arent blocked, which happens more than you'd expect

anyone else noticing the same patterns or am i off here?
```

---

### 4. How do we optimize our Shopify stores for LLMs (ChatGPT, Gemini, etc.)?
**URL:** https://community.shopify.com/t/how-do-we-optimize-our-shopify-stores-for-llms-chatgpt-gemini-etc/566409
**Pain point:** LLM optimization how-to

**REPLY:**
```
things ive found that seem to make a difference (working on this for my thesis):

- check if GPTBot and OAI-SearchBot are actually able to access your pages. not just robots.txt but CDN/WAF level. a lot of stores block them without knowing
- json-ld schema with more than just the basics. reviews, faq, brand context all seem to help
- llms.txt file on your root domain. its a newer thing but its basically a plain text summary for ai crawlers
- if youre multilingual, double check your hreflang setup. llms really struggle with page pairs

still learning though so take it with a grain of salt. if anyones tried other stuff id love to hear what worked
```

---

### 5. Has anyone optimized their store for AI-driven product discovery (ChatGPT, Claude, Perplexity)?
**URL:** https://community.shopify.com/t/has-anyone-optimized-their-store-for-ai-driven-product-discovery-chatgpt-claude-perplexity/422405
**Pain point:** seeking practical experience

**REPLY:**
```
im a student working on this exact problem. tested a bunch of canadian brands and honestly the results were kind of shocking. brands that own page 1 on google are nowhere on chatgpt or perplexity.

the bing connection is huge btw. chatgpt uses bing as its search backend so your google rankings dont really carry over. that was the biggest aha moment for me

also if anyone here runs a bilingual store (fr/en), id really love to hear your experience. from what ive seen the bilingual setup specifically causes problems for ai engines and im trying to understand it better
```

---

### 6. Urgent!! Need help in making my shopify website appear in AI search results
**URL:** https://community.shopify.com/t/urgent-need-help-in-making-my-shopify-website-appear-in-ai-search-results/421532
**Pain point:** urgent help request

**REPLY:**
```
quick things to check that ive found from looking into this:

1. robots.txt: make sure GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot arent blocked. a lot of themes and security apps do this by default
2. CDN/firewall: even if robots.txt is clean, cloudflare and similar tools sometimes return 403s to ai bots
3. structured data: run your product pages through the schema.org validator. the more context in your json-ld the better

whats your store url? im doing research on ai search visibility for school and can take a look if you want
```

---

### 7. How Can I Add Product Schema for Visibility in AI Search?
**URL:** https://community.shopify.com/t/how-can-i-add-product-schema-for-visibility-in-ai-search/584394
**Pain point:** schema markup for AI

**REPLY:**
```
this is probably the highest leverage thing you can do rn. most shopify themes only ship with basic product schema but ai engines respond way better when you have the full picture, brand info, aggregate reviews, faq, availability, gtin/sku identifiers.

json-ld format is the way to go over microdata. and add faqPage schema to your product pages with actual questions your customers ask, not generic stuff.

one gotcha though: make sure the ai crawlers can actually access your pages in the first place. ive seen stores with perfect schema but GPTBot is getting 403d at the CDN level so none of it matters lol
```

---

### 8. How can I boost multi-language SEO for my e-commerce site?
**URL:** https://community.shopify.com/c/ecommerce-marketing/how-can-i-boost-multi-language-seo-for-my-e-commerce-site/td-p/2461572
**Pain point:** multilingual SEO (perfect bilingual angle)

**REPLY:**
```
ok so for traditional seo the usual advice applies, hreflang tags, separate urls, localized content not just machine translations. but theres something new that i havent seen anyone talk about yet.

ai search engines (chatgpt, perplexity etc) really struggle with bilingual sites. im researching this for school and specifically looking at canadian fr/en stores. when you have page pairs with hreflang tags, the models cant figure out which version to cite and often skip both entirely.

on top of that, french content is super underrepresented in llm training data. like some models have french at 0.16% of their training set. so if your french pages are your primary ones, ai search engines barely know they exist.

this is the exact problem im trying to solve rn so if you have a bilingual store and are willing to share your url id love to take a look. trying to collect as many examples as i can for my research
```

---

### 9. Is ChatGPT the new goldmine for a Shopify store?
**URL:** https://community.shopify.com/t/is-chatgpt-the-new-goldmine-for-a-shopify-store/420191
**Pain point:** ChatGPT as sales channel

**REPLY:**
```
the potential is there for sure, especially with the shopify x openai integration. but from what ive seen most stores arent even showing up yet.

i tested this with a bunch of canadian brands for a research project. asked chatgpt stuff like "best canadian winter jackets" and huge brands with amazing google seo just didnt get mentioned. turns out chatgpt pulls from bing not google so thats a whole separate optimization game.

its early days but feels like theres a real first mover advantage for stores that figure this out now
```

---

### 10. Question about ai visibility for shopify stores!
**URL:** https://community.shopify.com/t/question-about-ai-visibility-for-shopify-stores/587072
**Pain point:** general AI visibility question

**REPLY:**
```
this is what im spending all my time on rn lol. the short version: ai search is a completely different game from google seo and most stores are invisible without knowing it.

the two biggest things ive found: chatgpt runs on bing (not google), and a surprising number of stores accidentally block ai crawlers at the CDN level. like the bots literally cant read the pages even though robots.txt looks fine.

still learning a lot about this, doing it for a school project. what kind of store are you running? curious if you've tested how it shows up on chatgpt
```

---

## INDIE HACKERS REPLIES

---

### 11. AI Visibility Is the New SEO for Indie Makers
**URL:** https://www.indiehackers.com/post/b897ac131a
**Pain point:** indie makers and AI visibility

**REPLY:**
```
this resonates hard. ive been looking at this from the ecommerce angle specifically and its wild how broken it is.

audited a bunch of canadian brands and found that even ones dominating google are completely absent from chatgpt and perplexity recommendations. the bilingual angle is especially interesting to me, canadian stores running fr/en pages get crushed because llms cant resolve which version to cite.

french is also like 0.16% of some models training data which means french-primary content basically doesnt exist to these systems. feels like a massive underserved niche.

anyone else building in the ai visibility space? curious what angles you're seeing
```

---

### 12. When anyone can build, distribution is the only moat (Potatometer thread)
**URL:** https://www.indiehackers.com/post/when-anyone-can-build-distribution-is-the-only-moat-built-a-free-tool-to-improve-your-chatgpt-and-google-visibility-8059f100ee
**Pain point:** similar tool, distribution discussion

**REPLY:**
```
cool tool. working on something in a similar space but focused on ecommerce, specifically how brands show up on ai search.

one thing ive been digging into thats super underexplored: multilingual sites. canadian fr/en stores are basically invisible to llms because the models cant handle hreflang page pairs. curious if youve run into that with your tool at all?

totally agree on distribution being the moat btw. the tech side of these tools is getting easier to build every month, its all about getting in front of the right people
```

---

## LINKEDIN CONNECTION REQUESTS

**Important:** Send from your own LinkedIn. Each has a connection note (300 char max) and a follow-up message to send after they accept. Verify each person is still at the company before sending.

---

### 13. Jasmine Bouchard - Director, eCommerce & Digital Marketing @ RUDSAK
**LinkedIn:** https://ca.linkedin.com/in/jasmine-bouchard-9439b713
**Status:** CONFIRMED still at RUDSAK

**CONNECTION NOTE:**
```
hi jasmine, student in montreal researching how canadian fashion brands show up on ai search engines like chatgpt. ran some tests on rudsak and found some interesting gaps, would love to share if youre open to it
```

**FOLLOW-UP (after accept):**
```
hey jasmine, thanks for connecting!

so for my research im testing how brands show up when people ask chatgpt or perplexity for product recommendations. i ran rudsak through a few queries where the brand should naturally come up (like "best canadian leather jackets") and it wasnt getting cited.

the main things i found: some ai crawlers seem to be getting blocked, the fr/en page setup is confusing the models (they cant figure out which version to recommend), and theres some structured data gaps.

im still a student so this is all research stage, but id love to share the full breakdown if its useful. trying to learn from people who actually work on this stuff. happy to send a quick report or hop on a call, whatever is easier for you
```

---

### 14. Alain Parenteau - Director, Multi-Channel Merchandising @ ALDO Group
**LinkedIn:** https://www.linkedin.com/in/alain-parenteau-80a81024/
**Status:** appears current at ALDO (VERIFY on LinkedIn before sending)

**CONNECTION NOTE:**
```
hi alain, student in montreal researching ai search visibility for canadian brands. tested aldo on chatgpt/perplexity and it didnt come up for any of the 9 non-branded queries i tried. would love to share what i found
```

**FOLLOW-UP (after accept):**
```
hey alain, thanks for accepting!

for a research project im looking at how canadian ecommerce brands show up on ai search engines. i tested aldo across 9 queries where it should naturally come up (things like "best comfortable work shoes" or "affordable leather bags canada") and it wasnt cited in any of them.

from what i can tell the main issues are: chatgpt pulls from bing and aldos bing presence seems weaker than google, some ai crawlers might be hitting errors on the site, and the fr/en page setup is causing confusion for the models.

this is for school so im genuinely just trying to learn and get feedback. would love to share the full audit if its useful to you. always trying to learn from people working on this in the real world
```

---

### 15. Michael Bliah - VP, eCommerce @ Groupe Dynamite
**LinkedIn:** https://ca.linkedin.com/in/michaelbliah
**Status:** appears current at Groupe Dynamite (VERIFY on LinkedIn before sending)

**CONNECTION NOTE:**
```
hi michael, student in montreal researching ai search visibility for canadian fashion brands. ran some tests on dynamite and garage and found interesting blind spots on chatgpt/perplexity. happy to share if useful
```

**FOLLOW-UP (after accept):**
```
hey michael, thanks for connecting!

im doing research on how canadian ecommerce brands show up on ai search engines. tested dynamite and garage across chatgpt, perplexity, and a few others.

both brands seem to be underperforming on ai search compared to their google rankings. the patterns i see are similar to other canadian brands ive tested, ai crawlers potentially getting blocked at the CDN level, the bilingual fr/en setup causing confusion for the models, and some structured data gaps.

im a student so this is all research, but id love your perspective on whether this is something thats on the radar at groupe dynamite. happy to share what i found in more detail if its interesting to you
```

---

### 16. Mackage / APP Group - CMO (Head of eCommerce and Marketing)
**LinkedIn:** Search "CMO Mackage APP Group" on LinkedIn to find current profile
**Note:** Search found there's a CMO for Mackage and Soia & Kyo at APP Group in Montreal. Need to find the specific person's name on LinkedIn before sending.

**CONNECTION NOTE (template, replace [name]):**
```
hi [name], student in montreal researching ai search for canadian luxury brands. tested mackage on chatgpt/perplexity and it only came up for 1 out of 12 relevant queries. would love to share if useful
```

**FOLLOW-UP (template, replace [name]):**
```
hey [name], thanks for connecting!

for my research im looking at how luxury brands show up on ai search engines. tested mackage across 12 queries where it should naturally come up (things like "best luxury winter coats canada" or "high end down jackets") and it only showed up for 1.

the main issues i see: chatgpt pulls from bing and mackages bing presence seems weaker than google, some ai crawlers might not be accessing the site properly, and the bilingual fr/en setup seems to cause problems for the models.

feels like a big opportunity especially for a brand like mackage where people asking chatgpt for luxury coat recs are probably ready to buy. im still in school working on this so id really value your perspective. happy to send over what i found
```

---

## HACKER NEWS REPLIES

---

### 17. How Generative Engine Optimization (GEO) rewrites the rules of search
**URL:** https://news.ycombinator.com/item?id=44133279
**Pain point:** GEO as new paradigm

**REPLY:**
```
been working on this from the ecommerce angle. the gap between google seo and ai search visibility is massive, especially for brands that invested heavily in traditional seo.

one thing i havent seen discussed much: multilingual sites get absolutely wrecked by this. im researching canadian fr/en ecommerce stores and llms cant resolve hreflang page pairs at all. they just skip both versions. french is also ~0.16% of some models training data so french-primary content is basically nonexistent to these systems.

feels like theres a huge underserved niche here for anyone building geo tools that handle multilingual properly
```

---

### 18. Show HN: Searchable AI visibility index (15k+ brands, 500 industries)
**URL:** https://news.ycombinator.com/item?id=46145082
**Pain point:** AI visibility tracking at scale

**REPLY:**
```
this is cool. curious if you have any data on how bilingual sites perform vs single-language ones?

im researching canadian ecommerce brands (fr/en) and finding that the bilingual setup specifically tanks ai visibility. the models cant resolve which page version to cite when theres hreflang page pairs so they skip both. wondering if your index shows the same pattern at scale
```

---

### 19. AI found us before Google did
**URL:** https://news.ycombinator.com/item?id=47293911
**Pain point:** AI search as discovery channel

**REPLY:**
```
interesting. im seeing the opposite for ecommerce brands, especially canadian ones. brands dominating google are completely invisible on chatgpt and perplexity.

the bing dependency is huge since chatgpt uses bing as its search backend. and for bilingual stores running fr/en pages, the models just give up trying to figure out which version to cite.

curious what your site structure looks like that made ai find you first. single language? clean schema?
```

---

### 20. What is GEO and why is no one building in it?
**URL:** https://news.ycombinator.com/item?id=42906914
**Pain point:** GEO market gap

**REPLY:**
```
im building in this space, focused on ecommerce specifically. the problem is real but the tooling is still early.

one niche i think is massively underserved: multilingual geo. im based in montreal and researching how canadian fr/en stores show up on ai search. the results are terrible. llms cant handle hreflang page pairs, french content is barely represented in training data, and cdn/waf setups block ai crawlers without anyone realizing.

theres definitely an opportunity here, the question is whether its big enough to build a business around vs just a feature of broader seo tools
```

---

### 21. Show HN: Geneo - Track your brand visibility across AI search
**URL:** https://news.ycombinator.com/item?id=44325360
**Pain point:** similar product, networking

**REPLY:**
```
neat. do you handle multilingual tracking? specifically fr/en bilingual sites?

ive been researching canadian ecommerce brands and the bilingual setup seems to be a unique failure mode for ai visibility. the models cant resolve hreflang page pairs so they skip both versions entirely. wondering if your tracking picks that up or if it just shows the brand as "not visible" without the bilingual context
```

---

### 22. Show HN: We Built a Tool for GEO
**URL:** https://news.ycombinator.com/item?id=45495087
**Pain point:** similar tool builders

**REPLY:**
```
cool, working on something adjacent focused on ecommerce brands.

one pattern im seeing that i dont think anyone has cracked yet: bilingual/multilingual sites. canadian stores with fr/en page pairs are basically invisible to llms because the models cant resolve which version to cite. french is also massively underrepresented in training data.

how are you handling multilingual content in your tool? feels like a gap in the whole geo space right now
```

---

## DEV.TO REPLIES

---

### 23. GEO: Why Your Website Might Be Invisible to AI in 2026
**URL:** https://dev.to/kazkn/geo-generative-engine-optimization-why-your-website-might-be-invisible-to-ai-in-2026-df7
**Pain point:** AI invisibility explainer

**REPLY:**
```
good writeup. one angle id add: bilingual/multilingual sites are disproportionately affected by this.

im researching canadian ecommerce stores that run fr/en and the ai visibility is close to zero for most of them. the models cant resolve hreflang page pairs, french training data representation is tiny (~0.16% in some models), and a lot of these stores have cdns blocking ai crawlers without realizing.

structured data helps but it doesnt solve the fundamental language resolution problem. feels like a gap in the geo tooling space
```

---

### 24. AEO, GEO, and LLMO: The New Frontier of SEO in the Age of AI
**URL:** https://dev.to/lovestaco/aeo-geo-and-llmo-the-new-frontier-of-seo-in-the-age-of-ai-4bbj
**Pain point:** AEO/GEO framework discussion

**REPLY:**
```
solid overview. one thing thats missing from most aeo/geo discussions: what happens when your site serves content in multiple languages?

ive been looking at this for canadian ecommerce (fr/en bilingual stores) and its a mess. llms cant figure out hreflang page pairs, they either cite the wrong language version or skip both. and french content gets way less recall because its such a small percentage of training data.

feels like everyone assumes single-language english sites when talking about geo. the multilingual angle is a whole different problem that nobody has good answers for yet
```

---

## SHOPIFY DEV COMMUNITY REPLIES

---

### 25. Adding LLMs.txt file to Shopify store
**URL:** https://community.shopify.dev/t/adding-llms-txt-file-to-shopify-store/19276
**Pain point:** llms.txt implementation

**REPLY:**
```
llms.txt is a good start but from my testing its only part of the puzzle. the bigger issues for most stores are:

1. ai crawlers getting blocked at the cdn/waf level (not just robots.txt)
2. structured data being too basic, most themes only ship with minimal schema
3. for bilingual stores, the hreflang setup confusing the models about which page to cite

ive been testing this specifically with canadian fr/en stores and the bilingual problem is the hardest one to solve. llms.txt helps with brand context but it doesnt fix the language resolution issue.

anyone here running a multilingual store and tried llms.txt? curious if it moved the needle for you
```

---

### 26. AI Feed Compliance for ChatGPT Shopping - Looking for Feedback
**URL:** https://community.shopify.dev/t/just-launched-on-shopify-ai-feed-compliance-for-chatgpt-shopping-looking-for-feedback/27145
**Pain point:** ChatGPT shopping compliance

**REPLY:**
```
cool app. curious how it handles bilingual/multilingual stores? specifically fr/en canadian stores with hreflang page pairs.

ive been researching this and one of the biggest gaps i see is that ai engines cant resolve which language version of a product page to cite when theres multiple versions. does your compliance check flag that as an issue or is it more focused on the feed structure itself?

also wondering if you check for cdn-level blocking of ai crawlers, not just robots.txt. ive found a lot of stores where robots.txt is clean but cloudflare is returning 403s to GPTBot
```

---

### 27. 500 Internal Server Errors for ChatGPT & AI Bots
**URL:** https://community.shopify.com/t/500-internal-server-errors-for-chatgpt-ai-bots/415017
**Pain point:** AI crawlers hitting errors

**REPLY:**
```
this is more common than people think. ive been checking this across a bunch of stores and the 403/500 errors for ai bots come from a few places:

- cdn/waf settings (cloudflare, akamai etc) blocking bot traffic
- rate limiting configs that are too aggressive for ai crawlers
- security apps on shopify that flag GPTBot and similar as suspicious

the frustrating part is your store can look totally fine from a regular browser but ai crawlers see a completely different response. worth checking your server logs specifically for requests from GPTBot, OAI-SearchBot, and PerplexityBot user agents
```

---

### 28. Feature request: Support for llms.txt (AI crawler management)
**URL:** https://community.shopify.com/t/feature-request-support-for-llms-txt-ai-crawler-management/422216/2
**Pain point:** llms.txt feature request

**REPLY:**
```
+1 on this. llms.txt support being native to shopify would be huge.

right now the apps that do it are fine but having it built into the platform would mean way more stores actually set it up. most merchants dont even know their stores are invisible to ai search engines.

one thing id add to the feature request: native handling of multilingual llms.txt for stores running multiple languages. the bilingual problem (especially fr/en for canadian stores) is one of the biggest gaps in ai visibility right now and having shopify handle the language routing natively would save a lot of headaches
```

---

## REDDIT SEARCH TERMS
**(Reddit is blocked for me, search these yourself and post replies)**

Search in r/shopify, r/ecommerce, r/SEO, r/bigseo, r/canadabusiness:

1. `AI search visibility shopify` in r/shopify
2. `ChatGPT product recommendations ecommerce` in r/ecommerce
3. `bilingual SEO Canada french english` in r/SEO
4. `GEO generative engine optimization` in r/bigseo
5. `Canadian ecommerce AI` in r/canadabusiness
6. `shopify ChatGPT integration` in r/shopify
7. `llms.txt structured data ecommerce` in r/SEO
8. `perplexity shopping ecommerce` in r/ecommerce

**Template Reddit reply (adapt to thread context):**
```
been looking into this for a school project. ive been testing how ecommerce brands (mostly canadian) show up across chatgpt, perplexity, etc.

tldr: most stores ranking well on google are invisible on ai search. chatgpt runs on bing not google, a lot of stores block ai crawlers at the CDN level without knowing, and structured data matters way more for ai citations than traditional seo.

for bilingual fr/en stores its even worse, the models cant figure out which page version to recommend so they skip both.

if anyone wants i could use more test cases for my research, happy to check your store
```

---

## STATUS SUMMARY

| # | Platform | Target | Status |
|---|----------|--------|--------|
| 1 | Shopify Community | AI search visibility thread /599726 | DRAFT READY |
| 2 | Shopify Community | ChatGPT/Claude/Perplexity fix /593006 | DRAFT READY |
| 3 | Shopify Community | ChatGPT product results /579646 | DRAFT READY |
| 4 | Shopify Community | LLM optimization /566409 | DRAFT READY |
| 5 | Shopify Community | AI-driven product discovery /422405 | DRAFT READY |
| 6 | Shopify Community | Urgent AI search help /421532 | DRAFT READY |
| 7 | Shopify Community | Product schema AI /584394 | DRAFT READY |
| 8 | Shopify Community | Multi-language SEO /2461572 | DRAFT READY |
| 9 | Shopify Community | ChatGPT goldmine /420191 | DRAFT READY |
| 10 | Shopify Community | AI visibility question /587072 | DRAFT READY |
| 11 | Indie Hackers | AI Visibility New SEO | DRAFT READY |
| 12 | Indie Hackers | Potatometer/distribution moat | DRAFT READY |
| 13 | LinkedIn | Jasmine Bouchard @ RUDSAK | DRAFT READY (CONFIRMED) |
| 14 | LinkedIn | Alain Parenteau @ ALDO | DRAFT READY (VERIFY FIRST) |
| 15 | LinkedIn | Michael Bliah @ Groupe Dynamite | DRAFT READY (VERIFY FIRST) |
| 16 | LinkedIn | CMO @ Mackage/APP Group | TEMPLATE (FIND NAME FIRST) |
| -- | Reddit | 8 search terms provided | YOU SEARCH + USE TEMPLATE |
| 17 | Hacker News | GEO rewrites the rules of search | DRAFT READY |
| 18 | Hacker News | Searchable AI visibility index (15k brands) | DRAFT READY |
| 19 | Hacker News | AI found us before Google did | DRAFT READY |
| 20 | Hacker News | What is GEO and why is no one building in it? | DRAFT READY |
| 21 | Hacker News | Show HN: Geneo brand visibility tracker | DRAFT READY |
| 22 | Hacker News | Show HN: We built a GEO tool | DRAFT READY |
| 23 | Dev.to | GEO: Why your site is invisible to AI in 2026 | DRAFT READY |
| 24 | Dev.to | AEO, GEO, and LLMO: New frontier of SEO | DRAFT READY |
| 25 | Shopify Dev | Adding llms.txt file to Shopify store | DRAFT READY |
| 26 | Shopify Dev | AI Feed Compliance for ChatGPT Shopping | DRAFT READY |
| 27 | Shopify Community | 500 errors for ChatGPT & AI bots | DRAFT READY |
| 28 | Shopify Community | Feature request: llms.txt support | DRAFT READY |

---

## POSTING STRATEGY

- **shopify community:** need a shopify account to post. if you dont have one make a free dev store. do max 2-3 per day, not all at once
- **shopify dev community:** separate account from regular shopify community. more technical audience, lean into the dev angle
- **indie hackers:** just log in and reply. both are good to post same day
- **hacker news:** use your existing HN account. HN crowd is technical so keep it data-driven, less "student" more "researcher". dont overpost, 1-2 per day max. HN will downvote anything that smells like self-promotion
- **dev.to:** create account if you dont have one. dev audience, keep it technical. good place to also write your own post eventually about the bilingual findings
- **linkedin:** verify each contact is still at the company first. space them out, 1 connection request per day
- **reddit:** use your personal account. new accounts get flagged. adapt the template to each thread
- **if people respond:** keep the same casual tone. if they want you to check their store, get their url and run it through the tool. frame it as "yeah totally, always looking for more data for my research"

## SUGGESTED POSTING ORDER (spread over 1-2 weeks)

**Day 1-2:** Shopify Community (3 threads) + 1 Indie Hackers
**Day 3-4:** Hacker News (2 threads) + Shopify Dev (1 thread)
**Day 5-6:** Shopify Community (3 more) + Dev.to (1 thread) + 1 LinkedIn connection
**Day 7-8:** Hacker News (2 more) + Shopify Community (2 more) + 1 LinkedIn connection
**Day 9-10:** Remaining Shopify Community + Shopify Dev + Indie Hackers #2 + LinkedIn connections
**Ongoing:** Reddit (as you find threads) + LinkedIn follow-ups as people accept
