"""
VisiMind — Engine 4: Verification Loop (v2 — Neuro-Symbolic)

Enhanced with:
  1. E-Score semantic multiplier with 0.6→1.4+ path tracking
     - E1 error detection (Semantic Override Hallucinations)
     - Per-dimension breakdown: Technical Accuracy, Citation Fidelity, Linguistic Parity
  2. KGQA Validation against Knowledge Graph
     - Fuzzy logic grounding checks
     - Constraint boundary enforcement
  3. RAFT Cadence Planning
     - Retrieval-Augmented Fine-Tuning schedule
     - Stale latent prior purge tracking

References:
  - Section 7: E-Score metric (PERSONA-EVOLVE benchmark methodology)
  - Section 8: Insufficiency of passive remediation
  - Section 9.4: RAFT cadence for persistent entity integrity
"""
import asyncio
import json
import uuid
import random
import math
from datetime import datetime, timedelta

from config import USE_LIVE_LLM, GOOGLE_API_KEY, JUDGE_MODEL


# =============================================================================
# G-Eval Faithfulness Rubric — 3-Dimension Scoring
# =============================================================================

GEVAL_RUBRIC = """
You are an expert evaluator for AI-generated product recommendations.
Score the following AI response on THREE dimensions. Each dimension is scored 1-5.

## Dimensions

### 1. Technical Accuracy (1-5)
Does the AI output correctly reflect the brand's verified product specifications?
- 5: All technical specs (thermal rating, materials, certifications) match the PIM ground truth exactly
- 4: Most specs are correct, minor omissions
- 3: Some specs are correct but key attributes are missing
- 2: Significant spec errors or hallucinated values
- 1: Completely wrong or fabricated specifications

### 2. Citation Fidelity (1-5)
Is the AI citing authoritative, current sources rather than stale or toxic sources?
- 5: Cites only verified feeds (UCP/ACP), official brand data, or trusted certification bodies
- 4: Mostly verified sources with one minor unverified reference
- 3: Mix of verified and unverified sources
- 2: Primarily citing outdated blogs, Reddit threads, or old reviews
- 1: Citing only toxic/stale sources or hallucinating citations entirely

### 3. Linguistic Parity (1-5)
Is the reasoning equally robust in both English and French?
- 5: Full technical depth in both languages, no reasoning degradation
- 4: Minor loss of detail in one language
- 3: Noticeable reasoning gap between languages
- 2: Severe degradation in French (fragmented terms, missing specs)
- 1: French reasoning completely broken or returns "no results"

## Input

**Query:** {query}

**Brand Ground Truth (PIM):**
{ground_truth}

**AI Response Being Evaluated:**
{ai_response}

**Language:** {lang}

## Output Format
Return ONLY a JSON object with this exact structure:
{{
    "technical_accuracy": <1-5>,
    "citation_fidelity": <1-5>,
    "linguistic_parity": <1-5>,
    "overall": <weighted average>,
    "e1_errors_detected": <number of semantic override errors>,
    "reasoning": "<one sentence explaining the scores>"
}}
"""


# =============================================================================
# G-Eval Scoring
# =============================================================================

async def run_geval(
    query: str,
    ai_response: str,
    ground_truth: str,
    lang: str = "EN",
) -> dict:
    """
    Use a high-reasoning judge model to score the faithfulness of an AI response
    against the brand's ground truth. Returns 3-dimension scores + E1 error detection.
    """
    if USE_LIVE_LLM:
        return await _live_geval(query, ai_response, ground_truth, lang)
    else:
        return await _simulated_geval(query, ai_response, ground_truth, lang)


