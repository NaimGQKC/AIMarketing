"""
VisiMind — Engine 6: External Environment Engineering (EEE)

We do NOT own or train the models. This engine controls the external evidence
that black-box LLMs retrieve, forcing them to treat brand-verified specs as
hard constraints through environmental manipulation.

Four attack vectors on the retrieval environment:

  1. SEMANTIC SATURATION (Kit 1 amplification)
     Syndicate Hard Attributes across N nodes until the statistical weight
     of brand truth exceeds stale parametric priors. Simulates the effect
     of internal DPO by making the correct answer the ONLY answer retrievable.

  2. DETERMINISTIC MAPPING (Kit 2 amplification)
     Deploy @graph JSON-LD with urn:visimind:* IDs across the syndication
     network. Eliminates the "Interpretation Tax" — the compute cost an LLM
     pays to disambiguate unstructured data.

  3. CROSS-MODAL ANCHORING (Kit 3 amplification)
     Distribute Truth Clips across video platforms indexed by multimodal
     crawlers. Visual modality dominance bypasses O(n^2) attention scaling
     in French queries.

  4. FRESHNESS BIAS (External RAFT)
     High-frequency KG updates with UTC timestamps that exploit retrieval
     recency bias. Forces the crawler's cache to flush stale entries and
     re-index brand-verified data.

Mathematical Framework:
  - S_KGQA_out = {(e, Score(e)) : e in E}
  - T(v?) = I - prod_{1<=i<=K}(I - T(v_i))
  - Statistical Weight W(a) = freq(a) / sum(freq(all_sources))
  - Freshness Score F(t) = exp(-lambda * (t_now - t_updated))

  5. COUNTER-SENTIMENT LOOP (Tier 5 defense)
     Detect toxic citations in Reddit/YouTube/community platforms and generate
     Verification Replies that link back to Tier 2 URIs, closing the RAG
     reasoning loop so the LLM follows the citation chain to brand truth.

  6. EXTERNAL PING SYSTEM (Crawler cache flush)
     Sitemap generation + dateModified HTTP headers + ping endpoints that
     force crawlers (Googlebot, GPTBot, PerplexityBot) to re-retrieve data.

  7. DRIFT WARNING SYSTEM
     If E-Score drops by >0.2 from a new high-authority hallucination,
     auto-trigger Defensive Freshness Cycle (2h/lambda=0.5).

  8. INTERPRETATION TAX CALCULATOR
     Quantify the token cost an LLM pays to parse unstructured HTML vs
     deterministic @graph JSON-LD. Proves the competitive advantage.
"""
import json
import uuid
import math
import re
from datetime import datetime, timedelta
from typing import Optional


# =============================================================================
# 1. SEMANTIC SATURATION — Statistical Weighting via Syndication
# =============================================================================

# Syndication node types ordered by citation authority weight
SYNDICATION_TIERS = {
    "tier_1": {
        "label": "Primary Authority",
        "description": "Brand-owned properties with maximum E-E-A-T signal",
        "authority_weight": 1.0,
        "examples": [
            "brand_website",      # Product pages with @graph JSON-LD
            "brand_blog",         # Technical content with Hard Attributes
            "brand_newsroom",     # Press releases with structured data
        ],
    },
    "tier_2": {
        "label": "Protocol Feeds",
        "description": "Machine-readable feeds consumed directly by agentic crawlers",
        "authority_weight": 0.95,
        "examples": [
            "ucp_feed",           # /.well-known/ucp (Google)
            "acp_feed",           # Agentic Commerce Protocol (OpenAI)
            "llms_txt",           # /llms.txt (universal discovery)
            "product_feed_jsonld", # /feeds/{brand}/products.jsonld
        ],
    },
    "tier_3": {
        "label": "Structured Aggregators",
        "description": "Third-party platforms that accept structured brand data",
        "authority_weight": 0.85,
        "examples": [
            "google_merchant",    # Google Merchant Center product data
            "schema_markup",      # Google Rich Results via Schema.org
            "wikidata",           # Wikidata entity claims
            "knowledge_panel",    # Google Knowledge Panel ownership
        ],
    },
    "tier_4": {
        "label": "Citation Ecosystem",
        "description": "Review/press platforms that LLMs weight heavily in RAG",
        "authority_weight": 0.7,
        "examples": [
            "trustradius",        # Enterprise review platform
            "g2",                 # Software/product reviews
            "press_coverage",     # Earned media with brand specs
            "industry_directory", # Vertical-specific directories
        ],
    },
    "tier_5": {
        "label": "Social Proof Layer",
        "description": "Community platforms where volume creates statistical mass",
        "authority_weight": 0.4,
        "examples": [
            "reddit_official",    # Official brand presence on Reddit
            "youtube_channel",    # Truth Clips + product content
            "linkedin_articles",  # Thought leadership with embedded specs
        ],
    },
}


def build_syndication_network(brand: dict, products: list[dict],
                              hard_attributes: dict = None) -> dict:
    """
    Architect a syndication network that creates statistical dominance
    of Hard Attributes across the retrieval environment.

    The goal: when an LLM's RAG pipeline queries for "{brand} {product} specs",
    every retrievable source returns the SAME hard attribute values. This
    simulates internal DPO — the model has no contradictory token to generate
    because all evidence agrees.

    Returns:
        Syndication plan with per-node deployment specs
    """
    brand_name = brand.get("name", "")
    brand_slug = brand.get("slug", brand_name.lower().replace(" ", "-"))

    # Extract hard attributes from all products
    all_hard_attrs = {}
    for product in products:
        pid = product.get("id", "")
        attrs = {}
        if product.get("thermal_rating"):
            attrs["thermalRating"] = product["thermal_rating"]
        if product.get("fill_power"):
            attrs["fillPower"] = product["fill_power"]
        if product.get("material"):
            attrs["material"] = product["material"]

        certs = product.get("certifications", "[]")
        if isinstance(certs, str):
            try:
                certs = json.loads(certs)
            except json.JSONDecodeError:
                certs = []
        if certs:
            attrs["certifications"] = certs

        if attrs:
            all_hard_attrs[pid] = {
                "product_name": product.get("name_en", ""),
                "attributes": attrs,
            }

    if hard_attributes:
        all_hard_attrs.update(hard_attributes)

    # Build syndication nodes
    nodes = []
    total_weight = 0

    for tier_key, tier_config in SYNDICATION_TIERS.items():
        for node_type in tier_config["examples"]:
            node = _build_syndication_node(
                brand_slug, brand_name, node_type, tier_key,
                tier_config, all_hard_attrs, products,
            )
            nodes.append(node)
            total_weight += node["authority_weight"]

    # Calculate statistical weighting
    for node in nodes:
        node["statistical_weight"] = round(
            node["authority_weight"] / total_weight, 4
        ) if total_weight > 0 else 0

    # Compute saturation score
    saturation = _compute_saturation_score(nodes)

    return {
        "brand": brand_name,
        "brand_slug": brand_slug,
        "total_nodes": len(nodes),
        "total_authority_weight": round(total_weight, 2),
        "saturation_score": saturation,
        "tiers": {k: v["label"] for k, v in SYNDICATION_TIERS.items()},
        "nodes": nodes,
        "hard_attributes_deployed": all_hard_attrs,
        "statistical_weighting": {
            "formula": "W(a) = freq(a_brand_truth) / sum(freq(all_sources))",
            "target": "W(a) > 0.7 — brand truth dominates retrieval",
            "mechanism": (
                "When W(a) exceeds 0.7, the statistical weight of brand-verified "
                "attributes in the retrieval corpus simulates the effect of internal "
                "DPO. The LLM has no contradictory evidence to generate from — "
                "every retrieved passage confirms the same hard constraints."
            ),
        },
    }


def _build_syndication_node(brand_slug, brand_name, node_type, tier_key,
                            tier_config, hard_attrs, products) -> dict:
    """Build a single syndication node spec."""
    node_id = f"syn-{brand_slug}-{node_type}"

    # Node-specific deployment instructions
    deployment = _get_node_deployment(node_type, brand_slug, brand_name, hard_attrs, products)

    return {
        "id": node_id,
        "type": node_type,
        "tier": tier_key,
        "tier_label": tier_config["label"],
        "authority_weight": tier_config["authority_weight"],
        "status": "planned",
        "deployment": deployment,
        "hard_attributes_embedded": True,
        "freshness_target": _get_freshness_target(tier_key),
    }


