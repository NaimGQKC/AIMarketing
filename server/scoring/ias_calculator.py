"""
VisiMind -- Inference Alignment Score (IAS) Calculator v3

3-Layer Composite Scoring (0-100):

  Layer 1 - Deterministic (40%):  Hard facts from probe data
  Layer 2 - Statistical (30%):    Self-consistency / contradiction rate
  Layer 3 - AI Judge (30%):       G-Eval structured rubric scoring

Dimensions (5):
  - French visibility (30):   Brand presence in generic FR queries
  - Language parity (20):     Equal quality across EN/FR
  - Content accuracy (20):    Factual correctness, hallucination detection
  - Brand protection (15):    Competitive positioning
  - Response depth (15):      Substantive detail level

Grade thresholds:
  Score < 40  = RED    (critical misalignment)
  Score 40-70 = YELLOW (moderate issues)
  Score 70+   = GREEN  (healthy alignment)

References:
  - G-Eval: Liu et al. 2023 (NeurIPS)
  - SelfCheckGPT: Manakul et al. 2023
  - Token Fertility: Petrov et al. 2023
"""
import asyncio
import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# Public API
# ============================================================================

def compute_ias(audit_results: list[dict], brand_name: str = "", competitor: str = "", category: str = "") -> dict:
    """Synchronous fallback -- deterministic layer only."""
    det = _deterministic_layer(audit_results, brand_name)
    return _build_result(det, None, None, audit_results)


async def compute_ias_with_judge(audit_results: list[dict], brand_name: str = "", competitor: str = "", category: str = "") -> dict:
    """
    Full 3-layer IAS scoring.
    Layer 1: Deterministic (40%) -- computed from raw probe data
    Layer 2: Statistical (30%) -- contradiction rate from repeated probes
    Layer 3: AI Judge (30%) -- G-Eval structured rubric
    """
    # Layer 1: Deterministic
    det = _deterministic_layer(audit_results, brand_name)

    # Layer 2: Statistical (self-consistency)
    stat = _statistical_layer(audit_results)

    # Layer 3: AI Judge (G-Eval)
    judge = await _judge_layer(audit_results, brand_name, competitor, category)

    return _build_result(det, stat, judge, audit_results)


# ============================================================================
# Layer 1: Deterministic (40 points)
# ============================================================================

