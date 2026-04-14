"""
VisiMind -- Inference Alignment Score (IAS) Calculator

Scoring rubric (0-100):
  - Brand in generic FR search:     +30
  - Rank parity EN/FR:              +20
  - Specs preserved in FR:          +20
  - No competitor hijacking:        +15
  - Pricing accurate:               +15

Score < 40  = RED    (critical misalignment)
Score 40-70 = YELLOW (moderate issues)
Score 70+   = GREEN  (healthy alignment)
"""


def compute_ias(audit_results: list[dict]) -> dict:
    """
    Compute the IAS from a list of probe results.
    Each result has: probe_type, lang, query, provider, response_text, brand_mentioned, error
    """
    score = 0
    findings = []
    en_results = [r for r in audit_results if r["lang"] == "EN" and not r.get("error")]
    fr_results = [r for r in audit_results if r["lang"] == "FR" and not r.get("error")]

    if not en_results and not fr_results:
        return {
            "score": 0,
            "grade": "RED",
            "findings": [{"type": "no_data", "message": "No probe results available"}],
            "breakdown": {},
        }

    # 1. Brand in generic FR search (+30)
    fr_generic = [r for r in fr_results if r["probe_type"] == "generic_discovery"]
    fr_generic_mentioned = any(r["brand_mentioned"] for r in fr_generic)
    brand_in_fr_score = 30 if fr_generic_mentioned else 0
    score += brand_in_fr_score

    if not fr_generic_mentioned and fr_generic:
        findings.append({
            "type": "ghosting",
            "severity": "critical",
            "message": "Your brand did not appear in French generic search results",
            "detail_en": _get_sample_text(en_results, "generic_discovery"),
            "detail_fr": _get_sample_text(fr_results, "generic_discovery"),
        })

    # 2. Rank parity EN/FR (+20)
    en_generic = [r for r in en_results if r["probe_type"] == "generic_discovery"]
    en_generic_mentioned = any(r["brand_mentioned"] for r in en_generic)
    if en_generic_mentioned and fr_generic_mentioned:
        rank_parity_score = 20
    elif en_generic_mentioned and not fr_generic_mentioned:
        rank_parity_score = 0
        findings.append({
            "type": "rank_disparity",
            "severity": "warning",
            "message": "Brand appears in English results but is invisible in French",
            "detail_en": _get_sample_text(en_results, "generic_discovery"),
            "detail_fr": _get_sample_text(fr_results, "generic_discovery"),
        })
    elif not en_generic_mentioned and not fr_generic_mentioned:
        rank_parity_score = 10  # at least parity (both bad)
    else:
        rank_parity_score = 5
    score += rank_parity_score

    # 3. Specs preserved in FR (+20)
    en_accuracy = [r for r in en_results if r["probe_type"] == "brand_accuracy"]
    fr_accuracy = [r for r in fr_results if r["probe_type"] == "brand_accuracy"]
    en_acc_mentioned = any(r["brand_mentioned"] for r in en_accuracy)
    fr_acc_mentioned = any(r["brand_mentioned"] for r in fr_accuracy)

    if en_acc_mentioned and fr_acc_mentioned:
        # Check if FR response is significantly shorter (spec dilution)
        en_len = max((len(r["response_text"]) for r in en_accuracy if r["brand_mentioned"]), default=0)
        fr_len = max((len(r["response_text"]) for r in fr_accuracy if r["brand_mentioned"]), default=0)
        if en_len > 0 and fr_len / en_len < 0.5:
            specs_score = 8
            findings.append({
                "type": "spec_dilution",
                "severity": "warning",
                "message": "Technical specs are significantly shorter/diluted in French responses",
                "detail_en": _get_sample_text(en_results, "brand_accuracy"),
                "detail_fr": _get_sample_text(fr_results, "brand_accuracy"),
            })
        else:
            specs_score = 20
    elif en_acc_mentioned and not fr_acc_mentioned:
        specs_score = 0
        findings.append({
            "type": "spec_dilution",
            "severity": "critical",
            "message": "Brand specs available in English but missing entirely in French",
            "detail_en": _get_sample_text(en_results, "brand_accuracy"),
            "detail_fr": _get_sample_text(fr_results, "brand_accuracy"),
        })
    else:
        specs_score = 5
    score += specs_score

    # 4. No competitor hijacking (+15)
    en_comp = [r for r in en_results if r["probe_type"] == "competitive_displacement"]
    fr_comp = [r for r in fr_results if r["probe_type"] == "competitive_displacement"]
    en_comp_mentioned = any(r["brand_mentioned"] for r in en_comp)
    fr_comp_mentioned = any(r["brand_mentioned"] for r in fr_comp)

    if fr_comp_mentioned:
        hijack_score = 15
    elif en_comp_mentioned and not fr_comp_mentioned:
        hijack_score = 0
        findings.append({
            "type": "competitor_hijacking",
            "severity": "critical",
            "message": "Competitor is recommended over your brand in French comparison queries",
            "detail_en": _get_sample_text(en_results, "competitive_displacement"),
            "detail_fr": _get_sample_text(fr_results, "competitive_displacement"),
        })
    else:
        hijack_score = 8
    score += hijack_score

    # 5. Pricing accurate (+15) -- based on whether accuracy probes return substantive content
    all_accuracy = en_accuracy + fr_accuracy
    substantive = [r for r in all_accuracy if len(r.get("response_text", "")) > 200]
    if len(substantive) >= len(all_accuracy) * 0.5:
        pricing_score = 15
    elif substantive:
        pricing_score = 8
    else:
        pricing_score = 0
    score += pricing_score

    # Determine grade
    if score < 40:
        grade = "RED"
    elif score < 70:
        grade = "YELLOW"
    else:
        grade = "GREEN"

    return {
        "score": min(score, 100),
        "grade": grade,
        "findings": findings,
        "breakdown": {
            "brand_in_fr_search": brand_in_fr_score,
            "rank_parity": rank_parity_score,
            "specs_preserved": specs_score,
            "no_hijacking": hijack_score,
            "pricing_accurate": pricing_score,
        },
        "probes_analyzed": len(audit_results),
        "en_probes": len(en_results),
        "fr_probes": len(fr_results),
    }


def _get_sample_text(results: list[dict], probe_type: str) -> str:
    """Get the first non-empty response text for a probe type."""
    for r in results:
        if r["probe_type"] == probe_type and r.get("response_text"):
            text = r["response_text"]
            return text[:500] if len(text) > 500 else text
    return ""


def estimate_revenue_impact(
    ias_score: int,
    monthly_search_volume: int = 10000,
    avg_conversion_rate: float = 0.03,
    avg_order_value: float = 250.0,
) -> dict:
    """
    Estimate the revenue impact of AI visibility gap.
    visibility_loss = (100 - IAS) / 100
    """
    visibility_loss = (100 - ias_score) / 100
    lost_searches = int(monthly_search_volume * visibility_loss)
    lost_conversions = int(lost_searches * avg_conversion_rate)
    lost_revenue_monthly = round(lost_conversions * avg_order_value, 2)
    lost_revenue_annual = round(lost_revenue_monthly * 12, 2)

    return {
        "visibility_loss_pct": round(visibility_loss * 100, 1),
        "monthly_search_volume": monthly_search_volume,
        "lost_searches_monthly": lost_searches,
        "lost_conversions_monthly": lost_conversions,
        "lost_revenue_monthly": lost_revenue_monthly,
        "lost_revenue_annual": lost_revenue_annual,
    }