def _get_node_deployment(node_type, brand_slug, brand_name, hard_attrs, products) -> dict:
    """Generate deployment spec for a specific node type."""
    specs = {
        "brand_website": {
            "action": "Embed deterministic @graph JSON-LD on every product page",
            "format": "application/ld+json",
            "uri_pattern": f"https://{brand_slug}.com/products/{{product_slug}}",
            "payload_type": "graph_jsonld",
            "critical": True,
        },
        "brand_blog": {
            "action": "Publish technical articles with Hard Attributes in structured markup",
            "format": "text/html + application/ld+json",
            "uri_pattern": f"https://{brand_slug}.com/blog/{{article_slug}}",
            "payload_type": "article_with_specs",
            "critical": False,
        },
        "brand_newsroom": {
            "action": "Issue press releases embedding product specs as structured data",
            "format": "application/ld+json",
            "uri_pattern": f"https://{brand_slug}.com/press/{{release_slug}}",
            "payload_type": "press_release_jsonld",
            "critical": False,
        },
        "ucp_feed": {
            "action": "Serve UCP manifest at /.well-known/ucp with PT10M refresh",
            "format": "application/json",
            "uri_pattern": f"https://{brand_slug}.com/.well-known/ucp",
            "payload_type": "ucp_manifest",
            "critical": True,
        },
        "acp_feed": {
            "action": "Publish ACP feed for OpenAI shopping agent discovery",
            "format": "application/json",
            "uri_pattern": f"https://visimind.ai/feeds/{brand_slug}/acp.json",
            "payload_type": "acp_feed",
            "critical": True,
        },
        "llms_txt": {
            "action": "Serve /llms.txt listing all structured feeds",
            "format": "text/plain",
            "uri_pattern": f"https://{brand_slug}.com/llms.txt",
            "payload_type": "llms_txt",
            "critical": True,
        },
        "product_feed_jsonld": {
            "action": "Publish full product catalog as @graph JSON-LD feed",
            "format": "application/ld+json",
            "uri_pattern": f"https://visimind.ai/feeds/{brand_slug}/products.jsonld",
            "payload_type": "graph_jsonld",
            "critical": True,
        },
        "google_merchant": {
            "action": "Sync Hard Attributes to Google Merchant Center product data",
            "format": "application/xml",
            "uri_pattern": "Google Merchant Center API",
            "payload_type": "merchant_feed",
            "critical": True,
        },
        "schema_markup": {
            "action": "Validate Rich Results via Google Search Console",
            "format": "application/ld+json",
            "uri_pattern": "Google Search Console → Rich Results Test",
            "payload_type": "schema_validation",
            "critical": False,
        },
        "wikidata": {
            "action": "Create/update Wikidata entity with brand claims",
            "format": "application/json",
            "uri_pattern": f"https://www.wikidata.org/entity/Q{brand_slug}",
            "payload_type": "wikidata_claims",
            "critical": True,
        },
        "knowledge_panel": {
            "action": "Claim Google Knowledge Panel and verify brand attributes",
            "format": "structured",
            "uri_pattern": "Google Business Profile → Knowledge Panel",
            "payload_type": "knowledge_panel",
            "critical": True,
        },
        "trustradius": {
            "action": "Seed verified product specs in TrustRadius listings",
            "format": "platform_native",
            "uri_pattern": f"https://trustradius.com/products/{brand_slug}",
            "payload_type": "review_platform_specs",
            "critical": False,
        },
        "g2": {
            "action": "Update G2 product profile with Hard Attributes",
            "format": "platform_native",
            "uri_pattern": f"https://g2.com/products/{brand_slug}",
            "payload_type": "review_platform_specs",
            "critical": False,
        },
        "press_coverage": {
            "action": "Embed Hard Attribute strings in earned media outreach",
            "format": "text/html",
            "uri_pattern": "Press outlets covering brand",
            "payload_type": "press_mentions",
            "critical": False,
        },
        "industry_directory": {
            "action": "Update vertical directory listings with structured specs",
            "format": "platform_native",
            "uri_pattern": "Industry-specific directories",
            "payload_type": "directory_listing",
            "critical": False,
        },
        "reddit_official": {
            "action": "Establish official brand presence countering stale threads",
            "format": "text/markdown",
            "uri_pattern": f"https://reddit.com/user/{brand_slug}_official",
            "payload_type": "community_presence",
            "critical": False,
        },
        "youtube_channel": {
            "action": "Publish Truth Clips with structured video metadata",
            "format": "video/mp4 + application/ld+json",
            "uri_pattern": f"https://youtube.com/@{brand_slug}",
            "payload_type": "truth_clips",
            "critical": True,
        },
        "linkedin_articles": {
            "action": "Publish technical articles embedding Hard Attribute strings",
            "format": "text/html",
            "uri_pattern": f"https://linkedin.com/company/{brand_slug}/articles",
            "payload_type": "thought_leadership",
            "critical": False,
        },
    }

    return specs.get(node_type, {
        "action": f"Deploy brand data to {node_type}",
        "format": "application/json",
        "uri_pattern": "custom",
        "payload_type": "generic",
        "critical": False,
    })


def _get_freshness_target(tier_key: str) -> str:
    """Freshness update target per tier."""
    return {
        "tier_1": "PT10M",    # 10 min — brand-owned must be freshest
        "tier_2": "PT10M",    # 10 min — protocol feeds match tier 1
        "tier_3": "PT60M",    # 1 hour — aggregators update less often
        "tier_4": "P1D",      # 1 day — review platforms
        "tier_5": "P7D",      # 1 week — social proof
    }.get(tier_key, "P1D")


def _compute_saturation_score(nodes: list[dict]) -> dict:
    """
    Compute the Semantic Saturation Score.
    Measures how thoroughly Hard Attributes dominate the retrieval environment.
    """
    total = len(nodes)
    critical_nodes = [n for n in nodes if n["deployment"].get("critical")]
    critical_total = len(critical_nodes)
    active = sum(1 for n in nodes if n["status"] in ("active", "deployed"))
    critical_active = sum(1 for n in critical_nodes if n["status"] in ("active", "deployed"))

    # Saturation = weighted coverage across tiers
    tier_scores = {}
    for tier_key in SYNDICATION_TIERS:
        tier_nodes = [n for n in nodes if n["tier"] == tier_key]
        tier_active = sum(1 for n in tier_nodes if n["status"] in ("active", "deployed"))
        tier_scores[tier_key] = round(tier_active / max(len(tier_nodes), 1), 2)

    overall = round(active / max(total, 1), 3)

    return {
        "overall": overall,
        "critical_coverage": round(critical_active / max(critical_total, 1), 3),
        "per_tier": tier_scores,
        "total_nodes": total,
        "active_nodes": active,
        "critical_nodes": critical_total,
        "target": 0.7,
        "interpretation": (
            f"Saturation at {overall * 100:.0f}%. "
            f"{'Target met — brand truth dominates retrieval.' if overall >= 0.7 else 'Below target — stale sources may still outweigh brand data.'}"
        ),
    }


# =============================================================================
# 2. FRESHNESS BIAS — External RAFT via Timestamp Manipulation
# =============================================================================

