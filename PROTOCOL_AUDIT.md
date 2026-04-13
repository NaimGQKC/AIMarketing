# Protocol Audit: ACP Remediation

**Date:** 2026-04-13
**Issue:** 1 of 4 — Deprecated ACP Protocol Remediation
**Auditor:** Automated remediation sprint

---

## Summary

All references to "ACP" (Agentic Commerce Protocol / OpenAI ACP) have been replaced across the codebase. The deprecated ACP protocol has been replaced with MCP (Model Context Protocol, Anthropic) for agent-to-agent communication and tool integration contexts, and with GPTBot crawlability language for OpenAI-specific claims. UCP (Universal Commerce Protocol) references remain untouched as they are current and correct.

**Total files modified:** 8
**Rule 1 (MCP) applications:** 18
**Rule 2 (UCP keep as-is):** 0 modifications (all UCP references preserved)
**Rule 3 (A2A) applications:** 0 (no inter-agent orchestration contexts found)
**Rule 4 (GPTBot crawlability) applications:** 3
**REVIEW NEEDED items:** 0

---

## Change Log

### File: IDEA.txt
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 15 | `UCP/ACP feeds to talk directly to Google/OpenAI protocols` | `UCP feeds for Google, MCP-compatible structured data (MCP is the dominant standard -- 97M+ monthly SDK downloads, governed by Linux Foundation Agentic AI Foundation), and optimization for GPTBot crawlability and Bing IndexNow submission` | 1 + 4 |

### File: TWITTER_OUTREACH_STRATEGY.md
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 343 | `emerging ACP feeds let you push structured data directly to AI systems` | `MCP-compatible structured feeds (MCP is the dominant standard -- 97M+ monthly SDK downloads, governed by Linux Foundation Agentic AI Foundation) let you push structured data directly to AI systems` | 1 |

### File: src/pages/Connect.jsx
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 66 | `UCP / ACP` | `UCP / MCP` (with MCP annotation comment) | 1 |

### File: server/routers/dashboard.py
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 166 | `UCP/ACP connection health` | `UCP/MCP connection health` (with MCP annotation comment) | 1 |
| 183 | `ACP (OpenAI)` | `MCP (Anthropic)` | 1 |

### File: server/engines/verification.py
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 50 | `verified feeds (UCP/ACP)` | `verified feeds (UCP/MCP)` | 1 |

### File: server/engines/ingest_parser.py
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 229 | `"ucp", "acp"` | `"ucp", "mcp"` (with MCP annotation comment) | 1 |

### File: server/engines/eee_engine.py
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 83 | `"acp_feed", # Agentic Commerce Protocol (OpenAI)` | `"mcp_feed", # MCP (Model Context Protocol, Anthropic) -- dominant standard, 97M+ monthly SDK downloads` | 1 |
| 266 | `"acp_feed": { "action": "Publish ACP feed for OpenAI shopping agent discovery"` | `"mcp_feed": { "action": "Publish MCP-compatible feed optimized for GPTBot crawlability and Bing IndexNow submission"` | 1 + 4 |
| 269 | `acp.json` | `mcp.json` | 1 |
| 270 | `"payload_type": "acp_feed"` | `"payload_type": "mcp_feed"` | 1 |
| 439 | `(UCP, ACP, JSON-LD)` | `(UCP, MCP, JSON-LD)` | 1 |
| 525 | `"acp_feed": "Refresh updated_at field"` | `"mcp_feed": "Refresh updated_at field"` | 1 |
| 538 | `Refresh ACP feed updated_at` | `Refresh MCP feed updated_at` | 1 |
| 725 | `"acp": { ... "consumer": "OpenAI Operator / ChatGPT Shopping", "advantage": "Agentic Commerce Protocol -- native shopping agent format" }` | `"mcp": { ... "consumer": "Optimized for GPTBot crawlability and Bing IndexNow submission", "advantage": "MCP (Model Context Protocol) -- dominant agent-to-agent standard" }` | 1 + 4 |
| 727 | `acp.json` | `mcp.json` | 1 |
| 803 | `Publish ACP feed for OpenAI shopping agents` | `Publish MCP-compatible feed optimized for GPTBot crawlability and Bing IndexNow submission` | 1 + 4 |
| 991 | `Tier 2 URI (UCP/ACP feed)` | `Tier 2 URI (UCP/MCP feed)` | 1 |

### File: server/engines/remediation.py
| Line | Old Text | New Text | Rule |
|------|----------|----------|------|
| 500 | `"target_protocols": ["UCP", "ACP"]` | `"target_protocols": ["UCP", "MCP"]` (with MCP annotation comment) | 1 |
| 633 | `# ACP Feed Formatting` | `# MCP Feed Formatting` | 1 |
| 636 | `def format_acp_feed(...)` | `def format_mcp_feed(...)` (with updated docstring and MCP annotation) | 1 |
| 637 | `Format product data for OpenAI ACP (Agentic Commerce Protocol) discovery feed` | `Format product data for MCP (Model Context Protocol, Anthropic) compatible discovery feed` | 1 |
| 660 | `"protocol": "acp"` | `"protocol": "mcp"` | 1 |

---

## Intentionally Unchanged References

### "Agentic Commerce" (general concept, not the ACP protocol)
These references use "Agentic Commerce" as a general industry term (not the deprecated ACP protocol name) and were intentionally left unchanged:

- **src/pages/Roadmap.jsx:541** -- `{/* Agentic Commerce Priority */}` (JSX comment, section label)
- **src/pages/Roadmap.jsx:547** -- `Agentic Commerce Priority` (UI label text)
- **src/pages/Roadmap.css:695** -- `/* Agentic Commerce Priority */` (CSS comment)
- **server/routers/eee.py:111** -- `Agentic Commerce priority map` (docstring)
- **server/engines/eee_engine.py:652** -- `AGENTIC COMMERCE PRIORITY` (section header comment)
- **server/engines/eee_engine.py:1598** -- `Compute Agentic Commerce priority` (docstring)
- **PRODUCT_HUNT_LAUNCH_PLAN.md:28** -- `"agentic commerce" narrative` (industry trend reference)
- **PRODUCT_HUNT_LAUNCH_PLAN.md:644** -- Fortune article title about Agentic Commerce (external URL/title)

**Rationale:** "Agentic Commerce" is a valid industry concept describing AI-agent-driven commerce; it is distinct from the specific deprecated "ACP" (Agentic Commerce Protocol) from OpenAI. These references describe the domain, not the protocol.

---

## Verification

Final grep for `ACP`, `Agentic Commerce Protocol`, and `OpenAI ACP` returned **zero matches** across the entire codebase. All deprecated protocol references have been successfully remediated.

UCP references verified intact -- all `/.well-known/ucp` manifests and UCP mentions remain unchanged.