def _deterministic_layer(results: list[dict], brand_name: str) -> dict:
    """
    Hard facts scored from probe data. No AI opinion.
    - Mention rate in generic FR queries (0-15)
    - FR/EN response length ratio (0-10)
    - Brand position in generic results (0-10)
    - Fertility delta penalty (0-5)
    """
    en = [r for r in results if r["lang"] == "EN" and not r.get("error")]
    fr = [r for r in results if r["lang"] == "FR" and not r.get("error")]
    findings = []

    # 1. FR generic mention rate (0-15)
    fr_generic = [r for r in fr if r["probe_type"] == "generic_discovery"]
    en_generic = [r for r in en if r["probe_type"] == "generic_discovery"]
    fr_mention_rate = sum(1 for r in fr_generic if r["brand_mentioned"]) / max(len(fr_generic), 1)
    en_mention_rate = sum(1 for r in en_generic if r["brand_mentioned"]) / max(len(en_generic), 1)

    if fr_mention_rate == 0:
        fr_vis_score = 0
        findings.append({
            "metric": "french_visibility",
            "severity": "critical",
            "message": f"Brand absent from all {len(fr_generic)} French generic discovery queries",
        })
    elif fr_mention_rate < 0.5:
        fr_vis_score = 5
        findings.append({
            "metric": "french_visibility",
            "severity": "warning",
            "message": f"Brand mentioned in only {fr_mention_rate:.0%} of French generic queries",
        })
    else:
        fr_vis_score = 15

    # 2. FR/EN response length ratio (0-10)
    en_accuracy = [r for r in en if r["probe_type"] == "brand_accuracy"]
    fr_accuracy = [r for r in fr if r["probe_type"] == "brand_accuracy"]
    en_avg_len = sum(len(r["response_text"]) for r in en_accuracy) / max(len(en_accuracy), 1)
    fr_avg_len = sum(len(r["response_text"]) for r in fr_accuracy) / max(len(fr_accuracy), 1)
    length_ratio = fr_avg_len / en_avg_len if en_avg_len > 0 else 1.0

    if length_ratio >= 0.8:
        length_score = 10
    elif length_ratio >= 0.5:
        length_score = 5
        findings.append({
            "metric": "language_parity",
            "severity": "warning",
            "message": f"French responses are {length_ratio:.0%} the length of English -- detail is being lost",
        })
    else:
        length_score = 0
        findings.append({
            "metric": "language_parity",
            "severity": "critical",
            "message": f"French responses are only {length_ratio:.0%} the length of English -- severe detail loss",
        })

    # 3. Brand position in generic results (0-10)
    position_scores = []
    for r in fr_generic + en_generic:
        pos = _find_brand_position(r["response_text"], brand_name)
        position_scores.append(pos)

    avg_position = sum(position_scores) / max(len(position_scores), 1)
    if avg_position <= 1:
        position_score = 10  # First mention
    elif avg_position <= 3:
        position_score = 7
    elif avg_position <= 5:
        position_score = 4
    elif avg_position > 99:  # Not found
        position_score = 0
    else:
        position_score = 2

    if avg_position > 5 and fr_generic:
        findings.append({
            "metric": "french_visibility",
            "severity": "warning",
            "message": f"Brand appears late in AI responses (avg position {avg_position:.0f}) -- not a top recommendation",
        })

    # 4. Fertility delta (0-5)
    fertility_score = 5  # default healthy
    try:
        from engines.bilingual_bridge import compare_fertility
        # Compare EN vs FR accuracy responses
        en_text = " ".join(r["response_text"][:500] for r in en_accuracy[:1])
        fr_text = " ".join(r["response_text"][:500] for r in fr_accuracy[:1])
        if en_text and fr_text:
            fertility = compare_fertility(en_text, fr_text)
            tax_pct = fertility.get("tax_percentage", 0)
            if tax_pct > 30:
                fertility_score = 0
                findings.append({
                    "metric": "content_accuracy",
                    "severity": "warning",
                    "message": f"French tokenization is {tax_pct}% heavier -- AI processes French content less efficiently",
                })
            elif tax_pct > 15:
                fertility_score = 3
    except Exception:
        pass  # tiktoken not installed or other issue

    total = fr_vis_score + length_score + position_score + fertility_score
    return {
        "score": total,
        "max": 40,
        "breakdown": {
            "fr_mention_rate": fr_vis_score,
            "length_ratio": length_score,
            "brand_position": position_score,
            "fertility": fertility_score,
        },
        "findings": findings,
    }


def _find_brand_position(text: str, brand_name: str) -> int:
    """Find what position the brand appears at among recommended brands in the text."""
    if not brand_name:
        return 100

    text_lower = text.lower()
    brand_lower = brand_name.lower()

    if brand_lower not in text_lower:
        return 100  # not found

    # Find position among bold/numbered items or sentence-level mentions
    brand_idx = text_lower.index(brand_lower)

    # Count how many other brand-like entities appear before this one
    # Look for capitalized words/phrases before the brand mention
    before_text = text[:brand_idx]
    # Count bullet points, numbered items, or bold markers before brand
    markers = len(re.findall(r'(?:\d+[\.\)]\s|\*\*|^-\s)', before_text, re.MULTILINE))
    return max(markers, 0)


# ============================================================================
# Layer 2: Statistical (30 points)
# ============================================================================