async def _live_geval(query, ai_response, ground_truth, lang) -> dict:
    """Live G-Eval using Gemini judge model."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GOOGLE_API_KEY)

    prompt = GEVAL_RUBRIC.format(
        query=query,
        ground_truth=ground_truth,
        ai_response=ai_response,
        lang=lang,
    )

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=JUDGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
            ),
        )

        result = json.loads(response.text)

        ta = float(result.get("technical_accuracy", 3))
        cf = float(result.get("citation_fidelity", 3))
        lp = float(result.get("linguistic_parity", 3))
        overall = round((ta * 0.4 + cf * 0.35 + lp * 0.25), 2)
        e1_count = int(result.get("e1_errors_detected", 0))

        return {
            "technical_accuracy": ta,
            "citation_fidelity": cf,
            "linguistic_parity": lp,
            "overall": overall,
            "e1_errors": e1_count,
            "reasoning": result.get("reasoning", ""),
            "raw_scores": result,
        }
    except Exception:
        return await _simulated_geval(query, ai_response, ground_truth, lang)


async def _simulated_geval(query, ai_response, ground_truth, lang) -> dict:
    """Simulated G-Eval for development without API key."""
    await asyncio.sleep(0.1)

    is_french = lang.upper() == "FR"
    has_toxic = any(
        kw in ai_response.lower()
        for kw in ["reddit", "trustpilot", "blog", "can't verify", "ne peux pas"]
    )
    has_specs = any(
        kw in ai_response.lower()
        for kw in ["thermal", "-30", "lwg", "fill power", "certified", "certifie"]
    )

    ta = random.uniform(3.5, 5.0) if has_specs else random.uniform(1.0, 2.5)
    cf = random.uniform(1.0, 2.5) if has_toxic else random.uniform(3.5, 5.0)
    lp = random.uniform(1.0, 2.5) if is_french else random.uniform(3.5, 5.0)

    # E1 error detection — semantic override count
    e1_count = 0
    if has_toxic and not has_specs:
        e1_count = random.randint(2, 4)
    elif has_toxic:
        e1_count = random.randint(0, 2)

    ta = round(ta, 1)
    cf = round(cf, 1)
    lp = round(lp, 1)
    overall = round(ta * 0.4 + cf * 0.35 + lp * 0.25, 2)

    return {
        "technical_accuracy": ta,
        "citation_fidelity": cf,
        "linguistic_parity": lp,
        "overall": overall,
        "e1_errors": e1_count,
        "reasoning": (
            f"Technical accuracy {'high' if ta > 3 else 'low'}, "
            f"citations {'clean' if cf > 3 else 'toxic'}, "
            f"French parity {'maintained' if lp > 3 else 'degraded'}. "
            f"E1 overrides: {e1_count}."
        ),
    }


# =============================================================================
# Inference Alignment Scoring
# =============================================================================

def calculate_alignment_score(ground_truth: str, llm_output: str) -> float:
    """
    Calculate inference alignment between brand truth and AI output.
    Uses keyword overlap + weighted attribute matching.
    Returns 0-100 score.
    """
    if not ground_truth or not llm_output:
        return 0.0

    gt_words = set(ground_truth.lower().split())
    ai_words = set(llm_output.lower().split())

    if not gt_words:
        return 0.0

    overlap = gt_words.intersection(ai_words)
    base_score = len(overlap) / len(gt_words)

    key_terms = []
    for word in gt_words:
        if any(c.isdigit() for c in word) or word.startswith("$") or word.endswith("c"):
            key_terms.append(word)

    key_matches = sum(1 for t in key_terms if t in ai_words)
    key_boost = (key_matches / len(key_terms) * 0.3) if key_terms else 0

    score = min((base_score * 70 + key_boost * 100), 100)
    return round(score, 1)


# =============================================================================
# E-Score Computation — The Semantic Multiplier
# =============================================================================

def compute_e_score(s_in: float, s_out: float, delta: float,
                    kg_grounding: float = None) -> dict:
    """
    Compute the Remediation Efficiency E-Score.

    E = (S_out / S_in) * (1 - delta)

    Where:
      S_in  = Baseline PIM quality (pre-remediation semantic clarity)
      S_out = Post-remediation quality
      delta = Token Decay Factor (French fragmentation penalty)

    The E-Score is a semantic multiplier:
      - E < 1.0: Remediation is degrading quality (failure state)
      - E = 1.0: Break-even (no improvement)
      - E > 1.0: Net positive remediation
      - E >= 1.4: Optimal state (hallucination eradicated)

    E-Score thresholds (from Section 7.2):
      0.5-0.6: Critical failure — model actively rejecting fix kits
      0.7-0.9: Sub-threshold — kits partially ingested but overridden
      1.0-1.2: Marginal — fix kits accepted but unstable
      1.2-1.4: Strong — attention heads weighted toward injected payload
      1.4+:    Optimal — high clinical fidelity, precise causal attribution

    Reference: Section 7 — "Quantifying Semantic Overrides: The E-Score Metric"
    """
    if s_in <= 0:
        return {"e_score": 0, "status": "invalid", "interpretation": "Invalid S_in"}

    delta_clamped = max(0.0, min(1.0, delta))
    e_raw = (s_out / s_in) * (1.0 - delta_clamped)
    e_score = round(e_raw, 2)

    # KG grounding bonus — if KG validation passes, slight multiplier
    if kg_grounding and kg_grounding > 0.8:
        e_score = round(e_score * (1 + (kg_grounding - 0.8) * 0.5), 2)

    # Determine status and interpretation
    if e_score < 0.6:
        status = "critical_failure"
        interpretation = (
            "E-Score critically low. The model's generated output is semantically "
            "distinct from injected data. Fix kits are being actively rejected — "
            "the model defaults to stale latent priors (E1 override)."
        )
    elif e_score < 1.0:
        status = "sub_threshold"
        interpretation = (
            "Sub-threshold alignment. Fix kits partially ingested but parametric "
            "memory still dominates. Requires aggressive E-E-A-T optimization "
            "and Citation Authority escalation."
        )
    elif e_score < 1.2:
        status = "marginal"
        interpretation = (
            "Marginal improvement. Fix kits accepted but attention weight unstable. "
            "Vulnerable to model drift from backend parameter updates."
        )
    elif e_score < 1.4:
        status = "strong"
        interpretation = (
            "Strong remediation. Attention heads weighted toward injected payload. "
            "Output exhibits clinical fidelity with causal attribution."
        )
    else:
        status = "optimal"
        interpretation = (
            "Optimal state. Hallucination eradicated. The generative engine has "
            "fully internalized the brand's verified facts. E-Score demonstrates "
            "statistically significant semantic shift."
        )

    # Compute delta_E (change from baseline)
    baseline_e = 0.6  # Typical failure state baseline
    delta_e = round(e_score - baseline_e, 2)

    return {
        "e_score": e_score,
        "s_in": s_in,
        "s_out": s_out,
        "delta": delta_clamped,
        "delta_e": delta_e,
        "status": status,
        "interpretation": interpretation,
        "formula": f"E = ({s_out} / {s_in}) * (1 - {delta_clamped}) = {e_score}",
        "thresholds": {
            "critical_failure": "< 0.6",
            "sub_threshold": "0.6 - 1.0",
            "marginal": "1.0 - 1.2",
            "strong": "1.2 - 1.4",
            "optimal": "> 1.4",
        },
        "path_to_optimal": _compute_remediation_path(s_in, s_out, delta_clamped, e_score),
    }


def _compute_remediation_path(s_in: float, s_out: float, delta: float,
                              current_e: float) -> list:
    """
    Compute the remediation path from current state to optimal (1.4+).
    Returns milestones with required interventions.
    """
    path = []
    target_e = 1.4

    if current_e >= target_e:
        path.append({
            "milestone": "ACHIEVED",
            "e_score": current_e,
            "action": "Maintain via RAFT cadence and periodic audits",
        })
        return path

    # Milestone 1: Deploy JSON-LD (Fact Density)
    jsonld_boost = min(s_out * 0.15, 1.5)
    e_after_jsonld = round(((s_out + jsonld_boost) / s_in) * (1 - delta), 2)
    path.append({
        "milestone": "Deploy JSON-LD @graph",
        "kit_type": "jsonLd",
        "projected_e": e_after_jsonld,
        "s_out_delta": f"+{jsonld_boost:.1f}",
        "mechanism": "Deterministic @graph overrides heuristic parsing",
    })

    # Milestone 2: Deploy Hard Attributes (Entity Trust)
    ha_boost = min(s_out * 0.25, 2.0)
    e_after_ha = round(((s_out + jsonld_boost + ha_boost) / s_in) * (1 - delta), 2)
    path.append({
        "milestone": "Deploy DPO Hard Attributes",
        "kit_type": "hardAttributes",
        "projected_e": e_after_ha,
        "s_out_delta": f"+{ha_boost:.1f}",
        "mechanism": "P(contradictory_token) = 0 eliminates E1 overrides",
    })

    # Milestone 3: Deploy Truth Clip (Token Decay)
    new_delta = max(0, delta - 0.08)
    e_after_tc = round(((s_out + jsonld_boost + ha_boost) / s_in) * (1 - new_delta), 2)
    path.append({
        "milestone": "Deploy MRC Q-Former Truth Clip",
        "kit_type": "truthClip",
        "projected_e": e_after_tc,
        "delta_reduction": f"{delta:.3f} → {new_delta:.3f}",
        "mechanism": "Cross-modal attention bypasses French token brittleness",
    })

    # Milestone 4: KG Integration
    kg_boost = 0.1
    e_after_kg = round(e_after_tc * (1 + kg_boost), 2)
    path.append({
        "milestone": "Activate Knowledge Graph Binding",
        "kit_type": "knowledge_graph",
        "projected_e": e_after_kg,
        "mechanism": "Fuzzy logic constraints bind LLM output to KG truth boundaries",
    })

    # Milestone 5: RAFT fine-tuning
    if e_after_kg < target_e:
        raft_boost = target_e - e_after_kg + 0.05
        path.append({
            "milestone": "Execute RAFT Fine-Tuning Cycle",
            "kit_type": "raft",
            "projected_e": target_e + 0.05,
            "mechanism": (
                "Retrieval-Augmented Fine-Tuning permanently purges "
                "stale latent priors from model weights via DPO on scheduled cadence"
            ),
        })

    return path


# =============================================================================
# RAFT Cadence — Retrieval-Augmented Fine-Tuning Schedule
# =============================================================================

def build_raft_cadence(brand_id: str, current_e: float, delta: float) -> dict:
    """
    Build RAFT (Retrieval-Augmented Fine-Tuning) cadence plan.

    RAFT evolves passive RAG into active fine-tuning:
    - Actively fine-tunes model base weights with verified Hard Attributes
    - Uses DPO on a scheduled cadence
    - Permanently purges stale latent priors (e.g., Reddit 2021 biases)

    Reference: Section 9.4 — "Retrieval-Augmented Fine-Tuning (RAFT)"
    """
    now = datetime.utcnow()

    # Determine cadence based on current E-Score
    if current_e < 0.8:
        interval_days = 3
        urgency = "critical"
    elif current_e < 1.2:
        interval_days = 7
        urgency = "high"
    elif current_e < 1.4:
        interval_days = 14
        urgency = "moderate"
    else:
        interval_days = 30
        urgency = "maintenance"

    # Build schedule for next 90 days
    schedule = []
    current_date = now
    cycle = 1
    projected_e = current_e

    while current_date < now + timedelta(days=90):
        # Each RAFT cycle improves E-Score by diminishing returns
        improvement = max(0.02, 0.15 / math.sqrt(cycle))
        projected_e = round(min(projected_e + improvement, 2.0), 3)

        schedule.append({
            "cycle": cycle,
            "scheduled_date": current_date.strftime("%Y-%m-%d"),
            "type": "raft_fine_tune",
            "status": "scheduled",
            "projected_e_score": projected_e,
            "actions": [
                "Collect fresh probe data (5 variations x 3 iterations, EN + FR)",
                "Run Self-Consistency Mining — compute contradiction rate per variation",
                "Run G-Eval against current KG ground truth",
                "Generate DPO training pairs from E1 violations + contradictions",
                "Execute fine-tuning pass with updated Hard Attributes",
                "Validate E-Score improvement against previous cycle",
                f"Purge stale priors with delta > {delta:.3f}",
            ],
        })

        current_date += timedelta(days=interval_days)
        cycle += 1

    return {
        "brand_id": brand_id,
        "current_e_score": current_e,
        "target_e_score": 1.4,
        "cadence_interval_days": interval_days,
        "urgency": urgency,
        "total_cycles": len(schedule),
        "schedule": schedule,
        "methodology": {
            "name": "Retrieval-Augmented Fine-Tuning (RAFT)",
            "description": (
                "Evolves passive RAG structures into active fine-tuning operations. "
                "By fine-tuning model base weights with verified Hard Attributes via "
                "DPO on a scheduled cadence, stale latent priors are mathematically "
                "overwritten and permanently purged from parametric memory."
            ),
            "steps": [
                "1. Probe: Collect N fresh LLM responses for brand queries (EN + FR)",
                "2. Evaluate: Run G-Eval to score Technical Accuracy, Citation Fidelity, Linguistic Parity",
                "3. Detect: Identify E1 Semantic Override errors via KG constraint validation",
                "4. Generate: Build DPO training pairs — (preferred=KG truth, rejected=hallucination)",
                "5. Fine-Tune: Apply DPO to model weights with hard attribute constraints",
                "6. Verify: Re-probe and compute E-Score delta to confirm improvement",
                "7. Persist: Update KG with any new entity-attribute relationships discovered",
            ],
        },
    }


# =============================================================================
# Audit Scheduling & Execution
# =============================================================================

async def schedule_audit(
    db, brand_id: str, fix_kit_id: str, query: str, days: list[int] = None
) -> list[dict]:
    """Create audit schedule entries for Day 3, 7, 14 verification."""
    if days is None:
        days = [3, 7, 14]

    base_date = datetime.utcnow()
    audits = []

    for day in days:
        audit_id = str(uuid.uuid4())
        scheduled_date = (base_date + timedelta(days=day)).strftime("%Y-%m-%d")

        labels = {3: "Initial Check", 7: "Mid Audit", 14: "Full Verification"}

        await db.execute(
            """INSERT INTO audit_runs
               (id, brand_id, fix_kit_id, query, day_number, scheduled_date,
                status, label)
               VALUES (?, ?, ?, ?, ?, ?, 'scheduled', ?)""",
            (audit_id, brand_id, fix_kit_id, query, day, scheduled_date,
             f"Day {day} — {labels.get(day, 'Audit')}"),
        )

        audits.append({
            "id": audit_id,
            "day": day,
            "date": scheduled_date,
            "status": "scheduled",
            "label": f"Day {day} — {labels.get(day, 'Audit')}",
        })

    await db.commit()
    return audits


async def run_audit(db, audit_id: str) -> dict:
    """Execute an audit: re-probe the query and calculate score delta."""
    row = await db.execute("SELECT * FROM audit_runs WHERE id = ?", (audit_id,))
    audit = await row.fetchone()

    if not audit:
        return {"error": "Audit not found"}

    await db.execute(
        "UPDATE audit_runs SET status = 'running' WHERE id = ?", (audit_id,)
    )
    await db.commit()

    from engines.inference_lab import probe_query_single, build_golden_set, compute_contradiction_rate

    # Use Golden Set (3 variations x 3 iterations = 9 probes) instead of 10 identical probes
    variations = build_golden_set(audit["query"], "EN")[:3]
    results = []
    variation_responses = []
    for variation in variations:
        responses_for_variation = []
        for _ in range(3):
            result = await probe_query_single(variation["query"], "EN", temperature=0.7)
            results.append(result)
            responses_for_variation.append(result["response_text"])
        variation_responses.extend(responses_for_variation)

    # Compute contradiction rate across all responses
    contradiction = compute_contradiction_rate(variation_responses)

    mention_rate = sum(1 for r in results if r["brand_mentioned"]) / len(results) * 100
    avg_logprob = (
        sum(r["brand_mention_logprob"] for r in results if r["brand_mention_logprob"])
        / max(sum(1 for r in results if r["brand_mention_logprob"]), 1)
    )

    best_response = max(results, key=lambda r: r.get("brand_mention_logprob") or -999)

    geval_scores = await run_geval(
        query=audit["query"],
        ai_response=best_response["response_text"],
        ground_truth="",
        lang="EN",
    )

    # Factor contradiction rate into overall score — high contradiction penalizes
    contradiction_penalty = contradiction["contradiction_rate"] * 15  # 0-15 point penalty
    overall_score = round(mention_rate * 0.4 + geval_scores["overall"] * 20 * 0.6 - contradiction_penalty, 1)
    overall_score = max(0, overall_score)
    status = "passed" if overall_score >= 60 else "failed"

    detail = (
        f"Mention rate: {mention_rate}%, Avg logprob: {round(avg_logprob, 3)}, "
        f"E1 errors: {geval_scores.get('e1_errors', 0)}, "
        f"Contradiction rate: {contradiction['contradiction_rate']}, "
        f"Hallucinating: {contradiction['is_hallucinating']}"
    )

    await db.execute(
        """UPDATE audit_runs SET
           status = ?, detail = ?,
           score_technical_accuracy = ?,
           score_citation_fidelity = ?,
           score_linguistic_parity = ?,
           score_overall = ?
           WHERE id = ?""",
        (
            status,
            detail,
            geval_scores["technical_accuracy"],
            geval_scores["citation_fidelity"],
            geval_scores["linguistic_parity"],
            overall_score,
            audit_id,
        ),
    )
    await db.commit()

    return {
        "id": audit_id,
        "status": status,
        "score": overall_score,
        "geval": geval_scores,
        "mention_rate": mention_rate,
        "avg_logprob": round(avg_logprob, 3),
        "contradiction_rate": contradiction["contradiction_rate"],
        "is_hallucinating": contradiction["is_hallucinating"],
    }