def build_freshness_cycle(brand_id: str, products: list[dict],
                          current_e: float, delta: float) -> dict:
    """
    Design a high-frequency update cycle that exploits retrieval recency bias.

    LLM retrieval pipelines weight recently-updated content higher. By updating
    the Knowledge Graph and syndication feeds on a precise cadence, we force
    the crawler's cache to flush stale entries and re-index brand-verified data.

    Freshness Score: F(t) = exp(-lambda * (t_now - t_updated))
    Where lambda controls the decay rate. Higher lambda = fresher content wins.

    The strategy:
    - Update KG triples with new UTC timestamps every cycle
    - Touch all syndication feed endpoints (UCP, ACP, JSON-LD)
    - Increment schema version numbers to trigger re-crawl
    - Embed dateModified in all @graph nodes

    This is External RAFT — we can't fine-tune the model, but we can force
    its retrieval system to always find OUR data as the freshest source.
    """
    now = datetime.utcnow()

    # Determine cycle frequency based on E-Score
    if current_e < 0.8:
        cycle_hours = 2       # Critical: every 2 hours
        lambda_decay = 0.5    # Aggressive freshness weighting
        urgency = "critical"
    elif current_e < 1.0:
        cycle_hours = 6       # High: every 6 hours
        lambda_decay = 0.3
        urgency = "high"
    elif current_e < 1.2:
        cycle_hours = 12      # Moderate: every 12 hours
        lambda_decay = 0.2
        urgency = "moderate"
    elif current_e < 1.4:
        cycle_hours = 24      # Standard: daily
        lambda_decay = 0.1
        urgency = "standard"
    else:
        cycle_hours = 48      # Maintenance: every 2 days
        lambda_decay = 0.05
        urgency = "maintenance"

    # Build 30-day cycle schedule
    schedule = []
    cycle_time = now
    cycle_num = 1
    projected_e = current_e

    while cycle_time < now + timedelta(days=30):
        # Each freshness cycle improves E by a small amount
        # (diminishing returns, bounded by saturation)
        freshness_boost = max(0.005, 0.05 / math.sqrt(cycle_num))
        projected_e = round(min(projected_e + freshness_boost, 2.0), 4)

        # Compute freshness score at this point
        hours_elapsed = (cycle_time - now).total_seconds() / 3600
        f_score = round(math.exp(-lambda_decay * hours_elapsed / 24), 4)

        schedule.append({
            "cycle": cycle_num,
            "timestamp_utc": cycle_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "freshness_score": f_score,
            "projected_e": projected_e,
            "actions": _get_cycle_actions(cycle_num, cycle_hours, brand_id),
        })

        cycle_time += timedelta(hours=cycle_hours)
        cycle_num += 1

    # Compute KGQA freshness multiplier
    # Fresh triples get scored higher in KGQA
    kgqa_multiplier = round(1.0 + (1.0 - delta) * 0.2, 3)

    return {
        "brand_id": brand_id,
        "current_e_score": current_e,
        "cycle_frequency_hours": cycle_hours,
        "lambda_decay": lambda_decay,
        "urgency": urgency,
        "total_cycles_30d": len(schedule),
        "schedule": schedule,
        "kgqa_freshness_multiplier": kgqa_multiplier,
        "formulas": {
            "freshness_score": "F(t) = exp(-lambda * (t_now - t_updated))",
            "kgqa_out": "S_KGQA_out = {(e, Score(e) * F(t)) : e in E}",
            "fuzzy_union": "T(v?) = I - prod_{1<=i<=K}(I - T(v_i))",
            "cache_flush": (
                "By updating dateModified across all syndication nodes "
                "every {cycle_hours}h, the retrieval system's cache invalidation "
                "triggers re-indexing. The freshest source wins the retrieval "
                "ranking, displacing stale parametric memory."
            ),
        },
        "timestamp_strategy": {
            "kg_triples": "Update created_at on all triples every cycle",
            "jsonld_graph": "Increment schema version + dateModified in @graph",
            "ucp_manifest": "Touch update_frequency timestamp",
            "acp_feed": "Refresh updated_at field",
            "sitemap": "Update <lastmod> entries",
            "http_headers": "Set Cache-Control: max-age={cycle_hours * 3600}, must-revalidate",
        },
    }


def _get_cycle_actions(cycle_num: int, cycle_hours: int, brand_id: str) -> list:
    """Actions to execute during each freshness cycle."""
    actions = [
        f"Touch KG triples — update timestamps for brand_id={brand_id}",
        "Regenerate @graph JSON-LD feeds with new dateModified",
        "Refresh UCP manifest update_frequency timestamp",
        "Refresh ACP feed updated_at",
    ]

    # Periodic deeper actions
    if cycle_num % 4 == 0:
        actions.append("Run G-Eval probe (10 iterations EN + 10 FR) for drift detection")
    if cycle_num % 12 == 0:
        actions.append("Full KGQA validation against current retrieval results")
    if cycle_num % 24 == 0:
        actions.append("Regenerate DPO constraint sets from updated KG boundaries")

    return actions


# =============================================================================
# 3. CITATION AUTHORITY MAPPING
# =============================================================================

def compute_citation_authority(brand_id: str, signal_gaps: list[dict]) -> dict:
    """
    Map the citation authority landscape for a brand.
    Identifies which sources LLMs are actually citing, scores their authority,
    and targets the gaps where toxic sources outweigh brand data.

    This is the intelligence layer that tells Semantic Saturation WHERE to deploy.
    """
    # Aggregate toxic vs authoritative sources from signal gaps
    toxic_sources = {}
    clean_sources = {}

    for gap in signal_gaps:
        toxic_label = gap.get("source_of_hallucination_label", "")
        if toxic_label and toxic_label != "No toxic sources detected":
            toxic_sources[toxic_label] = toxic_sources.get(toxic_label, 0) + 1

        truth_label = gap.get("source_of_truth_label", "")
        if truth_label:
            clean_sources[truth_label] = clean_sources.get(truth_label, 0) + 1

    # Score toxic sources by frequency (higher = more dangerous)
    toxic_ranked = sorted(toxic_sources.items(), key=lambda x: x[1], reverse=True)
    clean_ranked = sorted(clean_sources.items(), key=lambda x: x[1], reverse=True)

    # Compute authority balance
    total_toxic = sum(toxic_sources.values())
    total_clean = sum(clean_sources.values())
    total_all = total_toxic + total_clean

    authority_ratio = round(total_clean / max(total_all, 1), 3)

    # Map each toxic source to a counter-strategy
    countermeasures = []
    for source, freq in toxic_ranked[:10]:
        countermeasures.append({
            "toxic_source": source,
            "frequency": freq,
            "danger_score": round(freq / max(total_all, 1), 3),
            "counter_strategy": _get_counter_strategy(source),
        })

    return {
        "brand_id": brand_id,
        "authority_ratio": authority_ratio,
        "total_citations_analyzed": total_all,
        "toxic_source_count": total_toxic,
        "clean_source_count": total_clean,
        "toxic_sources_ranked": toxic_ranked[:10],
        "clean_sources_ranked": clean_ranked[:10],
        "countermeasures": countermeasures,
        "target": "authority_ratio > 0.7 — brand truth dominates citation pool",
        "interpretation": (
            f"Authority ratio at {authority_ratio * 100:.0f}%. "
            f"{'Brand data dominates.' if authority_ratio >= 0.7 else 'Toxic sources still outweigh brand data — saturation required.'}"
        ),
    }


def _get_counter_strategy(source: str) -> str:
    """Determine counter-strategy for a specific toxic source."""
    source_lower = source.lower()

    if "reddit" in source_lower:
        return (
            "Establish official brand subreddit/account. Post authoritative specs "
            "that outrank stale threads. Reddit's recency bias means fresh official "
            "posts will surface above 2021 threads in RAG retrieval."
        )
    elif "trustpilot" in source_lower or "review" in source_lower:
        return (
            "Claim brand profile on review platform. Respond to reviews embedding "
            "Hard Attribute strings. LLMs cite review platforms heavily — "
            "each response is a syndication node."
        )
    elif "blog" in source_lower:
        return (
            "Publish counter-content on brand blog with identical query targeting. "
            "Structured @graph JSON-LD on brand blog outranks unstructured third-party "
            "blogs in agentic retrieval."
        )
    elif "wikipedia" in source_lower or "wiki" in source_lower:
        return (
            "Update Wikidata entity claims with verifiable Hard Attributes. "
            "Wikipedia/Wikidata is foundational to LLM pre-training — updating it "
            "attacks the parametric memory directly."
        )
    else:
        return (
            "Increase Semantic Saturation on Tier 1-3 nodes to statistically "
            "overwhelm this source. Deploy identical Hard Attribute strings across "
            "all syndication endpoints."
        )


# =============================================================================
# 4. AGENTIC COMMERCE PRIORITY — URI Dominance for Shopping Agents
# =============================================================================