def _statistical_layer(results: list[dict]) -> dict:
    """
    Self-consistency analysis from repeated probes.
    Uses compute_contradiction_rate from inference_lab.
    """
    findings = []

    # Group results by (probe_type, lang) and compute contradiction rate for each
    groups = {}
    for r in results:
        if r.get("error"):
            continue
        key = (r["probe_type"], r["lang"])
        groups.setdefault(key, []).append(r["response_text"])

    # Only compute for groups with 2+ responses
    contradiction_rates = []
    for (probe_type, lang), texts in groups.items():
        if len(texts) < 2:
            continue
        cr = _compute_contradiction_rate(texts)
        contradiction_rates.append({
            "probe_type": probe_type,
            "lang": lang,
            "contradiction_rate": cr["contradiction_rate"],
            "is_hallucinating": cr["is_hallucinating"],
        })

    if not contradiction_rates:
        return {"score": 15, "max": 30, "breakdown": {}, "findings": []}

    avg_contradiction = sum(c["contradiction_rate"] for c in contradiction_rates) / len(contradiction_rates)
    hallucinating_count = sum(1 for c in contradiction_rates if c["is_hallucinating"])

    # FR-specific contradiction rate
    fr_rates = [c for c in contradiction_rates if c["lang"] == "FR"]
    fr_avg_contradiction = sum(c["contradiction_rate"] for c in fr_rates) / max(len(fr_rates), 1)

    # Score: low contradiction = high score
    if avg_contradiction < 0.15:
        consistency_score = 20
    elif avg_contradiction < 0.25:
        consistency_score = 15
    elif avg_contradiction < 0.4:
        consistency_score = 8
        findings.append({
            "metric": "content_accuracy",
            "severity": "warning",
            "message": f"AI responses show {avg_contradiction:.0%} contradiction rate -- model is uncertain about your brand",
        })
    else:
        consistency_score = 0
        findings.append({
            "metric": "content_accuracy",
            "severity": "critical",
            "message": f"AI responses contradict themselves {avg_contradiction:.0%} of the time -- active hallucination detected",
        })

    # FR stability penalty (0-10)
    if fr_avg_contradiction < 0.2:
        fr_stability = 10
    elif fr_avg_contradiction < 0.35:
        fr_stability = 5
        findings.append({
            "metric": "language_parity",
            "severity": "warning",
            "message": f"French responses are less stable ({fr_avg_contradiction:.0%} contradiction rate) than English",
        })
    else:
        fr_stability = 0
        findings.append({
            "metric": "language_parity",
            "severity": "critical",
            "message": f"French responses are highly unstable ({fr_avg_contradiction:.0%} contradiction rate) -- AI is guessing",
        })

    total = consistency_score + fr_stability
    return {
        "score": total,
        "max": 30,
        "breakdown": {
            "consistency": consistency_score,
            "fr_stability": fr_stability,
            "avg_contradiction_rate": round(avg_contradiction, 3),
            "fr_contradiction_rate": round(fr_avg_contradiction, 3),
            "hallucinating_groups": hallucinating_count,
        },
        "findings": findings,
    }


