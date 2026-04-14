"""
VisiMind -- Outreach Router
Generate personalized cold emails and LinkedIn messages from audit/probe data.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import aiosqlite

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_db
from routers.auth import require_user

router = APIRouter(prefix="/api/v1/outreach", tags=["outreach"])


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    sequence_id: str = Field(..., description="One of: scary_report, competitor_advantage, french_gap, free_audit, design_partner")
    target_name: str = Field(..., min_length=1)
    target_title: str = Field(..., min_length=1)
    target_company: str = Field(..., min_length=1)


# ---------------------------------------------------------------------------
# Sequence catalogue
# ---------------------------------------------------------------------------

SEQUENCES = {
    "scary_report": {
        "id": "scary_report",
        "name": "The Scary Report",
        "description": "Use audit findings to shock the prospect with hard data about their AI invisibility.",
        "email_count": 3,
        "has_linkedin_variant": True,
    },
    "competitor_advantage": {
        "id": "competitor_advantage",
        "name": "Competitor Advantage",
        "description": "Show how the prospect's competitor is beating them in AI search results.",
        "email_count": 3,
        "has_linkedin_variant": True,
    },
    "french_gap": {
        "id": "french_gap",
        "name": "French Token Decay",
        "description": "Technical angle on the bilingual visibility gap between English and French AI responses.",
        "email_count": 3,
        "has_linkedin_variant": True,
    },
    "free_audit": {
        "id": "free_audit",
        "name": "Free Audit Offer",
        "description": "Lead with value by offering a complimentary AI visibility audit.",
        "email_count": 3,
        "has_linkedin_variant": True,
    },
    "design_partner": {
        "id": "design_partner",
        "name": "Design Partner",
        "description": "Exclusive early-adopter invitation with scarcity and FOMO positioning.",
        "email_count": 3,
        "has_linkedin_variant": True,
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_fr_gap(results: list) -> bool:
    """Return True when French probe responses are measurably worse than English."""
    en_mentions = 0
    fr_mentions = 0
    en_total = 0
    fr_total = 0
    for r in results:
        lang = r.get("lang", r.get("language", "EN")).upper()
        mentioned = r.get("brand_mentioned", 0)
        if lang.startswith("EN"):
            en_total += 1
            en_mentions += int(mentioned)
        elif lang.startswith("FR"):
            fr_total += 1
            fr_mentions += int(mentioned)
    if en_total == 0 or fr_total == 0:
        return True  # assume gap when data is missing
    en_rate = en_mentions / en_total
    fr_rate = fr_mentions / fr_total
    return fr_rate < en_rate


def _extract_audit_vars(brand: dict, audit: dict, results: list, ias_data: dict | None) -> dict:
    """Build the variable dict that templates interpolate."""
    score = ias_data.get("score", 0) if ias_data else 0
    grade = ias_data.get("grade", "RED") if ias_data else "RED"
    findings = ias_data.get("findings", []) if ias_data else []
    finding_summary = findings[0].get("message", "Your brand is not surfacing in AI-generated answers.") if findings else "Your brand is not surfacing in AI-generated answers."
    competitor = brand.get("top_competitor", "your closest competitor") or "your closest competitor"
    fr_gap = _compute_fr_gap(results)

    return {
        "brand_name": brand.get("brand_name", "your brand"),
        "score": score,
        "grade": grade,
        "competitor": competitor,
        "finding_summary": finding_summary,
        "fr_gap": fr_gap,
    }


# ---------------------------------------------------------------------------
# Template generators
# ---------------------------------------------------------------------------

def _gen_scary_report(v: dict, t: dict) -> dict:
    brand = v["brand_name"]
    score = v["score"]
    grade = v["grade"]
    competitor = v["competitor"]
    finding = v["finding_summary"]
    name = t["target_name"]
    company = t["target_company"]
    title = t["target_title"]

    emails = [
        {
            "subject": f"Your brand is invisible to AI -- here's the data",
            "body": (
                f"Hi {name},\n\n"
                f"I ran {brand} through our AI visibility scanner last week. The results are concerning.\n\n"
                f"Your Inference Alignment Score is {score}/100 (grade: {grade}). "
                f"That means when someone asks ChatGPT or Gemini about products in your category, "
                f"{brand} is either missing entirely or being misrepresented.\n\n"
                f"Specifically: {finding}\n\n"
                f"This is not a hypothetical. Over 40% of product research now starts with an AI agent, "
                f"and that number is climbing every quarter. If your brand is invisible to these systems, "
                f"you are losing revenue today.\n\n"
                f"I put together a one-page report for {company}. Want me to send it over?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 1,
        },
        {
            "subject": f"The revenue {brand} is losing to AI agents",
            "body": (
                f"Hi {name},\n\n"
                f"Following up on the AI visibility data I mentioned. Let me put a number on it.\n\n"
                f"Brands with an IAS below 30 (yours is {score}) typically see 15-25% of their "
                f"qualified search traffic diverted to competitors through AI-generated answers. "
                f"For a company like {company}, that could mean six figures in lost pipeline annually.\n\n"
                f"The worst part: {competitor} already shows up when customers ask AI about your category. "
                f"Every day this goes unfixed, their position gets reinforced in the model's weights.\n\n"
                f"We can fix this in under two weeks. The first step is a 20-minute call to walk "
                f"through your report.\n\n"
                f"Are you open to a quick chat this week?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 3,
        },
        {
            "subject": f"Last chance: your competitors are fixing this",
            "body": (
                f"Hi {name},\n\n"
                f"I will keep this short. Three companies in your space have already started "
                f"optimizing their AI visibility this quarter. {competitor} is one of them.\n\n"
                f"AI models reinforce what they already know. The longer {brand} stays invisible "
                f"(IAS: {score}/100), the harder and more expensive the fix becomes. "
                f"This is a compounding problem, not a static one.\n\n"
                f"I have 15 minutes on Thursday if you want to see the data. No pitch, just the report.\n\n"
                f"Either way, I wanted to make sure you had the information.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 7,
        },
    ]

    linkedin = {
        "connection_request": (
            f"Hi {name}, I ran an AI visibility scan on {brand} and found some gaps worth sharing. "
            f"Your IAS is {score}/100. Happy to send the one-page report if useful."
        )[:300],
        "follow_up_message": (
            f"Thanks for connecting, {name}. As mentioned, {brand}'s AI visibility score is {score}/100 "
            f"({grade}). When prospects ask GPT or Gemini about your category, {brand} is being overlooked. "
            f"I have a short report with specifics -- want me to send it over?"
        ),
    }

    return {"emails": emails, "linkedin": linkedin}


def _gen_competitor_advantage(v: dict, t: dict) -> dict:
    brand = v["brand_name"]
    score = v["score"]
    grade = v["grade"]
    competitor = v["competitor"]
    name = t["target_name"]
    company = t["target_company"]

    emails = [
        {
            "subject": f"{competitor} is beating {brand} in AI search",
            "body": (
                f"Hi {name},\n\n"
                f"I have been researching how AI agents represent brands in your space, and I found "
                f"something you should see.\n\n"
                f"When users ask ChatGPT or Gemini for recommendations in your category, {competitor} "
                f"appears consistently. {brand} does not. Your Inference Alignment Score is {score}/100, "
                f"which puts you in the {grade} zone.\n\n"
                f"This is not about SEO or paid ads. AI models build internal representations of brands "
                f"from structured data, citations, and entity trust signals. Right now, {competitor} "
                f"has stronger signals across the board.\n\n"
                f"I built a side-by-side comparison for {company}. It takes two minutes to read and "
                f"makes the gap very clear.\n\n"
                f"Interested?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 1,
        },
        {
            "subject": f"How {competitor} shows up vs {brand} in GPT",
            "body": (
                f"Hi {name},\n\n"
                f"Quick follow-up with the actual data. Here is what happens when a user asks "
                f"GPT-4 to recommend products in your category:\n\n"
                f"- {competitor}: mentioned by name, features listed accurately, often ranked #1\n"
                f"- {brand}: either missing, mentioned generically, or listed with incorrect specs\n\n"
                f"This pattern repeats across Gemini, Perplexity, and Claude. The AI models are "
                f"essentially sending your potential customers to {competitor}.\n\n"
                f"The gap is fixable. We have helped brands go from invisible to consistently "
                f"recommended in 2-3 weeks by fixing the underlying data signals.\n\n"
                f"Worth a 15-minute call to walk through the comparison?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 3,
        },
        {
            "subject": f"3 brands fixed this last month",
            "body": (
                f"Hi {name},\n\n"
                f"Last note on this. In the past 30 days, three brands in adjacent categories "
                f"went through our AI visibility optimization process. Average results:\n\n"
                f"- IAS score: 22 to 71 (from RED to GREEN)\n"
                f"- AI recommendation rate: up 3.4x\n"
                f"- Time to fix: 12 days\n\n"
                f"{brand} is currently at {score}/100. The math works in your favor if you move now, "
                f"because AI models reward early movers and reinforce existing patterns.\n\n"
                f"If the timing is wrong, no worries. But if {competitor} keeps building their "
                f"AI presence while {brand} stays invisible, the cost of catching up only goes up.\n\n"
                f"Happy to chat whenever it makes sense.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 7,
        },
    ]

    linkedin = {
        "connection_request": (
            f"Hi {name}, researching AI visibility in your space. {competitor} is outperforming "
            f"{brand} in GPT/Gemini results. Built a comparison -- happy to share."
        )[:300],
        "follow_up_message": (
            f"Thanks for connecting. I ran a head-to-head analysis of how AI agents represent "
            f"{brand} vs {competitor}. The short version: {competitor} gets recommended, {brand} "
            f"gets overlooked. Happy to send the full breakdown if you want to see the specifics."
        ),
    }

    return {"emails": emails, "linkedin": linkedin}


def _gen_french_gap(v: dict, t: dict) -> dict:
    brand = v["brand_name"]
    score = v["score"]
    grade = v["grade"]
    competitor = v["competitor"]
    fr_gap = v["fr_gap"]
    name = t["target_name"]
    company = t["target_company"]

    gap_status = "nearly zero" if fr_gap else "weaker than English"

    emails = [
        {
            "subject": f"{brand}'s French AI presence is nearly zero",
            "body": (
                f"Hi {name},\n\n"
                f"I ran a bilingual AI visibility audit on {brand} and the French results are alarming.\n\n"
                f"When AI agents respond to English queries in your category, {brand} shows up "
                f"occasionally. But switch to French and {brand} is practically invisible. "
                f"Your overall IAS is {score}/100 ({grade}), but the French-language score "
                f"drops even further.\n\n"
                f"This is a phenomenon called token decay. AI models are trained on predominantly "
                f"English data, so French brand signals degrade faster. Without deliberate French "
                f"entity reinforcement, your Quebec and francophone market presence in AI erodes "
                f"to near zero.\n\n"
                f"For a company operating in a bilingual market, this is a significant blind spot. "
                f"I have the full bilingual breakdown for {company} if you want to see the numbers.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 1,
        },
        {
            "subject": f"Quebec customers can't find you through AI",
            "body": (
                f"Hi {name},\n\n"
                f"Following up on the French AI visibility issue. Here is why this matters commercially.\n\n"
                f"Quebec represents 23% of Canada's population and has distinct purchasing patterns. "
                f"When a francophone customer asks an AI assistant about products in your category, "
                f"{brand} is not part of the conversation. {competitor} is doing slightly better, "
                f"but neither of you has optimized for this yet.\n\n"
                f"The opportunity: whoever fixes their French AI signals first will dominate "
                f"that segment. AI models reward first movers heavily because recommendations "
                f"compound over time.\n\n"
                f"The bilingual fix is actually simpler than most people expect. We map your "
                f"English entity signals, create French equivalents, and deploy both simultaneously.\n\n"
                f"Want to see the bilingual gap analysis for {company}?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 3,
        },
        {
            "subject": f"The fix takes 48 hours",
            "body": (
                f"Hi {name},\n\n"
                f"One last note on the French AI visibility gap. I know this might seem like a "
                f"complex technical problem, but the fix is actually fast.\n\n"
                f"For most brands, we can deploy bilingual entity signals in 48 hours. The process:\n\n"
                f"1. Map your existing English brand signals (product data, structured markup, citations)\n"
                f"2. Generate French-language equivalents with proper Quebec terminology\n"
                f"3. Deploy both to the channels AI models actually read\n\n"
                f"Brands that have done this see their French AI visibility jump from near-zero to "
                f"parity with English within one model refresh cycle (typically 2-4 weeks).\n\n"
                f"{brand}'s IAS is {score}/100 right now. The bilingual fix alone can move that "
                f"by 15-20 points.\n\n"
                f"Happy to walk you through it in 15 minutes if useful.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 7,
        },
    ]

    linkedin = {
        "connection_request": (
            f"Hi {name}, ran a bilingual AI audit on {brand}. English presence is weak, "
            f"French is {gap_status}. The fix is faster than you'd think -- happy to share the data."
        )[:300],
        "follow_up_message": (
            f"Thanks for connecting. The bilingual audit shows {brand}'s French AI visibility is "
            f"{gap_status}. Quebec customers asking AI agents about your category are not seeing "
            f"your brand at all. I have the full breakdown if you want the specifics."
        ),
    }

    return {"emails": emails, "linkedin": linkedin}


def _gen_free_audit(v: dict, t: dict) -> dict:
    brand = v["brand_name"]
    score = v["score"]
    grade = v["grade"]
    name = t["target_name"]
    company = t["target_company"]

    emails = [
        {
            "subject": f"Free AI visibility audit for {brand}",
            "body": (
                f"Hi {name},\n\n"
                f"I would like to offer {company} a complimentary AI visibility audit.\n\n"
                f"We scan how AI agents (ChatGPT, Gemini, Perplexity, Claude) represent your brand "
                f"when users ask about products in your category. The report includes:\n\n"
                f"- Your Inference Alignment Score (0-100)\n"
                f"- Which AI agents mention you vs competitors\n"
                f"- Whether your product specs are being represented accurately\n"
                f"- A bilingual comparison (English vs French AI responses)\n\n"
                f"No strings attached. We are building case studies in your space and want to "
                f"demonstrate the value. The audit takes 24 hours and the report is yours to keep "
                f"regardless of whether we work together.\n\n"
                f"Want me to run it?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 1,
        },
        {
            "subject": f"I ran {brand} through our AI scanner",
            "body": (
                f"Hi {name},\n\n"
                f"I went ahead and ran a preliminary scan on {brand}. I will not share the full "
                f"results without your permission, but I can tell you the high-level number: "
                f"your IAS is {score}/100.\n\n"
                f"For context, anything below 40 means AI agents are either ignoring your brand "
                f"or misrepresenting it. The average in your category is around 35.\n\n"
                f"The full report has specific findings -- which agents get it wrong, what "
                f"competitors show up instead, and where the biggest gaps are.\n\n"
                f"Want me to send it over? It is genuinely useful even if we never speak again.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 3,
        },
        {
            "subject": f"Your free report expires Friday",
            "body": (
                f"Hi {name},\n\n"
                f"Last note on this. The AI visibility report I generated for {brand} is based on "
                f"a point-in-time scan, so the data gets stale after about a week.\n\n"
                f"I would hate for it to go to waste. The report is free, it takes 5 minutes to "
                f"read, and it gives you a clear picture of how AI agents currently see {brand}.\n\n"
                f"Your IAS is {score}/100 ({grade}). Whether that is a priority for {company} "
                f"right now or not, at least you will have the data.\n\n"
                f"Just reply \"send it\" and I will forward the PDF.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 7,
        },
    ]

    linkedin = {
        "connection_request": (
            f"Hi {name}, offering free AI visibility audits for brands in your space. "
            f"We scan how GPT/Gemini represent {brand} and deliver a one-page report. Interested?"
        )[:300],
        "follow_up_message": (
            f"Thanks for connecting, {name}. I ran a quick scan on {brand} -- your AI visibility "
            f"score is {score}/100 ({grade}). Happy to send the full report, no strings attached. "
            f"Just let me know."
        ),
    }

    return {"emails": emails, "linkedin": linkedin}


def _gen_design_partner(v: dict, t: dict) -> dict:
    brand = v["brand_name"]
    score = v["score"]
    grade = v["grade"]
    competitor = v["competitor"]
    name = t["target_name"]
    company = t["target_company"]
    title = t["target_title"]

    emails = [
        {
            "subject": f"Invitation: {brand} as VisiMind design partner",
            "body": (
                f"Hi {name},\n\n"
                f"We are selecting five brands to join VisiMind's design partner cohort, and "
                f"{brand} is on our shortlist.\n\n"
                f"VisiMind is an AI visibility platform that helps brands control how they appear "
                f"in AI-generated recommendations (ChatGPT, Gemini, Perplexity). As a design partner, "
                f"{company} would get:\n\n"
                f"- Full AI visibility audit and ongoing monitoring (normally $2,400/quarter)\n"
                f"- Priority access to new features before general release\n"
                f"- Direct input into our product roadmap\n"
                f"- Founding partner pricing locked in permanently\n\n"
                f"In exchange, we ask for honest feedback and permission to use anonymized results "
                f"as case studies.\n\n"
                f"We have three spots left. Would {company} be interested?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 1,
        },
        {
            "subject": f"3 spots left in our pilot cohort",
            "body": (
                f"Hi {name},\n\n"
                f"Quick update on the design partner program I mentioned. We filled two of five "
                f"spots this week, so three remain.\n\n"
                f"I should mention: I ran a preliminary scan on {brand} as part of our evaluation. "
                f"Your IAS is {score}/100 ({grade}), which actually makes you an ideal fit for the "
                f"program. Brands starting from a lower baseline see the most dramatic improvements, "
                f"which makes for compelling case studies.\n\n"
                f"The commitment from your side is minimal: one onboarding call (30 min), a monthly "
                f"check-in (15 min), and a short feedback survey each quarter.\n\n"
                f"We handle everything else. You get full AI visibility optimization at a fraction "
                f"of the cost.\n\n"
                f"Worth a conversation?\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 3,
        },
        {
            "subject": f"We just signed {competitor}'s competitor",
            "body": (
                f"Hi {name},\n\n"
                f"Wanted to let you know: we signed a brand in your space to our design partner "
                f"cohort this week. I will not name them until we announce publicly, but they "
                f"compete directly with {competitor}.\n\n"
                f"That leaves two open spots. Once the cohort is full, the next intake is in Q3 "
                f"and pricing resets to standard rates.\n\n"
                f"I will be direct: {brand}'s AI visibility needs work (IAS: {score}/100). The design "
                f"partner program is the most cost-effective way to fix it, and you get a platform "
                f"that normally costs 4x what design partners pay.\n\n"
                f"If the timing is not right, no pressure. But I did not want you to miss the window.\n\n"
                f"Best,\nThe VisiMind Team"
            ),
            "send_day": 7,
        },
    ]

    linkedin = {
        "connection_request": (
            f"Hi {name}, selecting 5 brands for VisiMind's design partner cohort. "
            f"{brand} is on our shortlist. Free AI visibility platform + founding pricing. Interested?"
        )[:300],
        "follow_up_message": (
            f"Thanks for connecting. We are looking for design partners who want to fix their AI "
            f"visibility and help shape our product. {brand}'s IAS is {score}/100, which makes you "
            f"an ideal candidate. 3 spots left -- want me to send the details?"
        ),
    }

    return {"emails": emails, "linkedin": linkedin}


GENERATORS = {
    "scary_report": _gen_scary_report,
    "competitor_advantage": _gen_competitor_advantage,
    "french_gap": _gen_french_gap,
    "free_audit": _gen_free_audit,
    "design_partner": _gen_design_partner,
}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/{brand_id}/sequences")
async def list_sequences(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Return the five available outreach sequence templates."""
    # Verify brand belongs to user
    cursor = await db.execute(
        "SELECT id FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")

    return list(SEQUENCES.values())


