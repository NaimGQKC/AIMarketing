# Remediation Log

## Issue 1 — ACP Protocol
- IDEA.txt:15 — "UCP/ACP feeds to talk directly to Google/OpenAI protocols" → "UCP feeds for Google, MCP-compatible structured data (MCP is the dominant standard...), and optimization for GPTBot crawlability and Bing IndexNow submission" (rule 1 + 4)
- TWITTER_OUTREACH_STRATEGY.md:343 — "emerging ACP feeds" → "MCP-compatible structured feeds (MCP is the dominant standard...)" (rule 1)
- src/pages/Connect.jsx:66 — "UCP / ACP" → "UCP / MCP" (rule 1)
- server/routers/dashboard.py:166 — "UCP/ACP connection health" → "UCP/MCP connection health" (rule 1)
- server/routers/dashboard.py:183 — "ACP (OpenAI)" → "MCP (Anthropic)" (rule 1)
- server/engines/verification.py:50 — "verified feeds (UCP/ACP)" → "verified feeds (UCP/MCP)" (rule 1)
- server/engines/ingest_parser.py:229 — "acp" → "mcp" in authoritative patterns list (rule 1)
- server/engines/eee_engine.py:83 — "acp_feed" → "mcp_feed" identifier + comment updated (rule 1)
- server/engines/eee_engine.py:266 — "acp_feed" dict key → "mcp_feed", action text updated to MCP + GPTBot (rule 1 + 4)
- server/engines/eee_engine.py:269 — "acp.json" URI → "mcp.json" (rule 1)
- server/engines/eee_engine.py:270 — "payload_type": "acp_feed" → "mcp_feed" (rule 1)
- server/engines/eee_engine.py:439 — "(UCP, ACP, JSON-LD)" → "(UCP, MCP, JSON-LD)" (rule 1)
- server/engines/eee_engine.py:525 — "acp_feed" timestamp key → "mcp_feed" (rule 1)
- server/engines/eee_engine.py:538 — "Refresh ACP feed updated_at" → "Refresh MCP feed updated_at" (rule 1)
- server/engines/eee_engine.py:725 — "acp" dict key → "mcp", consumer/advantage text updated to MCP + GPTBot (rule 1 + 4)
- server/engines/eee_engine.py:727 — "acp.json" URI → "mcp.json" (rule 1)
- server/engines/eee_engine.py:803 — "Publish ACP feed for OpenAI shopping agents" → "Publish MCP-compatible feed optimized for GPTBot crawlability and Bing IndexNow submission" (rule 1 + 4)
- server/engines/eee_engine.py:991 — "(UCP/ACP feed)" → "(UCP/MCP feed)" (rule 1)
- server/engines/remediation.py:500 — "target_protocols": ["UCP", "ACP"] → ["UCP", "MCP"] (rule 1)
- server/engines/remediation.py:633 — "# ACP Feed Formatting" → "# MCP Feed Formatting" (rule 1)
- server/engines/remediation.py:636 — "format_acp_feed" → "format_mcp_feed" function rename (rule 1)
- server/engines/remediation.py:637 — docstring updated from "OpenAI ACP (Agentic Commerce Protocol)" → "MCP (Model Context Protocol, Anthropic)" (rule 1)
- server/engines/remediation.py:660 — "protocol": "acp" → "protocol": "mcp" (rule 1)