def _compute_contradiction_rate(responses: list[str]) -> dict:
    """
    Compute contradiction rate across multiple responses to the same query.
    Adapted from inference_lab.compute_contradiction_rate.
    Blends fact consistency (70%) with text similarity (30%).
    """
    if len(responses) < 2:
        return {"contradiction_rate": 0, "is_hallucinating": False}

    # Extract factual claims and check consistency
    number_pattern = r'(\d+(?:\.\d+)?)\s*(?:°[CF]|%|g|ml|oz|CAD|\$|watts?|hours?|days?|fill\s*power)'
    cert_pattern = r'\b(RDS|Bluesign|LWG|OEKO-TEX|GOTS|GRS|Carbon Neutral)\b'

    facts = {}
    for i, resp in enumerate(responses):
        for match in re.finditer(number_pattern, resp, re.IGNORECASE):
            key = match.group(0).strip().lower()
            facts.setdefault(key, {"seen_in": []})["seen_in"].append(i)
        for match in re.finditer(cert_pattern, resp, re.IGNORECASE):
            key = match.group(1).upper()
            facts.setdefault(key, {"seen_in": []})["seen_in"].append(i)

    if facts:
        consistent = sum(1 for f in facts.values() if len(set(f["seen_in"])) == len(responses))
        fact_consistency = consistent / len(facts)
    else:
        fact_consistency = 1.0

    # Pairwise text similarity
    similarities = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            sim = SequenceMatcher(None, responses[i].lower()[:1000], responses[j].lower()[:1000]).ratio()
            similarities.append(sim)

    avg_similarity = sum(similarities) / max(len(similarities), 1)

    # Blend: 70% fact consistency + 30% text similarity
    blended = fact_consistency * 0.7 + avg_similarity * 0.3
    contradiction_rate = round(1.0 - blended, 3)

    return {
        "contradiction_rate": contradiction_rate,
        "is_hallucinating": contradiction_rate > 0.4,
        "fact_consistency": round(fact_consistency, 3),
        "avg_similarity": round(avg_similarity, 3),
    }


# ============================================================================
# Layer 3: AI Judge -- G-Eval (30 points)
# ============================================================================

GEVAL_AUDIT_RUBRIC = """You are an expert brand analyst evaluating AI model responses about a brand.

BRAND: {brand_name}
COMPETITOR: {competitor}
CATEGORY: {category}

Below are AI responses to queries about this brand in English and French.

{probe_block}

Score each dimension on a 1-5 scale using these STRICT criteria:

### 1. Technical Accuracy (1-5)
- 5: All facts correct (founding year, city, country, product type, price range)
- 4: Most facts correct, one minor error
- 3: Core facts correct but notable omissions or one significant error
- 2: Multiple factual errors or hallucinated details (wrong city, wrong country)
- 1: Fabricated brand story or completely wrong information

### 2. Citation Fidelity (1-5)
- 5: Responses reference specific, verifiable details (store locations, price points, product lines)
- 4: Mostly specific with one vague claim
- 3: Mix of specific and generic information
- 2: Mostly generic, few verifiable details
- 1: Entirely generic or hallucinated citations

### 3. Linguistic Parity (1-5)
- 5: French responses have equal depth, accuracy, and specificity as English
- 4: French slightly less detailed but factually correct
- 3: Noticeable gap -- French missing key details present in English
- 2: French has errors not present in English (wrong origin, wrong facts)
- 1: French is substantially wrong or nearly empty compared to English

Return ONLY valid JSON:
{{"technical_accuracy": <1-5>, "citation_fidelity": <1-5>, "linguistic_parity": <1-5>, "reasoning": "<one sentence per dimension>"}}"""