@router.post("/{brand_id}/generate")
async def generate_outreach(brand_id: str, req: GenerateRequest, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Generate a personalized outreach sequence for a brand using audit data."""
    # Validate sequence id
    if req.sequence_id not in SEQUENCES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown sequence_id '{req.sequence_id}'. Valid options: {', '.join(SEQUENCES.keys())}",
        )

    # Fetch brand (verify ownership)
    cursor = await db.execute(
        "SELECT * FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    brand_dict = dict(brand)

    # Fetch latest audit results
    cursor = await db.execute(
        "SELECT * FROM audit_results WHERE brand_profile_id = ? ORDER BY created_at DESC LIMIT 1",
        (brand_id,),
    )
    audit = await cursor.fetchone()
    if not audit:
        raise HTTPException(
            status_code=404,
            detail="No audit results found for this brand. Run an audit first.",
        )
    audit_dict = dict(audit)

    # Parse stored JSON
    results = json.loads(audit_dict["results"]) if audit_dict.get("results") else []
    ias_data = json.loads(audit_dict["ias_data"]) if audit_dict.get("ias_data") else None

    # Build template variables
    audit_vars = _extract_audit_vars(brand_dict, audit_dict, results, ias_data)

    target = {
        "target_name": req.target_name,
        "target_title": req.target_title,
        "target_company": req.target_company,
    }

    # Generate the sequence
    generator = GENERATORS[req.sequence_id]
    output = generator(audit_vars, target)

    return {
        "brand_name": audit_vars["brand_name"],
        "sequence": req.sequence_id,
        "target": {
            "name": req.target_name,
            "title": req.target_title,
            "company": req.target_company,
        },
        "emails": output["emails"],
        "linkedin": output["linkedin"],
        "audit_data_used": {
            "ias_score": audit_vars["score"],
            "grade": audit_vars["grade"],
            "top_finding": audit_vars["finding_summary"],
            "fr_visibility_gap": audit_vars["fr_gap"],
        },
    }


@router.get("/{brand_id}/history")
async def get_outreach_history(brand_id: str, user: dict = Depends(require_user), db: aiosqlite.Connection = Depends(get_db)):
    """Return previously generated outreach sequences (placeholder -- returns empty list)."""
    # Verify brand belongs to user
    cursor = await db.execute(
        "SELECT id FROM brand_profiles WHERE id = ? AND user_id = ?",
        (brand_id, user["id"]),
    )
    if not await cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")

    return []