## Issue 2 — Probing Volume Tiers
- server/config.py:25 — Changed PROBE_ITERATIONS default from 3 to 50 (standard tier)
- server/config.py:31-42 — Added PROBE_TIER config and PROBE_TIER_MAP (scout/standard/enterprise) with statistical rationale comment
- server/engines/inference_lab.py:1-17 — Updated module docstring to describe tiered probe volumes instead of hardcoded N=3
- server/engines/inference_lab.py:26 — Added PROBE_TIER, PROBE_TIER_MAP to config imports
- server/engines/inference_lab.py:44-68 — Added resolve_probe_tier() helper function with statistical rationale docstring
- server/engines/inference_lab.py:78-83 — Updated build_golden_set docstring to reference tier-based N
- server/engines/inference_lab.py:440-467 — Updated run_probe_task: added probe_tier param, resolve tier to get iterations, default iterations from tier
- server/engines/inference_lab.py:569 — Added probe_tier to summary dict returned by run_probe_task
- server/models.py:99-105 — Updated ProbeRequest: iterations now Optional (default None, derived from tier), added probe_tier field
- server/routers/diagnose.py:15 — Added resolve_probe_tier import
- server/routers/diagnose.py:208-253 — Updated start_probe endpoint: resolves tier, computes effective iterations, passes probe_tier to run_probe_task, returns probe_tier and ci_label in response
- server/engines/verification.py:556-562 — Updated run_audit: uses resolve_probe_tier("scout") for audit re-probes instead of hardcoded 3 iterations
- src/api/client.js:49-59 — Updated probe() API call: iterations default null, added probeTier param (default "standard")
- src/pages/Verify.jsx:50-95 — Added PROBE_TIER_BADGES config and StatisticalConfidenceBadge component (scout/standard/enterprise badges with tooltips)
- src/pages/Verify.jsx:252 — Added probeTier state variable (default "standard")
- src/pages/Verify.jsx:279 — Reads probe_tier from efficiency response if present
- src/pages/Verify.jsx:330-332 — Rendered StatisticalConfidenceBadge inline in E-Score card

## Issue 3 — Token Decay Narrative

### (a) Decouple JSON-LD from token decay
- IDEA.txt:15 — "Bilingual JSON-LD to stop French token decay" → "Bilingual JSON-LD to improve entity recognition and fact density for AI extraction [...] Truth Clips bypass text tokenization entirely by anchoring brand identity in language-agnostic visual embeddings."
- PRODUCT_HUNT_LAUNCH_PLAN.md:108 — JSON-LD Fix Kit description reframed from "eliminates token waste" to "improves entity recognition and fact density for AI extraction"
- PRODUCT_HUNT_LAUNCH_PLAN.md:338 — Decoupled: JSON-LD for entity recognition, Truth Clips for tokenization bypass
- PRODUCT_HUNT_LAUNCH_PLAN.md:347 — "token decay problem and JSON-LD Fix Kit approach" → separate framing
- PRODUCT_HUNT_LAUNCH_PLAN.md:411 — "diagnoses bilingual token decay, generates JSON-LD Fix Kits" → "measures bilingual tokenization premium, generates JSON-LD Fix Kits for entity recognition"
- PRODUCT_HUNT_LAUNCH_PLAN.md:501 — "eliminates token waste" → "improves entity recognition and fact density"
- CONTENT-STRATEGY.md:1325 — "French token decay, bilingual JSON-LD implementation" → "French tokenization premium, bilingual JSON-LD implementation for entity recognition"
- sales-operations-playbook.md:791 — "How would bilingual JSON-LD structured data solve the token decay" → "How would bilingual JSON-LD structured data improve entity recognition to address the tokenization premium"
- server/engines/bilingual_bridge.py:165 — "Generate bilingual JSON-LD with high-density French tokens that prevent LLM reasoning decay" → "Generate bilingual JSON-LD that improves entity recognition and fact density for AI extraction"
- partnership-strategy.md:600 — Added "improve entity recognition and" to JSON-LD Fix Kit description

### (b) Truth Clip Kit framing
- src/pages/Remediate.jsx:22 — "Cross-modal attention bypasses O(n²) French token decay via visual grounding" → "Bypasses text tokenization entirely by anchoring brand identity in language-agnostic visual embeddings"
- server/engines/remediation.py:13 — "Cross-modal attention anchoring for French token decay bypass" → "Bypasses text tokenization entirely via language-agnostic visual embeddings"
- server/engines/remediation.py:316 — "Cross-modal attention layers redirect French token decay queries to stable visual space" → "redirect French queries to stable visual space, sidestepping text tokenization"
- server/engines/remediation.py:510 — "Bypasses French Token Decay via cross-modal attention grounding" → "Bypasses text tokenization entirely by anchoring brand identity in language-agnostic visual embeddings"
- server/engines/verification.py:382 — "Cross-modal attention bypasses French token brittleness" → "Bypasses text tokenization entirely via language-agnostic visual embeddings"
- server/engines/eee_engine.py:860 — "Bypasses Token Decay gaps" → "Bypasses text tokenization entirely"
- server/engines/eee_engine.py:1455 — "Truth Clips bypass this by anchoring in visual vector space" → "Truth Clips sidestep this by anchoring brand identity in language-agnostic visual embeddings"