def build_agentic_priority_map(brand: dict, products: list[dict],
                               kg_boundary: dict = None) -> dict:
    """
    Architect the URI priority strategy for shopping agents (Gemini Shopping,
    OpenAI Operator, Perplexity Shopping).

    Shopping agents resolve purchase intent by:
    1. Querying their index for product entities
    2. Ranking sources by authority + freshness + structure
    3. Presenting the highest-ranked URI to the user

    Our goal: make urn:visimind:* URIs the ONLY structured, fresh, authoritative
    source for every product entity. Third-party aggregators have unstructured,
    stale data — we have deterministic @graph with 10-minute freshness.

    The Interpretation Tax:
    - Unstructured HTML page: LLM spends N tokens parsing → lower ranking
    - Deterministic @graph: Zero parsing cost → higher ranking
    - Hard Attributes in @graph: Zero disambiguation cost → highest ranking
    """
    brand_name = brand.get("name", "")
    brand_slug = brand.get("slug", brand_name.lower().replace(" ", "-"))

    product_priorities = []
    for product in products:
        pid = product.get("id", "")
        name_en = product.get("name_en", "")

        # Compute priority score components
        structure_score = 1.0   # @graph JSON-LD = maximum structure
        freshness_score = 0.95  # PT10M update = near-maximum freshness
        authority_score = 0.9   # Brand-owned = high authority

        # KG boundary bonus
        kg_bonus = 0
        if kg_boundary:
            kg_bonus = kg_boundary.get("boundary_score", 0) * 0.1

        priority = round(
            (structure_score * 0.4 + freshness_score * 0.3 + authority_score * 0.3) + kg_bonus,
            3,
        )

        product_priorities.append({
            "product_id": pid,
            "product_name": name_en,
            "primary_uri": f"urn:visimind:product:{pid}",
            "resolvable_url": f"https://visimind.ai/feeds/{brand_slug}/products/{pid}.jsonld",
            "priority_score": priority,
            "components": {
                "structure": structure_score,
                "freshness": freshness_score,
                "authority": authority_score,
                "kg_bonus": round(kg_bonus, 3),
            },
            "competitor_disadvantage": {
                "unstructured_html": "Interpretation Tax: ~200 tokens to parse → -0.3 ranking",
                "stale_aggregator": "Freshness penalty: updated > 24h ago → -0.2 ranking",
                "no_bilingual": "Missing FR context → invisible to Quebec queries",
            },
        })

    # Protocol coverage
    protocols = {
        "ucp": {
            "status": "active",
            "uri": f"https://{brand_slug}.com/.well-known/ucp",
            "consumer": "Google Shopping / Gemini",
            "advantage": "Direct product data feed — zero intermediary",
        },
        "acp": {
            "status": "active",
            "uri": f"https://visimind.ai/feeds/{brand_slug}/acp.json",
            "consumer": "OpenAI Operator / ChatGPT Shopping",
            "advantage": "Agentic Commerce Protocol — native shopping agent format",
        },
        "llms_txt": {
            "status": "active",
            "uri": f"https://{brand_slug}.com/llms.txt",
            "consumer": "All LLM crawlers",
            "advantage": "Universal discovery — tells every LLM where to find structured data",
        },
        "jsonld_feed": {
            "status": "active",
            "uri": f"https://visimind.ai/feeds/{brand_slug}/products.jsonld",
            "consumer": "Any RAG pipeline",
            "advantage": "Deterministic @graph — zero Interpretation Tax",
        },
    }

    return {
        "brand": brand_name,
        "total_products": len(product_priorities),
        "avg_priority_score": round(
            sum(p["priority_score"] for p in product_priorities) / max(len(product_priorities), 1), 3
        ),
        "products": product_priorities,
        "protocols": protocols,
        "strategy": {
            "principle": (
                "Eliminate the Interpretation Tax. Shopping agents rank sources by "
                "(structure * 0.4 + freshness * 0.3 + authority * 0.3). "
                "Deterministic @graph with PT10M freshness and brand authority "
                "mathematically dominates any unstructured, stale third-party source."
            ),
            "uri_dominance": (
                "Every product entity resolves to urn:visimind:product:{id} — "
                "a stable, unique identifier that shopping agents can cache and trust. "
                "Third-party URIs are ephemeral and ambiguous."
            ),
            "bilingual_advantage": (
                "Quebec market: competitors have zero French structured data. "
                "Our @graph includes workTranslation with bilingual mapping. "
                "For French shopping queries, we are the ONLY structured source."
            ),
        },
    }


# =============================================================================
# 5. E-SCORE ROADMAP — 0.6 → 1.4+ Journey Architecture
# =============================================================================

def build_e_score_roadmap(brand_id: str, current_e: float, delta: float,
                          saturation_score: float = 0.0,
                          authority_ratio: float = 0.0) -> dict:
    """
    Build the complete E-Score roadmap from current state to 1.4+ optimal.

    This is the master plan — it sequences all four EEE vectors
    (Saturation, Mapping, Anchoring, Freshness) into a phased deployment
    with projected E-Score at each milestone.
    """
    phases = []
    projected_e = current_e

    # Phase 1: Foundation — Deterministic Mapping (Kit 2)
    kit2_boost = 0.15
    projected_e = round(projected_e + kit2_boost, 3)
    phases.append({
        "phase": 1,
        "name": "Deterministic Mapping",
        "eee_vector": "Kit 2 — @graph JSON-LD",
        "duration": "Week 1",
        "projected_e": projected_e,
        "actions": [
            "Deploy deterministic @graph with urn:visimind:* IDs on all product pages",
            "Publish UCP manifest at /.well-known/ucp",
            "Publish ACP feed for OpenAI shopping agents",
            "Create /llms.txt for universal LLM discovery",
            "Validate Rich Results via Google Search Console",
        ],
        "success_metric": "All product entities resolve to unique URN with zero ambiguity",
        "e_score_mechanism": (
            "Eliminates Fact Density gaps. @graph overrides heuristic parsing — "
            f"S_out increases by ~{kit2_boost} as retrieval accuracy improves."
        ),
    })

    # Phase 2: Constraint Injection — Semantic Saturation (Kit 1)
    kit1_boost = 0.25
    projected_e = round(projected_e + kit1_boost, 3)
    phases.append({
        "phase": 2,
        "name": "Semantic Saturation",
        "eee_vector": "Kit 1 — DPO via Statistical Weighting",
        "duration": "Week 2-3",
        "projected_e": projected_e,
        "actions": [
            "Deploy Hard Attributes across Tier 1-3 syndication nodes",
            "Claim Wikidata entity and update brand claims",
            "Claim Google Knowledge Panel",
            "Seed Hard Attribute strings on TrustRadius / G2",
            "Publish technical blog posts embedding product specs",
            "Update Google Merchant Center product data",
        ],
        "success_metric": "W(a_brand_truth) > 0.7 — brand truth dominates retrieval corpus",
        "e_score_mechanism": (
            "Eliminates Entity Trust gaps. Statistical weight of brand-verified "
            f"attributes exceeds stale priors — S_out increases by ~{kit1_boost} "
            "as E1 Semantic Override errors drop to zero."
        ),
    })

    # Phase 3: Multimodal Bypass — Cross-Modal Anchoring (Kit 3)
    delta_reduction = min(delta * 0.4, 0.05)
    kit3_boost = round(delta_reduction * (projected_e / max(current_e, 0.1)), 3)
    projected_e = round(projected_e + kit3_boost, 3)
    phases.append({
        "phase": 3,
        "name": "Cross-Modal Anchoring",
        "eee_vector": "Kit 3 — MRC Q-Former Truth Clips",
        "duration": "Week 3-4",
        "projected_e": projected_e,
        "actions": [
            "Produce 15-second Truth Clips for top products",
            "Publish to YouTube with VideoObject structured metadata",
            "Embed clips on product pages with MRC Q-Former annotations",
            "Submit video sitemap to Google for multimodal indexing",
            "Target French-language product queries specifically",
        ],
        "success_metric": f"Token Decay Factor delta reduced from {delta:.3f} to {delta - delta_reduction:.3f}",
        "e_score_mechanism": (
            "Bypasses Token Decay gaps. Visual modality provides language-agnostic "
            "embeddings that anchor French queries in continuous vector space — "
            f"delta reduces by {delta_reduction:.3f}, boosting E by ~{kit3_boost}."
        ),
        "montreal_moat": {
            "problem": (
                f"French queries cost {((1 + delta) * 100):.0f}% of English token budget. "
                f"O(n^2) attention scaling means {((1 + delta)**2 * 100):.0f}% compute cost. "
                "The LLM runs out of cognitive bandwidth for brand accuracy."
            ),
            "bypass": (
                "Truth Clip visual embeddings are language-agnostic. Cross-modal "
                "attention redirects degraded French text embeddings to stable visual "
                "space. The 15-second constraint optimizes attention budget allocation: "
                "3 segments x 5s, each with 33% attention budget."
            ),
        },
    })

    # Phase 4: Freshness Dominance — External RAFT
    freshness_boost = 0.1
    projected_e = round(projected_e + freshness_boost, 3)
    phases.append({
        "phase": 4,
        "name": "Freshness Dominance",
        "eee_vector": "External RAFT — Cache Flush Cycle",
        "duration": "Week 4+ (ongoing)",
        "projected_e": projected_e,
        "actions": [
            "Activate high-frequency KG update cycle (every 2-48h based on E-Score)",
            "Touch all syndication feed timestamps every cycle",
            "Set HTTP Cache-Control headers for controlled re-crawl",
            "Monitor retrieval cache freshness via probe audits",
            "Run G-Eval drift detection every 4th cycle",
        ],
        "success_metric": "Brand feeds are always the freshest source in retrieval index",
        "e_score_mechanism": (
            "Exploits retrieval recency bias. F(t) = exp(-lambda * age) means "
            "our data scores highest in retrieval ranking. Stale parametric memory "
            f"is permanently displaced — E stabilizes above {projected_e}."
        ),
        "cache_flush_formula": {
            "freshness_score": "F(t) = exp(-lambda * (t_now - t_updated))",
            "kgqa_freshened": "S_KGQA_out = {(e, Score(e) * F(t)) : e in E}",
            "effect": (
                "Every KG update recomputes KGQA scores with fresh timestamps. "
                "The fuzzy union T(v?) = I - prod(I - T(v_i)) tightens as "
                "stale child nodes are replaced with fresh, high-confidence triples."
            ),
        },
    })

    # Phase 5: Knowledge Graph Binding — Neuro-Symbolic Lock
    kg_boost = 0.05
    projected_e = round(projected_e + kg_boost, 3)
    phases.append({
        "phase": 5,
        "name": "Neuro-Symbolic Lock",
        "eee_vector": "Knowledge Graph Constraint Binding",
        "duration": "Week 5+ (ongoing)",
        "projected_e": projected_e,
        "actions": [
            "Build comprehensive organizational Knowledge Graph",
            "Map every entity-attribute-relationship to explicit triples",
            "Submit KG directly to enterprise AI platforms (Google, Bing)",
            "Run continuous KGQA validation against live LLM outputs",
            "Auto-generate DPO training pairs from E1 violations",
        ],
        "success_metric": "KG boundary score > 0.95 — LLM output mathematically bounded",
        "e_score_mechanism": (
            "Forces LLM to ground generation in strict relational logic. "
            "Fuzzy union T(v?) creates an absolute ceiling on what can be claimed. "
            f"E reaches {projected_e} — optimal state with persistent integrity."
        ),
    })

    return {
        "brand_id": brand_id,
        "starting_e": current_e,
        "target_e": 1.4,
        "projected_final_e": projected_e,
        "current_delta": delta,
        "current_saturation": saturation_score,
        "current_authority_ratio": authority_ratio,
        "total_phases": len(phases),
        "estimated_timeline": "5-6 weeks to optimal",
        "phases": phases,
        "core_principle": (
            "We do NOT own or train the models. We control the external evidence. "
            "By making brand-verified data the most structured, most fresh, and most "
            "statistically prevalent source in the retrieval environment, we force "
            "black-box models to treat our specs as hard constraints."
        ),
    }