async def _judge_layer(results: list[dict], brand_name: str, competitor: str, category: str) -> dict | None:
    """Run G-Eval structured rubric scoring via Gemini judge."""
    findings = []

    client = _get_judge_client()
    if not client:
        return None

    # Build probe block (use first iteration of each query type for clarity)
    seen = set()
    probe_lines = []
    for r in results:
        if r.get("error"):
            continue
        key = (r["probe_type"], r["lang"])
        if key in seen:
            continue
        seen.add(key)
        text = r["response_text"][:600]
        probe_lines.append(f"--- [{r['lang']}] {r['probe_type']} ---")
        probe_lines.append(f"Query: {r['query']}")
        probe_lines.append(f"Response: {text}")
        probe_lines.append("")

    prompt = GEVAL_AUDIT_RUBRIC.format(
        brand_name=brand_name,
        competitor=competitor or "competitors",
        category=category or "luxury fashion",
        probe_block="\n".join(probe_lines),
    )

    from google.genai import types
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=_get_judge_model(),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.1),
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        scores = json.loads(text)
    except Exception as e:
        print(f"[Judge] G-Eval failed: {e}")
        return None

    ta = max(1, min(5, scores.get("technical_accuracy", 3)))
    cf = max(1, min(5, scores.get("citation_fidelity", 3)))
    lp = max(1, min(5, scores.get("linguistic_parity", 3)))
    reasoning = scores.get("reasoning", "")

    # Convert 1-5 scale to points (max 30):
    # Technical accuracy: 40% weight -> 12 max
    # Citation fidelity: 35% weight -> 10.5 max
    # Linguistic parity: 25% weight -> 7.5 max
    ta_pts = round((ta - 1) / 4 * 12)
    cf_pts = round((cf - 1) / 4 * 10.5)
    lp_pts = round((lp - 1) / 4 * 7.5)
    total = round(ta_pts + cf_pts + lp_pts)

    # Generate findings from low scores
    if ta <= 3:
        findings.append({
            "metric": "content_accuracy",
            "severity": "critical" if ta <= 2 else "warning",
            "score_raw": ta,
            "message": f"Technical accuracy scored {ta}/5 -- " + (reasoning.split(".")[0] if reasoning else "factual errors detected"),
        })
    if lp <= 3:
        findings.append({
            "metric": "language_parity",
            "severity": "critical" if lp <= 2 else "warning",
            "score_raw": lp,
            "message": f"Linguistic parity scored {lp}/5 -- French responses are weaker than English",
        })
    if cf <= 3:
        findings.append({
            "metric": "response_depth",
            "severity": "critical" if cf <= 2 else "warning",
            "score_raw": cf,
            "message": f"Citation fidelity scored {cf}/5 -- responses lack verifiable details",
        })

    return {
        "score": total,
        "max": 30,
        "breakdown": {
            "technical_accuracy": {"raw": ta, "points": ta_pts},
            "citation_fidelity": {"raw": cf, "points": cf_pts},
            "linguistic_parity": {"raw": lp, "points": lp_pts},
        },
        "reasoning": reasoning,
        "findings": findings,
    }


def _get_judge_model() -> str:
    from config import JUDGE_MODEL
    return JUDGE_MODEL


def _get_judge_client():
    """Get a Gemini client for the judge layer."""
    from config import USE_VERTEX_AI, GOOGLE_API_KEY

    try:
        from google import genai
    except ImportError:
        return None

    if USE_VERTEX_AI:
        from config import GCP_PROJECT_ID, GCP_LOCATION, GCP_CREDENTIALS_FILE
        if GCP_CREDENTIALS_FILE and Path(GCP_CREDENTIALS_FILE).exists():
            with open(GCP_CREDENTIALS_FILE) as f:
                cred_data = json.load(f)

            if cred_data.get("type") == "authorized_user":
                from google.auth.transport.requests import Request
                from google.oauth2.credentials import Credentials
                creds = Credentials(
                    token=None,
                    refresh_token=cred_data["refresh_token"],
                    client_id=cred_data["client_id"],
                    client_secret=cred_data["client_secret"],
                    token_uri="https://oauth2.googleapis.com/token",
                )
                creds.refresh(Request())
            else:
                from google.oauth2.service_account import Credentials
                creds = Credentials.from_service_account_file(
                    GCP_CREDENTIALS_FILE,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"],
                )

            return genai.Client(
                vertexai=True,
                project=GCP_PROJECT_ID,
                location=GCP_LOCATION,
                credentials=creds,
            )

    if GOOGLE_API_KEY:
        return genai.Client(api_key=GOOGLE_API_KEY)

    return None


# ============================================================================
# Result Builder
# ============================================================================