### (c) Terminology rename
- src/context/LanguageContext.jsx:54 — "Token Decay" → "Tokenization Premium" (EN)
- src/context/LanguageContext.jsx:97 — "Token Decay Factor (δ)" → "Token Fertility Factor (δ)" (EN)
- src/context/LanguageContext.jsx:165 — "Décroissance de jetons" → "Prime de tokenisation" (FR)
- src/context/LanguageContext.jsx:208 — "Facteur de décroissance (δ)" → "Facteur de fertilité des jetons (δ)" (FR)
- src/pages/Verify.jsx:33 — "No Token Decay" → "No tokenization premium"
- src/pages/Verify.jsx:640 — "Token Decay penalty" → "tokenization premium (Token Fertility ratio; Petrov et al., NeurIPS 2023)"
- src/pages/Verify.jsx:374 — "decay" badge → "premium" badge
- src/pages/Remediate.jsx:265 — "French Token Decay" → "Tokenization Premium"
- src/pages/Diagnose.jsx:239-240 — Maps "Token Decay" to display "Tokenization Premium"
- src/pages/Roadmap.jsx:221 — "Token Tax:" → "Tokenization Premium:"
- server/engines/verification.py:248 — "Token Decay Factor" → "Token Fertility Factor (per Petrov et al. 2023)"
- server/engines/verification.py:374 — "Token Decay" → "Tokenization Premium bypass"
- server/routers/verify.py:192 — "Token Decay Factor" → "Token Fertility Factor (tokenization premium)"
- server/engines/eee_engine.py:858 — "Token Decay Factor delta" → "Token Fertility Factor delta"
- server/engines/eee_engine.py:1434 — "Token tax" comment → "Tokenization premium"
- server/engines/bilingual_bridge.py:83 — "Token Tax" comment → "Tokenization Premium"
- server/engines/inference_lab.py:631 — return "Token Decay" → return "Tokenization Premium"
- server/engines/remediation.py:406 — "French Token Decay triggers" → "French tokenization premium triggers"
- server/engines/remediation.py:411 — "tokenDecayBypass" → "tokenizationBypass"
- server/engines/remediation.py:536 — "token_decay_bypass" → "tokenization_bypass"
- server/database.py:64 — comment updated to document "Tokenization Premium" as primary, "Token Decay" as legacy
- server/engines/batch_analyzer.py:335 — Added "Tokenization Premium": "truthClip" alongside legacy key
- server/engines/eee_engine.py:1533 — Added "Tokenization Premium": 0.5 alongside legacy key
- server/engines/remediation.py:450 — accepts both "Token Decay" and "Tokenization Premium"
- server/engines/remediation.py:551 — Added "Tokenization Premium": 35 alongside legacy key
- IDEA.txt:6 — "Token Decay in French" → "tokenization premium on French (Token Fertility ratio, Petrov et al. 2023)"
- TWITTER_OUTREACH_STRATEGY.md:59 — "severe 'token decay'" → "real, measurable tokenization premium"
- TWITTER_OUTREACH_STRATEGY.md:13 — "French token decay problem" → "French tokenization premium problem"
- TWITTER_OUTREACH_STRATEGY.md:209 — "Token Decay is Real" → "The Tokenization Premium is Real"
- TWITTER_OUTREACH_STRATEGY.md:576 — "#TokenDecay" → "#TokenizationPremium"
- PRODUCT_HUNT_LAUNCH_PLAN.md — 14 occurrences of "token decay" → "tokenization premium" across PH copy, HN post, descriptions
- CONTENT-STRATEGY.md — 18 occurrences: keyword tables, article titles, whitepaper names, lead magnets, landing page copy, meta descriptions, schema.org markup
- sales-operations-playbook.md — 13 occurrences: scoring tables, prompt templates, variable names, sequence names, report templates
- earned-media-outreach-strategy.md — 13 occurrences: podcast pitches, article pitches, email templates, talk proposals
- linkedin-outreach-playbook.md — 7 occurrences: DM templates, post titles, group engagement, persona descriptions
- partnership-strategy.md — 8 occurrences: partner pitches, value propositions, enablement materials
- design-partner-prospecting-list.md — 5 occurrences: prospecting notes, talking points
- outreach-sequences.md — 5 occurrences: sequence names, email body copy
- scary-report-templates.md:422 — "Bilingual Token Decay" → "Bilingual Tokenization Premium"
- TECHNICAL_COMMUNITY_STRATEGY.md — 6 occurrences: community posts, blog post titles, repo READMEs
- TOMORROW-ACTION-PLAN.md:226 — "French token decay finding" → "French tokenization premium finding"
- reddit-outreach-targets.md — 2 occurrences: target names, descriptions