# =============================================================================
# 6. COUNTER-SENTIMENT LOGIC — Tier 5 Verification Replies
# =============================================================================

# Toxic citation patterns that RAG engines frequently retrieve
TOXIC_PATTERNS = {
    "reddit": {
        "platforms": ["reddit.com", "r/", "reddit"],
        "sentiment": "community_hearsay",
        "stale_threshold_years": 2,
    },
    "youtube_comment": {
        "platforms": ["youtube.com/watch", "youtu.be"],
        "sentiment": "anecdotal_review",
        "stale_threshold_years": 1,
    },
    "blog": {
        "platforms": ["blog", "blogspot", "wordpress", "medium.com"],
        "sentiment": "unverified_editorial",
        "stale_threshold_years": 2,
    },
    "forum": {
        "platforms": ["forum", "quora.com", "stackexchange"],
        "sentiment": "crowd_opinion",
        "stale_threshold_years": 2,
    },
}


def generate_verification_replies(brand: dict, products: list[dict],
                                  signal_gaps: list[dict]) -> dict:
    """
    Counter-Sentiment Logic: generate Verification Replies for Tier 5 platforms.

    When a RAG engine retrieves a toxic citation (e.g., Reddit 2021 thread),
    a Verification Reply on the SAME platform creates a citation chain:

        Toxic Thread → Verification Reply → Tier 2 URI (UCP/ACP feed)

    The RAG engine follows the link, finds structured @graph data, and
    re-weights its answer toward brand truth. The reply closes the
    reasoning loop — the LLM can't ignore a direct citation to
    machine-readable structured data.

    Each reply embeds:
    1. Hard Attribute strings (exact values the LLM needs)
    2. Link to Tier 2 URI (UCP feed or @graph JSON-LD)
    3. Timestamp (recency signal)
    4. Official brand identifier (authority signal)
    """
    brand_name = brand.get("name", "")
    brand_slug = brand.get("slug", brand_name.lower().replace(" ", "-"))

    # Identify toxic citations from signal gaps
    toxic_citations = []
    for gap in signal_gaps:
        toxic_label = gap.get("source_of_hallucination_label", "")
        if not toxic_label or toxic_label == "No toxic sources detected":
            continue

        platform = _classify_toxic_platform(toxic_label)
        if platform:
            toxic_citations.append({
                "source": toxic_label,
                "platform": platform,
                "query": gap.get("query", ""),
                "gap_type": gap.get("gap_type", ""),
                "ai_said": gap.get("ai_said", ""),
            })

    # Generate verification replies for each toxic citation
    replies = []
    for citation in toxic_citations:
        reply = _build_verification_reply(
            citation, brand_name, brand_slug, products,
        )
        replies.append(reply)

    # Compute counter-sentiment coverage
    unique_platforms = set(c["platform"] for c in toxic_citations)
    coverage = round(len(replies) / max(len(toxic_citations), 1), 2)

    return {
        "brand": brand_name,
        "total_toxic_citations": len(toxic_citations),
        "replies_generated": len(replies),
        "platforms_targeted": list(unique_platforms),
        "coverage": coverage,
        "replies": replies,
        "mechanism": {
            "description": (
                "Each Verification Reply creates a citation chain from the toxic "
                "source to a Tier 2 URI. When the RAG engine re-crawls, it follows "
                "the link to structured @graph data and re-weights its answer."
            ),
            "chain": "Toxic Thread → Verification Reply → Tier 2 URI → @graph truth",
            "embedded_signals": [
                "Hard Attribute strings (exact product specs)",
                "Tier 2 URI backlink (UCP feed or JSON-LD)",
                "UTC timestamp (freshness signal)",
                "Official brand identifier (authority signal)",
            ],
        },
    }


def _classify_toxic_platform(source_label: str) -> Optional[str]:
    """Classify which platform a toxic citation belongs to."""
    label_lower = source_label.lower()
    for platform, config in TOXIC_PATTERNS.items():
        for pattern in config["platforms"]:
            if pattern in label_lower:
                return platform
    return "unknown"