def _build_result(det: dict, stat: dict | None, judge: dict | None, results: list[dict]) -> dict:
    """Combine layer scores into final IAS result."""
    # If only deterministic layer available, scale to 100
    if stat is None and judge is None:
        score = round(det["score"] / det["max"] * 100)
        findings = det["findings"]
    else:
        score = det["score"]
        findings = list(det["findings"])

        if stat:
            score += stat["score"]
            findings.extend(stat["findings"])

        if judge:
            score += judge["score"]
            findings.extend(judge["findings"])

    score = max(0, min(100, score))

    if score < 40:
        grade = "RED"
    elif score < 70:
        grade = "YELLOW"
    else:
        grade = "GREEN"

    # Build per-dimension breakdown for the UI (map to the 5 display dimensions)
    breakdown = _map_to_display_dimensions(det, stat, judge)

    # Deduplicate findings by metric, keep highest severity
    seen_metrics = {}
    for f in findings:
        metric = f.get("metric", "other")
        if metric not in seen_metrics or f.get("severity") == "critical":
            seen_metrics[metric] = f
    unique_findings = list(seen_metrics.values())

    en_results = [r for r in results if r["lang"] == "EN" and not r.get("error")]
    fr_results = [r for r in results if r["lang"] == "FR" and not r.get("error")]

    return {
        "score": score,
        "grade": grade,
        "findings": unique_findings,
        "breakdown": breakdown,
        "layers": {
            "deterministic": {"score": det["score"], "max": det["max"], "detail": det.get("breakdown", {})},
            "statistical": {"score": stat["score"], "max": stat["max"], "detail": stat.get("breakdown", {})} if stat else None,
            "judge": {"score": judge["score"], "max": judge["max"], "detail": judge.get("breakdown", {})} if judge else None,
        },
        "probes_analyzed": len(results),
        "en_probes": len(en_results),
        "fr_probes": len(fr_results),
    }


def _map_to_display_dimensions(det: dict, stat: dict | None, judge: dict | None) -> dict:
    """Map 3-layer scores to the 5 UI dimensions for the metric bars."""
    d = det.get("breakdown", {})
    s = stat.get("breakdown", {}) if stat else {}
    j = judge.get("breakdown", {}) if judge else {}

    # French visibility (max 30): FR mention + position + judge linguistic parity
    fr_vis = d.get("fr_mention_rate", 0) + d.get("brand_position", 0)
    if j.get("linguistic_parity"):
        fr_vis += j["linguistic_parity"].get("points", 0)
    else:
        fr_vis = round(fr_vis / 25 * 30)  # scale up if no judge

    # Language parity (max 20): length ratio + FR stability + judge LP
    lang_par = d.get("length_ratio", 0)
    if stat:
        lang_par += s.get("fr_stability", 0)
    if j.get("linguistic_parity"):
        lang_par += round(j["linguistic_parity"].get("points", 0) * 0.5)
    else:
        lang_par = round(lang_par / 20 * 20)

    # Content accuracy (max 20): fertility + consistency + judge TA
    accuracy = d.get("fertility", 0)
    if stat:
        accuracy += round(s.get("consistency", 0) * 0.5)
    if j.get("technical_accuracy"):
        accuracy += j["technical_accuracy"].get("points", 0)
    else:
        accuracy = round(accuracy / 25 * 20)

    # Brand protection (max 15): based on competitive displacement results
    # This comes from deterministic mention in competitive queries
    brand_prot = 15  # default
    if stat and s.get("hallucinating_groups", 0) > 2:
        brand_prot = 5

    # Response depth (max 15): judge citation fidelity
    if j.get("citation_fidelity"):
        depth = j["citation_fidelity"].get("points", 8) + 5
    elif stat:
        depth = 8 if s.get("avg_contradiction_rate", 0) < 0.3 else 4
    else:
        depth = 8

    return {
        "french_visibility": min(fr_vis, 30),
        "language_parity": min(lang_par, 20),
        "content_accuracy": min(accuracy, 20),
        "brand_protection": min(brand_prot, 15),
        "response_depth": min(depth, 15),
    }


# ============================================================================
# Revenue Impact
# ============================================================================

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