### (d) Tooltip/info modal additions
- src/context/LanguageContext.jsx:88 — tokenFertilityDesc EN updated to: "Measures the tokenization cost premium of your French content vs. English. French typically shows a 1.1-1.5x premium over English for general content, with specialized vocabulary experiencing higher ratios. Research: Petrov et al. 2023, Lundin et al. 2025."
- src/context/LanguageContext.jsx:199 — tokenFertilityDesc FR updated with equivalent research citation
- src/pages/Verify.jsx:640 — Formula proof block now cites "(Token Fertility ratio; Petrov et al., NeurIPS 2023)"
- TECHNICAL_COMMUNITY_STRATEGY.md:69 — E-Score description now cites "Token Fertility factor (Petrov et al., NeurIPS 2023)"

### (e) Soften alarming language
- TWITTER_OUTREACH_STRATEGY.md:59 — "severe 'token decay'" → "real, measurable tokenization premium"
- sales-operations-playbook.md:38 — "causes severe token decay" → "incurs a real, measurable tokenization premium"
- earned-media-outreach-strategy.md:165 — "systematic failure we call 'French AI Token Decay'" → "systematic, measurable tokenization premium we call the 'French AI Token Tax'"
- No instances of "catastrophic token" or "token collapse" found (verified zero hits)

## Issue 4 — Proprietary Terminology Anchoring

### Rule A — "Inference Gap" academic anchoring (first use per file)
- IDEA.txt:1 — "The 'Inference Gap'" → "The 'Inference Gap' (the phenomenon where AI recommends competitors while using your content as a citation source — documented across 541K+ LLM responses by Seer Interactive)" (rule A)
- index.html:6 — "Close the inference gap between" → "Close the inference gap — where AI recommends competitors while using your content as a citation source — between" (rule A)

### Rule B — "Montreal Wedge" removal from customer-facing materials
- IDEA.txt:6 — "(The Montreal Wedge)" → "(the French AI Visibility Gap)" (rule B)
- server/engines/bilingual_bridge.py:78 — KEPT: code comment, allowed per rule B

### Rule C — "Toxic Citations" academic anchoring (first use per file)
- IDEA.txt:4 — "Toxic Citations: Agents prioritize" → "Toxic Citations — stale third-party content (Reddit threads, outdated reviews) that AI prioritizes over your live product data: Agents prioritize" (rule C)
- CONTENT-STRATEGY.md:149 — "Toxic citations, missing structured data" → "Toxic citations — stale third-party content (Reddit threads, outdated reviews) that AI prioritizes over your live product data — missing structured data" (rule C)

### Rule D — "Inference Alignment Score" academic anchoring (first use per file)
- IDEA.txt:17 — "the Inference Alignment Score has increased" → "the Inference Alignment Score (measures how accurately AI systems represent your brand across languages, using methodology adapted from GEO visibility research, Princeton, 2024) has increased" (rule D)
- outreach-sequences.md:50 — "Inference Alignment Scale" → appended "(measures how accurately AI systems represent your brand across languages, using methodology adapted from GEO visibility research, Princeton, 2024)" (rule D)
- TWITTER_OUTREACH_STRATEGY.md:64 — "Inference Alignment scores jump" → appended anchoring parenthetical (rule D)
- CONTENT-STRATEGY.md:253 — "Inference Alignment Score from 30% to 82%" → appended anchoring parenthetical (rule D)
- scary-report-templates.md:17 — Added anchoring blockquote after "Inference Alignment Score (Hero Metric)" heading (rule D)
- sales-operations-playbook.md:465 — "Inference Alignment Score (EN)" → appended em-dash anchoring on first use (rule D)
- src/context/LanguageContext.jsx:14 — EN dashboardSubtitle appended "measuring how accurately AI systems represent your brand, adapted from GEO visibility research (Princeton, 2024)" (rule D)
- src/context/LanguageContext.jsx:125 — FR dashboardSubtitle appended equivalent French anchoring (rule D)