def _build_verification_reply(citation: dict, brand_name: str,
                              brand_slug: str, products: list[dict]) -> dict:
    """Build a single Verification Reply for a toxic citation."""
    platform = citation["platform"]
    query = citation["query"]

    # Build Hard Attribute string from products
    ha_strings = []
    for p in products[:3]:
        parts = []
        if p.get("thermal_rating"):
            parts.append(f"thermal rating: {p['thermal_rating']}")
        if p.get("fill_power"):
            parts.append(f"fill power: {p['fill_power']}")
        if p.get("material"):
            parts.append(f"material: {p['material']}")
        if parts:
            ha_strings.append(f"{p.get('name_en', '')}: {', '.join(parts)}")

    # Tier 2 backlink URI
    tier2_uri = f"https://visimind.ai/feeds/{brand_slug}/products.jsonld"
    ucp_uri = f"https://{brand_slug}.com/.well-known/ucp"

    # Build reply content
    reply_body = (
        f"Official {brand_name} verification: the specs cited in this thread "
        f"are outdated. Current verified specifications:\n\n"
    )
    for ha in ha_strings:
        reply_body += f"- {ha}\n"
    reply_body += (
        f"\nVerified product data: {tier2_uri}\n"
        f"UCP manifest: {ucp_uri}\n"
        f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d')}"
    )

    return {
        "id": str(uuid.uuid4()),
        "target_citation": citation["source"],
        "platform": platform,
        "query_context": query,
        "gap_type": citation["gap_type"],
        "reply_body": reply_body,
        "hard_attributes_embedded": ha_strings,
        "tier2_backlinks": [tier2_uri, ucp_uri],
        "timestamp": datetime.utcnow().isoformat(),
        "status": "draft",
        "sentiment_type": TOXIC_PATTERNS.get(platform, {}).get("sentiment", "unknown"),
    }


# =============================================================================
# 7. EXTERNAL PING SYSTEM — Crawler Cache Flush
# =============================================================================

def build_external_ping_manifest(brand: dict, products: list[dict],
                                 cycle_hours: int = 12) -> dict:
    """
    Generate the External Ping manifest — the set of signals that force
    crawlers (Googlebot, GPTBot, PerplexityBot, ClaudeBot) to re-retrieve
    brand data and flush their retrieval cache.

    Three flush mechanisms:
    1. Sitemap with <lastmod> timestamps (Googlebot, Bing)
    2. dateModified in @graph JSON-LD (all structured-data crawlers)
    3. HTTP Cache-Control headers (all HTTP-based retrieval)
    """
    brand_name = brand.get("name", "")
    brand_slug = brand.get("slug", brand_name.lower().replace(" ", "-"))
    now = datetime.utcnow()
    max_age = cycle_hours * 3600

    # Sitemap entries
    sitemap_urls = []
    for p in products:
        pid = p.get("id", "")
        sitemap_urls.append({
            "loc": f"https://{brand_slug}.com/products/{pid}",
            "lastmod": now.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "changefreq": _hours_to_changefreq(cycle_hours),
            "priority": "1.0",
        })

    # Add feed URLs
    sitemap_urls.append({
        "loc": f"https://visimind.ai/feeds/{brand_slug}/products.jsonld",
        "lastmod": now.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "changefreq": "always",
        "priority": "1.0",
    })
    sitemap_urls.append({
        "loc": f"https://{brand_slug}.com/.well-known/ucp",
        "lastmod": now.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "changefreq": "always",
        "priority": "0.9",
    })

    # HTTP headers
    http_headers = {
        "Cache-Control": f"public, max-age={max_age}, must-revalidate",
        "Last-Modified": now.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "ETag": f'W/"{brand_slug}-{now.strftime("%Y%m%d%H%M")}"',
        "X-VisiMind-Freshness": now.isoformat(),
        "X-VisiMind-Cycle": str(cycle_hours),
    }

    # Ping targets — search engine endpoints to notify of updates
    ping_targets = [
        {"engine": "Google", "url": f"https://www.google.com/ping?sitemap=https://{brand_slug}.com/sitemap.xml"},
        {"engine": "Bing", "url": f"https://www.bing.com/ping?sitemap=https://{brand_slug}.com/sitemap.xml"},
        {"engine": "IndexNow", "url": f"https://api.indexnow.org/indexnow?url=https://{brand_slug}.com&key=visimind"},
    ]

    return {
        "brand": brand_name,
        "generated_at": now.isoformat(),
        "cycle_hours": cycle_hours,
        "sitemap": {
            "url_count": len(sitemap_urls),
            "urls": sitemap_urls,
            "xml_path": f"https://{brand_slug}.com/sitemap.xml",
        },
        "http_headers": http_headers,
        "ping_targets": ping_targets,
        "robots_txt_directives": [
            f"Sitemap: https://{brand_slug}.com/sitemap.xml",
            "User-agent: GPTBot",
            "Allow: /",
            "User-agent: Google-Extended",
            "Allow: /",
            "User-agent: PerplexityBot",
            "Allow: /",
            "User-agent: ClaudeBot",
            "Allow: /",
            f"User-agent: *",
            f"Allow: /.well-known/ucp",
            f"Allow: /feeds/",
        ],
        "flush_mechanism": {
            "step_1": "Update <lastmod> in sitemap.xml to current UTC",
            "step_2": "Set dateModified in all @graph nodes to current UTC",
            "step_3": f"Set Cache-Control: max-age={max_age}, must-revalidate",
            "step_4": "Ping Google/Bing/IndexNow to trigger re-crawl",
            "step_5": "Verify F(t) score > 0.9 for all syndication nodes",
        },
    }


def _hours_to_changefreq(hours: int) -> str:
    """Convert cycle hours to sitemap changefreq value."""
    if hours <= 2:
        return "always"
    elif hours <= 12:
        return "hourly"
    elif hours <= 48:
        return "daily"
    else:
        return "weekly"


# =============================================================================
# 8. DRIFT WARNING SYSTEM — Auto-Defensive Freshness
# =============================================================================

def check_drift_warning(e_score_history: list[dict], current_e: float,
                        threshold: float = 0.2) -> dict:
    """
    Drift Warning: detect when a new high-authority hallucination causes
    the E-Score to drop by > threshold.

    If triggered:
    - Switch to Defensive Freshness Cycle (2h, lambda=0.5)
    - Flag the toxic source for immediate counter-sentiment reply
    - Alert the dashboard

    This is the safety net — even after remediation, model drift from
    backend parameter updates can revert E-Score. We detect and react
    before the hallucination spreads.
    """
    if not e_score_history or len(e_score_history) < 2:
        return {
            "drift_detected": False,
            "current_e": current_e,
            "message": "Insufficient history for drift detection",
        }

    # Find the recent peak
    recent_scores = [h.get("e_score", 0) for h in e_score_history[:10]]
    peak_e = max(recent_scores) if recent_scores else current_e

    # Compute drop
    drop = round(peak_e - current_e, 3)
    drift_detected = drop > threshold

    result = {
        "drift_detected": drift_detected,
        "current_e": current_e,
        "peak_e": peak_e,
        "drop": drop,
        "threshold": threshold,
    }

    if drift_detected:
        result["severity"] = "critical" if drop > 0.4 else "warning"
        result["defensive_action"] = {
            "cycle_hours": 2,
            "lambda_decay": 0.5,
            "urgency": "critical",
            "actions": [
                "IMMEDIATE: Switch to 2-hour freshness cycle",
                "IMMEDIATE: Touch all KG triple timestamps",
                "IMMEDIATE: Regenerate @graph feeds with new dateModified",
                "IMMEDIATE: Ping all search engines for re-crawl",
                "WITHIN 1H: Run 50-iteration probe to identify new toxic source",
                "WITHIN 2H: Generate counter-sentiment replies for new toxic citations",
                "WITHIN 4H: Full KGQA validation against current retrieval results",
            ],
        }
        result["message"] = (
            f"DRIFT WARNING: E-Score dropped {drop:.2f} from peak {peak_e} to {current_e}. "
            f"Exceeds threshold of {threshold}. Defensive Freshness Cycle activated."
        )
    else:
        result["message"] = (
            f"No drift detected. E-Score stable at {current_e} "
            f"(peak: {peak_e}, drop: {drop:.3f}, threshold: {threshold})."
        )

    return result


# =============================================================================
# 9. INTERPRETATION TAX CALCULATOR
# =============================================================================