### Rule E — "Bilingual Crisis" softened in customer-facing materials
- PRODUCT_HUNT_LAUNCH_PLAN.md:79 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- PRODUCT_HUNT_LAUNCH_PLAN.md:319 — "bilingual crisis" → "bilingual AI gap" (rule E)
- PRODUCT_HUNT_LAUNCH_PLAN.md:485 — "The Bilingual Crisis:" → "The Bilingual AI Gap:" (rule E)
- CONTENT-STRATEGY.md:156 — "The Bilingual Crisis:" → "The Bilingual AI Gap:" in blog title (rule E)
- CONTENT-STRATEGY.md:419 — "The Bilingual Crisis" → "The Bilingual AI Gap" in calendar table (rule E)
- CONTENT-STRATEGY.md:514 — "The Bilingual Crisis in AI Search" → "The Bilingual AI Gap in AI Search" in whitepaper outline (rule E)
- CONTENT-STRATEGY.md:1242 — "the 'Bilingual Crisis'" → "the 'bilingual visibility problem'" in llms.txt (rule E)
- linkedin-outreach-playbook.md:2 — "Bilingual Crisis" → "Bilingual AI Gap" in subtitle (rule E)
- design-partner-prospecting-list.md:2 — "Bilingual Crisis Opportunity" → "Bilingual AI Gap Opportunity" (rule E)
- design-partner-prospecting-list.md:151 — "bilingual crisis" → "bilingual AI gap" (rule E)
- design-partner-prospecting-list.md:178 — "The Bilingual Crisis pitch" → "The Bilingual AI Gap pitch" (rule E)
- earned-media-outreach-strategy.md:35 — "bilingual crisis" → "bilingual visibility problem" in pitch angle (rule E)
- earned-media-outreach-strategy.md:80 — "bilingual crisis" → "bilingual AI gap" (rule E)
- earned-media-outreach-strategy.md:194 — "the 'Bilingual Crisis'" → "the 'Bilingual AI Gap'" in email template (rule E)
- earned-media-outreach-strategy.md:378 — "Canadian Bilingual Crisis" → "Canadian Bilingual AI Gap" in pitch (rule E)
- earned-media-outreach-strategy.md:425 — "The Bilingual Crisis:" → "The Bilingual AI Gap:" in article title (rule E)
- earned-media-outreach-strategy.md:537 — "The Bilingual Crisis:" → "The Bilingual AI Gap:" in talk pitch (rule E)
- reddit-outreach-targets.md:61 — "the Bilingual Crisis" → "the bilingual visibility problem" (rule E)
- reddit-outreach-targets.md:81 — "the 'Bilingual Crisis'" → "the 'bilingual visibility problem'" (rule E)
- reddit-outreach-targets.md:87 — "the 'Bilingual Crisis'" → "the 'Bilingual AI Gap'" in DM template (rule E)
- TWITTER_OUTREACH_STRATEGY.md:13 — "Bilingual Crisis" → "Bilingual AI Gap" in target notes (rule E)
- TWITTER_OUTREACH_STRATEGY.md:34 — "Bilingual Crisis" → "Bilingual AI Gap" in target notes (rule E)
- TWITTER_OUTREACH_STRATEGY.md:42 — "Bilingual Crisis" → "Bilingual AI Gap" in target notes (rule E)
- TWITTER_OUTREACH_STRATEGY.md:146 — "Bilingual Crisis" → "Bilingual AI Gap" in DM template (rule E)
- TWITTER_OUTREACH_STRATEGY.md:186 — "The Bilingual Crisis" → "The Bilingual AI Gap" in thread title (rule E)
- TWITTER_OUTREACH_STRATEGY.md:234 — "the 'Bilingual Crisis'" → "the 'Bilingual AI Gap'" in tweet (rule E)
- TWITTER_OUTREACH_STRATEGY.md:260 — "The Bilingual Crisis" → "The Bilingual AI Gap" in tweet (rule E)
- TWITTER_OUTREACH_STRATEGY.md:385 — "the 'Bilingual Crisis'" → "the 'Bilingual AI Gap'" in tweet (rule E)
- TWITTER_OUTREACH_STRATEGY.md:427 — "the Bilingual Crisis" → "the Bilingual AI Gap" in tweet (rule E)
- TWITTER_OUTREACH_STRATEGY.md:447 — "The Bilingual Crisis" → "The Bilingual AI Gap" in tweet (rule E)
- TWITTER_OUTREACH_STRATEGY.md:651 — "Bilingual Crisis" → "Bilingual AI Gap" in checklist (rule E)
- TECHNICAL_COMMUNITY_STRATEGY.md:338 — "the Bilingual Crisis" → "the Bilingual AI Gap" (rule E)
- TECHNICAL_COMMUNITY_STRATEGY.md:679 — "The Bilingual Crisis in AI Search" → "The Bilingual AI Gap in AI Search" (rule E)
- scary-report-templates.md:279 — "The Bilingual Crisis" → "The Bilingual AI Gap" in tweet label (rule E)
- scary-report-content-MACKAGE.md:75 — "Bilingual Crisis" → "Bilingual AI Gap" in section header (rule E)
- RESOURCES-LEAD-GEN.md:50 — "Bilingual Crisis Report" → "Bilingual AI Gap Report" (rule E)
- RESOURCES-LEAD-GEN.md:88 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:109 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:126 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:138 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:149 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:180 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:192 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- RESOURCES-LEAD-GEN.md:228 — "Bilingual Crisis Score" → "Bilingual AI Gap Score" (rule E)
- RESOURCES-LEAD-GEN.md:249 — "Bilingual Crisis" → "Bilingual AI Gap" (rule E)
- server/routers/growth.py:180 — "Bilingual Crisis" → "Bilingual AI Gap" in email template string (rule E)
- server/routers/growth.py:807 — "Bilingual Crisis Report" → "Bilingual AI Gap Report" (rule E)
- server/routers/growth.py:849 — "Bilingual Crisis database" → "Bilingual AI Gap database" (rule E)