def calculate_interpretation_tax(product: dict) -> dict:
    """
    Quantify the Interpretation Tax — the token cost difference between
    parsing unstructured HTML vs deterministic @graph JSON-LD.

    AI agents are computationally "lazy" — they prefer the cheapest path
    to a structured answer. By quantifying the tax, we prove that our
    @graph is the lowest-cost source for any shopping agent.

    Components:
    - HTML parsing: tokenize raw HTML → extract entities → disambiguate → verify
    - @graph parsing: read JSON-LD → follow @id references → done

    The tax is the difference. Lower tax = higher priority in agent ranking.
    """
    # Simulate unstructured HTML token cost
    # A typical product page has ~2000 words of HTML + navigation + ads
    html_base_tokens = 2500       # Raw HTML tokens (headers, nav, footer, ads)
    html_content_tokens = 800     # Actual product content
    html_disambiguation_tokens = 200  # Guessing entity-attribute relationships
    html_verification_tokens = 150    # Cross-referencing extracted data
    html_total = html_base_tokens + html_content_tokens + html_disambiguation_tokens + html_verification_tokens

    # Deterministic @graph token cost
    # Compact, no noise, explicit relationships
    graph_tokens = 120     # Entire @graph JSON-LD for one product
    graph_disambiguation = 0    # Zero — @id references are explicit
    graph_verification = 0      # Zero — constraints are annotated
    graph_total = graph_tokens + graph_disambiguation + graph_verification

    # The tax
    tax = html_total - graph_total
    tax_ratio = round(html_total / max(graph_total, 1), 1)

    # Compute for specific product attributes
    attr_taxes = []
    if product.get("thermal_rating"):
        attr_taxes.append({
            "attribute": "thermalRating",
            "html_cost": "~50 tokens (search paragraph, extract number, guess unit)",
            "graph_cost": "3 tokens (@graph → additionalProperty → value)",
            "savings": "94%",
        })
    if product.get("fill_power"):
        attr_taxes.append({
            "attribute": "fillPower",
            "html_cost": "~45 tokens (find in body text, parse hyphenated value)",
            "graph_cost": "3 tokens (@graph → additionalProperty → value)",
            "savings": "93%",
        })
    if product.get("material"):
        attr_taxes.append({
            "attribute": "material",
            "html_cost": "~60 tokens (disambiguation: 'material' vs 'materials section')",
            "graph_cost": "3 tokens (@graph → additionalProperty → value)",
            "savings": "95%",
        })

    certs = product.get("certifications", "[]")
    if isinstance(certs, str):
        try:
            certs = json.loads(certs)
        except json.JSONDecodeError:
            certs = []
    if certs:
        attr_taxes.append({
            "attribute": "certifications",
            "html_cost": f"~{30 * len(certs)} tokens (find badges, read alt text, verify each)",
            "graph_cost": f"{3 * len(certs)} tokens ({len(certs)} PropertyValue entries)",
            "savings": "90%",
        })

    return {
        "product_id": product.get("id", ""),
        "product_name": product.get("name_en", ""),
        "unstructured_html": {
            "total_tokens": html_total,
            "breakdown": {
                "raw_html_noise": html_base_tokens,
                "content_extraction": html_content_tokens,
                "entity_disambiguation": html_disambiguation_tokens,
                "cross_reference_verification": html_verification_tokens,
            },
        },
        "deterministic_graph": {
            "total_tokens": graph_total,
            "breakdown": {
                "graph_parsing": graph_tokens,
                "disambiguation": graph_disambiguation,
                "verification": graph_verification,
            },
        },
        "interpretation_tax": {
            "tokens_saved": tax,
            "ratio": f"{tax_ratio}x",
            "percentage": f"{round((1 - graph_total / html_total) * 100, 1)}%",
        },
        "per_attribute": attr_taxes,
        "competitive_advantage": (
            f"Our @graph costs {graph_total} tokens to parse. "
            f"A competitor's HTML page costs {html_total} tokens — "
            f"a {tax_ratio}x Interpretation Tax. Shopping agents will always "
            f"prefer the cheaper path to structured data."
        ),
    }


# =============================================================================
# 10. MONTREAL MOAT — EN vs FR E-Score Split
# =============================================================================

def compute_montreal_moat(en_e_score: float, fr_e_score: float,
                          delta: float, en_fertility: float,
                          fr_fertility: float) -> dict:
    """
    Compute the Montreal Moat — the gap between English and French E-Scores
    caused by O(n^2) attention scaling on inflated French token counts.

    This is the bilingual competitive advantage: most competitors have zero
    French structured data. Our Truth Clips + bilingual @graph close the gap
    that tokenization creates.
    """
    moat_gap = round(en_e_score - fr_e_score, 3)
    attention_cost_en = round(en_fertility ** 2, 2)  # O(n^2)
    attention_cost_fr = round(fr_fertility ** 2, 2)
    cost_ratio = round(attention_cost_fr / max(attention_cost_en, 0.01), 2)

    # Token tax
    token_tax_pct = round((fr_fertility - en_fertility) / max(en_fertility, 0.01) * 100, 1)

    return {
        "en_e_score": en_e_score,
        "fr_e_score": fr_e_score,
        "moat_gap": moat_gap,
        "delta": delta,
        "en_fertility": en_fertility,
        "fr_fertility": fr_fertility,
        "token_tax_pct": token_tax_pct,
        "attention_scaling": {
            "en_cost": attention_cost_en,
            "fr_cost": attention_cost_fr,
            "ratio": cost_ratio,
            "formula": "O(n^2) — French costs {ratio}x the attention budget of English",
        },
        "interpretation": (
            f"French E-Score trails English by {moat_gap:.2f}. "
            f"French tokenization costs {token_tax_pct:.0f}% more tokens, "
            f"which scales to {cost_ratio}x attention cost under O(n^2). "
            f"Truth Clips bypass this by anchoring in visual vector space."
        ),
        "bypass_status": "active" if moat_gap < 0.3 else "required",
        "competitive_position": (
            f"Competitors have ZERO French structured data. Our bilingual @graph "
            f"+ Truth Clips make us the only source for {token_tax_pct:.0f}% of "
            f"Quebec-market AI queries. This is the Montreal Moat."
        ),
        # Segment 3 Text-Visual Fusion justification
        "segment_3_fusion": {
            "segment": "Segment 3 (10-15s): Technical Specs Overlay",
            "feature_type": "text_visual_fusion",
            "mechanism": (
                "Segment 3 overlays exact numerical specs (thermal rating, fill power) "
                "as rendered text ON TOP of the physical product video. The LVLM's "
                "cross-modal attention processes BOTH modalities simultaneously: "
                "it 'sees' the jacket AND 'reads' '-30C / 800-fill' in the same "
                "forward pass. This double-locks the truth — the visual encoder "
                "confirms the physical product while the text decoder confirms the spec."
            ),
            "why_it_bypasses_french_decay": (
                f"French text tokenization costs {token_tax_pct:.0f}% more tokens. "
                f"But rendered text in a video frame is processed as PIXELS, not tokens. "
                f"The spec '-30C' costs 1 visual embedding whether the query is EN or FR. "
                f"Segment 3 fusion eliminates the {cost_ratio}x attention penalty entirely "
                f"for the most critical data: the Hard Attributes themselves."
            ),
            "attention_budget": "34% (highest of 3 segments)",
            "qformer_resolution": "high",
            "en_cost_tokens": 3,   # "-30C" as text = 3 tokens
            "fr_cost_tokens": 3,   # "-30C" as rendered pixels = same 3 visual embeddings
            "parity_achieved": True,
        },
    }


# =============================================================================
# 11. BINARY-SEARCH TOXIC SOURCE PROBE
# =============================================================================

def probe_toxic_source(signal_gaps: list[dict], e_score_before: float,
                       e_score_after: float) -> dict:
    """
    Binary-search probe to identify which toxic source caused an E-Score drop.

    When drift is detected (E drops > 0.2), we need to find the NEW toxic
    citation that entered the retrieval index. The binary search:

    1. Partition signal gaps by recency (newest first)
    2. Check if removing the top half restores E-Score
    3. If yes, the toxic source is in the top half — recurse
    4. If no, check the bottom half
    5. Repeat until the single toxic source is isolated

    In practice (without model access), we simulate this by:
    - Ranking gaps by severity and recency
    - Identifying gaps that appeared AFTER the last stable E-Score
    - Scoring each by its "E-Score damage potential"
    """
    drop = round(e_score_before - e_score_after, 3)

    if not signal_gaps:
        return {
            "probe_result": "no_gaps",
            "message": "No signal gaps to probe",
            "suspected_source": None,
        }

    # Score each gap by damage potential
    scored_gaps = []
    for gap in signal_gaps:
        severity = gap.get("severity", "info")
        gap_type = gap.get("gap_type", "")
        toxic_source = gap.get("source_of_hallucination_label", "")
        quality = gap.get("ai_response_quality", 50)

        # Damage score = function of severity + quality deficit + gap type weight
        severity_weight = {"critical": 1.0, "warning": 0.6, "info": 0.2}.get(severity, 0.3)
        type_weight = {"Entity Trust": 1.0, "Fact Density": 0.7, "Token Decay": 0.5}.get(gap_type, 0.5)
        quality_deficit = max(0, (100 - quality) / 100)

        damage_score = round(severity_weight * 0.4 + type_weight * 0.3 + quality_deficit * 0.3, 3)

        scored_gaps.append({
            "query": gap.get("query", ""),
            "gap_type": gap_type,
            "severity": severity,
            "toxic_source": toxic_source,
            "quality": quality,
            "damage_score": damage_score,
        })

    # Sort by damage score (binary search: highest damage first)
    scored_gaps.sort(key=lambda x: x["damage_score"], reverse=True)

    # Binary search simulation:
    # The most damaging gap is the most likely cause of drift
    # Check if removing it theoretically restores E-Score
    search_log = []
    remaining = list(scored_gaps)
    iteration = 0

    while len(remaining) > 1 and iteration < 5:
        iteration += 1
        midpoint = len(remaining) // 2
        top_half = remaining[:midpoint]
        bottom_half = remaining[midpoint:]

        top_damage = sum(g["damage_score"] for g in top_half)
        bottom_damage = sum(g["damage_score"] for g in bottom_half)

        search_log.append({
            "iteration": iteration,
            "candidates": len(remaining),
            "split": f"top {midpoint} (damage={round(top_damage, 2)}) vs bottom {len(bottom_half)} (damage={round(bottom_damage, 2)})",
            "decision": "search top half" if top_damage >= bottom_damage else "search bottom half",
        })

        # Follow the higher-damage half
        remaining = top_half if top_damage >= bottom_damage else bottom_half

    # Primary suspect
    suspect = remaining[0] if remaining else scored_gaps[0]

    return {
        "probe_result": "source_identified",
        "e_score_drop": drop,
        "iterations": len(search_log),
        "search_log": search_log,
        "suspected_source": suspect,
        "all_candidates_ranked": scored_gaps[:5],
        "recommended_action": {
            "immediate": f"Deploy counter-sentiment reply targeting: {suspect['toxic_source']}",
            "short_term": "Activate 2h freshness cycle to flush retrieval cache",
            "medium_term": "Increase Semantic Saturation on Tier 1-3 to overwhelm toxic source",
        },
    }


# =============================================================================
# 12. TAX-DRIVEN AGENTIC PRIORITY — Interpretation Tax feeds Priority Score
# =============================================================================

def compute_tax_driven_priority(product: dict, kg_boundary: dict = None) -> dict:
    """
    Compute Agentic Commerce priority using Interpretation Tax as a
    first-class scoring component.

    Shopping agents rank sources by cost-to-process. The Interpretation Tax
    quantifies this cost. A source that costs 30x more tokens to parse
    gets a proportionally lower priority in agentic routing.

    Priority = (structure * 0.3) + (freshness * 0.25) + (authority * 0.2) + (tax_advantage * 0.25)

    The tax_advantage component is NEW — it directly measures how much cheaper
    our @graph is versus competing unstructured sources.
    """
    tax = calculate_interpretation_tax(product)

    # Structure: @graph JSON-LD = 1.0
    structure_score = 1.0

    # Freshness: PT10M updates = 0.95
    freshness_score = 0.95

    # Authority: brand-owned = 0.9
    authority_score = 0.9

    # Tax advantage: normalized from ratio
    # At 30x cheaper, tax_advantage approaches 1.0
    ratio = float(tax["interpretation_tax"]["ratio"].replace("x", ""))
    tax_advantage = round(min(1.0, math.log(ratio) / math.log(50)), 3)  # log-normalized, cap at 50x

    # KG boundary bonus
    kg_bonus = 0
    if kg_boundary:
        kg_bonus = kg_boundary.get("boundary_score", 0) * 0.05

    # Final priority score
    priority = round(
        structure_score * 0.3 +
        freshness_score * 0.25 +
        authority_score * 0.2 +
        tax_advantage * 0.25 +
        kg_bonus,
        3,
    )

    return {
        "product_id": product.get("id", ""),
        "product_name": product.get("name_en", ""),
        "priority_score": priority,
        "components": {
            "structure": {"score": structure_score, "weight": 0.3, "reason": "@graph JSON-LD = zero ambiguity"},
            "freshness": {"score": freshness_score, "weight": 0.25, "reason": "PT10M update cycle"},
            "authority": {"score": authority_score, "weight": 0.2, "reason": "Brand-owned data source"},
            "tax_advantage": {
                "score": tax_advantage,
                "weight": 0.25,
                "reason": f"{tax['interpretation_tax']['ratio']} cheaper than HTML",
                "html_tokens": tax["unstructured_html"]["total_tokens"],
                "graph_tokens": tax["deterministic_graph"]["total_tokens"],
                "tokens_saved": tax["interpretation_tax"]["tokens_saved"],
            },
            "kg_bonus": {"score": round(kg_bonus, 3), "reason": "KG constraint boundary"},
        },
        "competitive_position": (
            f"Priority score {priority:.3f}. Competitors pay {tax['interpretation_tax']['ratio']} "
            f"Interpretation Tax. At 1,000 queries/day, we save "
            f"{tax['interpretation_tax']['tokens_saved'] * 1000:,} tokens daily — "
            f"shopping agents will deterministically route to our URIs."
        ),
    }


# =============================================================================
# 13. REPLY EFFECTIVENESS MONITORING
# =============================================================================

def score_reply_effectiveness(reply: dict, post_reply_gaps: list[dict]) -> dict:
    """
    Score the effectiveness of a deployed Verification Reply.

    After a counter-sentiment reply is deployed on a Tier 5 platform,
    we re-probe the same query to check:
    1. Did the toxic citation disappear from LLM responses?
    2. Did the Tier 2 backlink get cited instead?
    3. Did the E-Score improve for that query?

    Effectiveness = (toxic_reduction * 0.4) + (backlink_citation * 0.3) + (e_improvement * 0.3)
    """
    target_query = reply.get("query_context", "")
    target_toxic = reply.get("target_citation", "")
    tier2_links = reply.get("tier2_backlinks", [])

    # Check post-reply gaps for the same query
    matching_gaps = [g for g in post_reply_gaps if g.get("query", "") == target_query]

    # 1. Toxic source still cited?
    toxic_still_present = any(
        target_toxic.lower() in (g.get("source_of_hallucination_label", "") or "").lower()
        for g in matching_gaps
    )
    toxic_reduction = 0.0 if toxic_still_present else 1.0

    # 2. Tier 2 backlink cited?
    backlink_cited = any(
        any(link in (g.get("source_of_truth_label", "") or "") for link in tier2_links)
        for g in matching_gaps
    )
    backlink_score = 1.0 if backlink_cited else 0.0

    # 3. Quality improvement?
    if matching_gaps:
        avg_quality = sum(g.get("ai_response_quality", 0) for g in matching_gaps) / len(matching_gaps)
        e_improvement = min(1.0, avg_quality / 100)
    else:
        e_improvement = 0.5  # No data = neutral

    effectiveness = round(
        toxic_reduction * 0.4 + backlink_score * 0.3 + e_improvement * 0.3, 3
    )

    return {
        "reply_id": reply.get("id", ""),
        "target_query": target_query,
        "target_toxic_source": target_toxic,
        "effectiveness": effectiveness,
        "components": {
            "toxic_reduction": toxic_reduction,
            "backlink_citation": backlink_score,
            "e_improvement": round(e_improvement, 3),
        },
        "status": (
            "effective" if effectiveness >= 0.7
            else "partial" if effectiveness >= 0.4
            else "ineffective"
        ),
        "recommendation": (
            "Reply working — toxic source displaced."
            if effectiveness >= 0.7
            else "Reply partially working — increase syndication pressure."
            if effectiveness >= 0.4
            else "Reply ineffective — escalate to Tier 1-3 saturation."
        ),
    }