### Rule F — "the first" / "the only" claim review
- partnership-strategy.md:732 — "VisiMind is the only AI remediation layer" → "VisiMind is a specialized AI remediation layer" (rule F)
- design-partner-prospecting-list.md:188 — "VisiMind is the only tool that handles the French/English tokenization premium" → "VisiMind is a specialized measurement stack for the French/English tokenization premium" (rule F)
- Remaining "the only" instances verified as defensible: brand-audit-results.md (factual audit data), REAL-QUERY-RESULTS-MACKAGE.md (factual query data), REAL-QUERY-RESULTS-OTHERS.md (factual query data), scary-report-content-MACKAGE.md (factual), MASTER_COPY_PASTE_OUTREACH.md (general business observation), server/engines/eee_engine.py (internal code)
- Remaining "the first" instances verified as defensible or non-claims: partnership-strategy.md:39 (narrowly scoped to "first Shopify app for GEO remediation"), outreach-queue.md:207 and MASTER-OUTREACH-READY.md:246 (narrow "first agency in Montreal" positioning for prospect), all other uses are temporal/ordinal ("the first 2 hours", "the first diagnostic", "in the first place")

### Verification results
- "Montreal Wedge" in customer-facing files: 0 hits (only bilingual_bridge.py code comment remains — allowed)
- "Bilingual Crisis" in PRODUCT_HUNT_LAUNCH_PLAN.md: 0 hits
- "Bilingual Crisis" across all customer-facing files: 0 hits (only IDEA.txt internal doc retains original alongside softened parenthetical)
- "the only" remaining: all defensible (factual observations, internal code)
- "the first" remaining: all defensible (narrow claims, temporal/ordinal usage)
- "Inference Gap" anchored on first use in: IDEA.txt, index.html
- "Inference Alignment Score" anchored on first use in: IDEA.txt, outreach-sequences.md, TWITTER_OUTREACH_STRATEGY.md, CONTENT-STRATEGY.md, scary-report-templates.md, sales-operations-playbook.md, LanguageContext.jsx (EN+FR)
- "Toxic Citations" anchored on first use in: IDEA.txt, CONTENT-STRATEGY.md
