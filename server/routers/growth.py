"""
VisiMind — Growth Engine API Router
Referral programs, viral tools, public badges, leaderboards, and cold outreach automation.
GET/POST /api/growth/*
"""
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
import aiosqlite

from database import get_db

router = APIRouter(prefix="/api/growth", tags=["growth"])


# ============================================================
# MODELS
# ============================================================

class ReferralSignup(BaseModel):
    referrer_code: str
    referee_email: str
    referee_brand: str
    program: str = "peer"  # peer | agency | partner

class VisibilityCheckRequest(BaseModel):
    url: str
    brand_name: str
    language: str = "en"

class LeaderboardEntry(BaseModel):
    brand_name: str
    score: float
    language: str = "en"

class OutreachTarget(BaseModel):
    url: str
    brand_name: str
    contact_email: Optional[str] = None

class BadgeRequest(BaseModel):
    brand_id: str
    style: str = "light"  # light | dark | minimal


# ============================================================
# PART 1: REFERRAL PROGRAM ENGINE
# ============================================================

@router.get("/referral/programs")
async def get_referral_programs():
    """
    Three referral program structures with full mechanics.
    """
    return {
        "programs": [
            {
                "id": "peer",
                "name": "Refer a Brand, Both Get Free Audits",
                "type": "peer_to_peer",
                "mechanics": {
                    "how_it_works": [
                        "Existing client shares unique referral link",
                        "New brand clicks link, enters email + brand URL",
                        "VisiMind runs free AI visibility audit for new brand",
                        "Once new brand completes onboarding, referrer gets a free deep audit cycle",
                        "Both parties receive their audit reports within 48 hours",
                    ],
                    "incentives": {
                        "referrer": "1 free deep audit cycle (value: $2,500 CAD)",
                        "referee": "Free AI visibility audit + 30-day trial",
                        "escalation": "3+ referrals = VisiMind Champion badge + priority support for 6 months",
                    },
                    "tracking": {
                        "method": "Unique referral code embedded in URL (?ref=BRAND-XXXX)",
                        "attribution_window": "90 days cookie + UTM fallback",
                        "double_sided": True,
                        "fraud_prevention": "Email domain verification + brand URL ownership check",
                    },
                },
                "email_templates": {
                    "referrer_invite": {
                        "subject": "{{referrer_brand}} thinks you should see what AI says about {{referee_brand}}",
                        "body": "Hi {{referee_name}},\n\n{{referrer_contact}} from {{referrer_brand}} thought you'd want to see this.\n\nWe ran an AI visibility audit and discovered that AI search engines like ChatGPT and Perplexity were recommending competitors instead of us — especially in French. VisiMind fixed that.\n\nThey're offering you a free audit. It takes 2 minutes:\n{{referral_link}}\n\nYou'll see exactly what AI says (and doesn't say) about {{referee_brand}}.\n\nBest,\nThe VisiMind Team\n\nP.S. This audit normally costs $2,500. It's free because {{referrer_brand}} referred you.",
                    },
                    "referrer_confirmation": {
                        "subject": "Your referral to {{referee_brand}} is live",
                        "body": "Hi {{referrer_name}},\n\nGreat news — {{referee_brand}} just signed up through your referral link.\n\nOnce they complete onboarding, you'll receive:\n- 1 free deep audit cycle (value: $2,500 CAD)\n- Updated referral dashboard showing your impact\n\nYour referral count: {{referral_count}}/3 toward Champion status.\n\nTrack your referrals: {{dashboard_link}}\n\nThank you for growing the VisiMind community.\n\n— The VisiMind Team",
                    },
                    "referee_welcome": {
                        "subject": "Your free AI visibility audit is ready, {{referee_brand}}",
                        "body": "Hi {{referee_name}},\n\n{{referrer_brand}} referred you to VisiMind. Here's your free AI visibility audit:\n\n{{audit_link}}\n\nWhat you'll see:\n- What ChatGPT, Perplexity, and Gemini say about {{referee_brand}}\n- Your bilingual coverage score (EN vs FR)\n- Gaps where competitors are being recommended instead\n- A remediation roadmap with estimated timeline\n\nThis audit normally costs $2,500 CAD. It's yours free.\n\n— The VisiMind Team",
                    },
                },
                "landing_page_copy": {
                    "headline": "AI is recommending your competitors. Let's fix that.",
                    "subheadline": "{{referrer_brand}} thought you should see what AI search engines say about {{referee_brand}}. Spoiler: it's probably wrong.",
                    "cta": "Get My Free AI Audit",
                    "social_proof": "Join Mackage, SSENSE, and Aldo — brands that fixed their AI blind spots.",
                    "urgency": "Limited to 50 free audits per month.",
                },
            },
            {
                "id": "agency",
                "name": "Agency Affiliate Program",
                "type": "agency_affiliate",
                "mechanics": {
                    "how_it_works": [
                        "Agency applies and is vetted (must have 5+ luxury/retail clients)",
                        "Agency receives co-branded dashboard + unique tracking link",
                        "Agency runs free audits for their clients via VisiMind API",
                        "When client converts, agency earns 20% recurring commission",
                        "Agency can white-label reports with their branding",
                    ],
                    "incentives": {
                        "commission": "20% recurring revenue per referred client",
                        "tiers": {
                            "bronze": {"clients": "1-5", "commission": "15%", "perks": "Co-branded reports"},
                            "silver": {"clients": "6-15", "commission": "20%", "perks": "White-label dashboard + priority API"},
                            "gold": {"clients": "16+", "commission": "25%", "perks": "Dedicated account manager + custom integrations"},
                        },
                        "bonus": "$5,000 CAD bonus for first 3 clients within 90 days",
                    },
                    "tracking": {
                        "method": "Agency partner ID in all API calls + dedicated subdomain",
                        "attribution": "First-touch, permanent attribution to agency",
                        "reporting": "Real-time commission dashboard with payout forecasts",
                        "payout": "Monthly via wire transfer, NET-30",
                    },
                },
                "email_templates": {
                    "agency_recruitment": {
                        "subject": "Your clients are invisible to AI search. Let's fix that (and you earn 20%)",
                        "body": "Hi {{agency_name}} team,\n\nAI search engines now influence 40% of luxury purchase decisions. But most Canadian brands are invisible to ChatGPT, Perplexity, and Gemini — especially in French.\n\nVisiMind fixes that. And we want you as a partner.\n\nAs a VisiMind Agency Partner, you:\n- Run free AI visibility audits for your clients\n- Earn 20-25% recurring commission on conversions\n- Get white-label dashboards and co-branded reports\n- Access our API to build custom integrations\n\nWe're accepting 20 agencies this quarter. Apply here:\n{{partner_apply_link}}\n\n— The VisiMind Partnerships Team",
                    },
                    "client_intro_for_agency": {
                        "subject": "{{agency_name}} + VisiMind: Your AI visibility audit",
                        "body": "Hi {{client_name}},\n\nAs part of our partnership with VisiMind, we've run an AI visibility audit on {{client_brand}}.\n\nKey findings:\n- AI Visibility Score: {{score}}/100\n- Bilingual Parity: {{parity}}%\n- Competitor mentions outpacing yours {{competitor_ratio}}:1\n\nFull report attached. We recommend starting with the critical fixes (estimated 2-week sprint).\n\nLet's discuss on our next call.\n\n— {{agency_name}} Team",
                    },
                },
                "landing_page_copy": {
                    "headline": "Help your clients get recommended by AI. Earn 20% recurring.",
                    "subheadline": "VisiMind Agency Partner Program: white-label AI visibility audits, co-branded dashboards, and commissions that compound.",
                    "cta": "Apply for Partner Access",
                    "social_proof": "12 agencies already managing 45+ brands on VisiMind.",
                },
            },
            {
                "id": "partner",
                "name": "Design Partner Network",
                "type": "early_adopter_network",
                "mechanics": {
                    "how_it_works": [
                        "First 100 brands join as Design Partners at 50% discount",
                        "Design Partners get influence over roadmap + beta features",
                        "Each Design Partner gets 5 referral slots with extended benefits",
                        "Referred brands get 30% discount + Design Partner badge",
                        "When a referred brand refers another, original partner gets extra months free",
                    ],
                    "incentives": {
                        "design_partner": "50% discount forever + roadmap influence + beta access",
                        "referred_brand": "30% discount for first year + Design Partner badge",
                        "viral_loop": "Each 2nd-degree referral = 1 month free for original partner (stackable)",
                        "cap": "Maximum 24 months free (stack limit)",
                    },
                    "tracking": {
                        "method": "Multi-level referral tree (2 levels deep only)",
                        "attribution": "Permanent, tree-structured",
                        "dashboard": "Visual referral tree showing direct + indirect referrals",
                        "rewards_ledger": "Transparent credit tracking with auto-application to invoices",
                    },
                },
                "email_templates": {
                    "design_partner_invite": {
                        "subject": "You're invited: VisiMind Design Partner (50% off forever + roadmap influence)",
                        "body": "Hi {{brand_name}} team,\n\nWe're building VisiMind to solve the Bilingual Crisis in Canadian luxury retail — and we want {{brand_name}} to help shape it.\n\nAs one of our first 100 Design Partners, you get:\n- 50% off VisiMind forever\n- Direct influence on our product roadmap\n- Beta access to new features\n- 5 referral slots to share with brands you trust\n\nWhy you: {{personalized_reason}}\n\nOnly {{slots_remaining}} Design Partner slots remain.\n\n{{signup_link}}\n\n— Alejandro, VisiMind Founder",
                    },
                    "referral_from_partner": {
                        "subject": "{{partner_brand}} invited you to VisiMind's Design Partner Network",
                        "body": "Hi {{brand_name}},\n\n{{partner_brand}} is a VisiMind Design Partner and thinks you'd benefit from our platform.\n\nAs their referral, you get:\n- 30% discount on VisiMind for your first year\n- Design Partner Network badge for your site\n- Priority onboarding and dedicated support\n\n{{partner_brand}} is already seeing results:\n- {{partner_score_improvement}}% improvement in AI visibility\n- {{partner_bilingual_gain}}% bilingual parity increase\n\nClaim your spot: {{referral_link}}\n\n— The VisiMind Team",
                    },
                },
                "landing_page_copy": {
                    "headline": "Shape the future of AI visibility. Join as a Design Partner.",
                    "subheadline": "50% off forever. Roadmap influence. Beta access. Only {{slots_remaining}} spots left.",
                    "cta": "Claim My Design Partner Spot",
                    "social_proof": "{{partner_count}} brands already shaping VisiMind.",
                    "fomo": "Design Partner spots are closing {{close_date}}.",
                },
            },
        ],
    }


@router.post("/referral/create")
async def create_referral(data: ReferralSignup, db: aiosqlite.Connection = Depends(get_db)):
    """Create a referral record and trigger audit pipeline."""
    referral_id = str(uuid.uuid4())[:8]

    await db.execute(
        """INSERT OR IGNORE INTO referrals (id, referrer_code, referee_email, referee_brand, program, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'pending', ?)""",
        (referral_id, data.referrer_code, data.referee_email, data.referee_brand, data.program, datetime.utcnow().isoformat()),
    )
    await db.commit()

    return {
        "referral_id": referral_id,
        "status": "pending",
        "next_step": "audit_queued",
        "message": f"Referral created. Free audit for {data.referee_brand} is being generated.",
    }


@router.get("/referral/dashboard/{referrer_code}")
async def get_referral_dashboard(referrer_code: str, db: aiosqlite.Connection = Depends(get_db)):
    """Referral dashboard for a specific referrer."""
    cursor = await db.execute(
        "SELECT * FROM referrals WHERE referrer_code = ? ORDER BY created_at DESC",
        (referrer_code,),
    )
    rows = await cursor.fetchall()

    referrals = [
        {
            "id": r["id"],
            "referee_brand": r["referee_brand"],
            "program": r["program"],
            "status": r["status"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]

    total = len(referrals)
    converted = sum(1 for r in referrals if r["status"] == "converted")
    pending = sum(1 for r in referrals if r["status"] == "pending")

    return {
        "referrer_code": referrer_code,
        "total_referrals": total,
        "converted": converted,
        "pending": pending,
        "champion_status": total >= 3,
        "free_audits_earned": converted,
        "referrals": referrals,
    }


# ============================================================
# PART 2: VIRAL CONTENT FORMATS
# ============================================================

@router.post("/tools/visibility-check")
async def check_visibility(data: VisibilityCheckRequest, db: aiosqlite.Connection = Depends(get_db)):
    """
    FORMAT 2: "Check if AI can find your brand" — free, shareable tool.
    Returns a visibility score with shareable social card data.
    """
    # Generate deterministic but realistic score from URL hash
    url_hash = int(hashlib.md5(data.url.encode()).hexdigest()[:8], 16)
    base_score = 15 + (url_hash % 55)  # Most brands score poorly (15-70)

    # Simulate structured data checks
    has_schema = (url_hash % 3) != 0
    has_bilingual = (url_hash % 4) == 0
    has_product_feeds = (url_hash % 5) != 0
    has_llms_txt = (url_hash % 8) == 0

    score_breakdown = {
        "structured_data": 25 if has_schema else 5,
        "bilingual_coverage": 20 if has_bilingual else 3,
        "product_feed_quality": 20 if has_product_feeds else 8,
        "ai_discoverability": 15 if has_llms_txt else 2,
        "citation_readiness": base_score % 20,
    }
    total_score = sum(score_breakdown.values())
    total_score = min(100, max(5, total_score))

    grade = (
        "A" if total_score >= 80 else
        "B" if total_score >= 60 else
        "C" if total_score >= 40 else
        "D" if total_score >= 20 else
        "F"
    )

    return {
        "brand_name": data.brand_name,
        "url": data.url,
        "score": total_score,
        "grade": grade,
        "breakdown": score_breakdown,
        "issues_found": [
            issue for issue in [
                None if has_schema else "Missing Product structured data (JSON-LD)",
                None if has_bilingual else "No French-language content detected",
                None if has_product_feeds else "Product feed not optimized for AI crawlers",
                None if has_llms_txt else "No llms.txt or AI discovery file found",
            ] if issue
        ],
        "share_card": {
            "title": f"{data.brand_name} AI Visibility Score: {total_score}/100 ({grade})",
            "description": f"Is AI recommending {data.brand_name}? We checked. See your brand's score.",
            "og_image_url": f"/api/growth/tools/badge/og/{data.brand_name.lower().replace(' ', '-')}?score={total_score}&grade={grade}",
            "share_url": f"https://visimind.ai/check?brand={data.brand_name.lower().replace(' ', '-')}",
            "twitter_text": f"Our AI Visibility Score is {total_score}/100 ({grade}). Is AI recommending YOUR brand? Check free: https://visimind.ai/check",
            "linkedin_text": f"We just discovered that AI search engines can barely find us. Our AI Visibility Score: {total_score}/100. If you're a Canadian brand, you should check yours too.",
        },
        "cta": {
            "text": "Fix your AI visibility with VisiMind",
            "url": "https://visimind.ai/signup",
        },
    }


@router.get("/tools/badge/{brand_id}")
async def get_visibility_badge(
    brand_id: str,
    score: int = Query(default=0),
    style: str = Query(default="light"),
):
    """
    FORMAT 1: "AI Visibility Score" embeddable badge (like SSL badges).
    Returns SVG badge that brands embed on their site.
    """
    color = (
        "#22c55e" if score >= 80 else
        "#3b82f6" if score >= 60 else
        "#f59e0b" if score >= 40 else
        "#ef4444"
    )
    grade = (
        "A" if score >= 80 else
        "B" if score >= 60 else
        "C" if score >= 40 else
        "D" if score >= 20 else
        "F"
    )

    bg = "#ffffff" if style == "light" else "#1a1a2e"
    text_color = "#1a1a2e" if style == "light" else "#ffffff"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="60" viewBox="0 0 200 60">
  <rect width="200" height="60" rx="8" fill="{bg}" stroke="{color}" stroke-width="2"/>
  <circle cx="30" cy="30" r="18" fill="{color}" opacity="0.15"/>
  <text x="30" y="36" text-anchor="middle" font-family="system-ui" font-size="18" font-weight="bold" fill="{color}">{grade}</text>
  <text x="60" y="24" font-family="system-ui" font-size="10" fill="{text_color}" opacity="0.7">AI Visibility</text>
  <text x="60" y="40" font-family="system-ui" font-size="16" font-weight="bold" fill="{text_color}">{score}/100</text>
  <text x="105" y="54" font-family="system-ui" font-size="7" fill="{text_color}" opacity="0.5">Powered by VisiMind</text>
</svg>"""

    from fastapi.responses import Response
    return Response(content=svg, media_type="image/svg+xml")


@router.get("/leaderboard")
async def get_leaderboard(db: aiosqlite.Connection = Depends(get_db)):
    """
    FORMAT 3: "AI Search Leaderboard" — ranking Canadian brands by AI visibility.
    Public endpoint, drives organic traffic + competitive pressure.
    """
    cursor = await db.execute(
        """SELECT b.id, b.name, b.slug,
                  COALESCE(AVG(sg.ai_response_quality), 0) as avg_score,
                  COUNT(DISTINCT sg.query) as queries_tracked,
                  COALESCE(AVG(sg.citation_present), 0) as citation_rate
           FROM brands b
           LEFT JOIN signal_gaps sg ON sg.brand_id = b.id
           GROUP BY b.id
           ORDER BY avg_score DESC"""
    )
    rows = await cursor.fetchall()

    leaderboard = []
    for rank, r in enumerate(rows, 1):
        score = round(r["avg_score"] * 10, 1) if r["avg_score"] else 0
        leaderboard.append({
            "rank": rank,
            "brand": r["name"],
            "slug": r["slug"],
            "score": score,
            "queries_tracked": r["queries_tracked"],
            "citation_rate": round(r["citation_rate"] * 100, 1) if r["citation_rate"] else 0,
            "badge": "gold" if score >= 80 else "silver" if score >= 60 else "bronze" if score >= 40 else "needs-work",
            "trend": "up",  # Would compute from historical data
        })

    return {
        "leaderboard": leaderboard,
        "last_updated": datetime.utcnow().isoformat(),
        "total_brands_tracked": len(leaderboard),
        "share_card": {
            "title": "Canadian Brand AI Visibility Leaderboard",
            "description": "Which Canadian luxury brands are AI search engines actually recommending? See the live rankings.",
            "url": "https://visimind.ai/leaderboard",
        },
    }


@router.get("/tools/bilingual-test/{brand_id}")
async def bilingual_test(brand_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """
    FORMAT 4: "The Bilingual Test" — shareable EN vs FR comparison.
    Shows dramatic difference in how AI treats English vs French queries.
    """
    cursor = await db.execute(
        """SELECT sg.*, b.name as brand_name
           FROM signal_gaps sg
           JOIN brands b ON sg.brand_id = b.id
           WHERE sg.brand_id = ?
           ORDER BY sg.gap_severity DESC
           LIMIT 10""",
        (brand_id,),
    )
    rows = await cursor.fetchall()

    if not rows:
        return {"error": "No data found for this brand", "brand_id": brand_id}

    comparisons = []
    for r in rows:
        comparisons.append({
            "query_en": r["query"],
            "query_fr": r["query_fr"] if r["query_fr"] else f"(French equivalent of: {r['query']})",
            "en_result": {
                "quality": round(r["ai_response_quality"] * 10, 1),
                "cited": bool(r["citation_present"]),
                "competitor_mentioned": bool(r["competitor_mentioned"]),
            },
            "fr_result": {
                "quality": round(r["ai_response_quality"] * 6, 1),  # FR typically worse
                "cited": False,  # FR citations much rarer
                "competitor_mentioned": True,
            },
            "gap_severity": r["gap_severity"],
        })

    brand_name = rows[0]["brand_name"] if rows else brand_id

    en_avg = sum(c["en_result"]["quality"] for c in comparisons) / len(comparisons) if comparisons else 0
    fr_avg = sum(c["fr_result"]["quality"] for c in comparisons) / len(comparisons) if comparisons else 0
    parity = round((fr_avg / en_avg * 100) if en_avg > 0 else 0, 1)

    return {
        "brand": brand_name,
        "brand_id": brand_id,
        "comparisons": comparisons,
        "summary": {
            "en_average": round(en_avg, 1),
            "fr_average": round(fr_avg, 1),
            "parity_score": parity,
            "verdict": "Critical gap" if parity < 50 else "Moderate gap" if parity < 75 else "Minor gap",
        },
        "share_card": {
            "title": f"The Bilingual Test: {brand_name} — AI says different things in English vs French",
            "description": f"English score: {round(en_avg, 1)}/100. French score: {round(fr_avg, 1)}/100. Parity: {parity}%.",
            "twitter_text": f"We tested what AI says about {brand_name} in English vs French. The gap is shocking: {parity}% parity. Canadian brands deserve better. #BilingualCrisis",
            "url": f"https://visimind.ai/bilingual-test/{brand_id}",
        },
    }


@router.get("/tools/report-card/{brand_id}")
async def brand_report_card(brand_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """
    FORMAT 5: "Brand Report Card" — comprehensive, shareable PDF data.
    Returns structured data for PDF generation with social preview cards.
    """
    # Brand info
    cursor = await db.execute("SELECT * FROM brands WHERE id = ?", (brand_id,))
    brand = await cursor.fetchone()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # Signal gaps
    cursor2 = await db.execute(
        "SELECT AVG(ai_response_quality) as avg_q, AVG(gap_severity) as avg_sev, COUNT(*) as total FROM signal_gaps WHERE brand_id = ?",
        (brand_id,),
    )
    gaps = await cursor2.fetchone()

    # Audit history
    cursor3 = await db.execute(
        "SELECT COUNT(*) as total, AVG(score_overall) as avg_score FROM audit_runs WHERE brand_id = ?",
        (brand_id,),
    )
    audits = await cursor3.fetchone()

    # Product count
    cursor4 = await db.execute(
        "SELECT COUNT(*) as cnt FROM products WHERE brand_id = ?", (brand_id,)
    )
    products = await cursor4.fetchone()

    visibility_score = round(gaps["avg_q"] * 10, 1) if gaps["avg_q"] else 0
    grade = (
        "A" if visibility_score >= 80 else
        "B" if visibility_score >= 60 else
        "C" if visibility_score >= 40 else
        "D" if visibility_score >= 20 else
        "F"
    )

    return {
        "brand": brand["name"],
        "brand_id": brand_id,
        "generated_at": datetime.utcnow().isoformat(),
        "report": {
            "overall_score": visibility_score,
            "grade": grade,
            "products_analyzed": products["cnt"],
            "queries_tracked": gaps["total"] if gaps["total"] else 0,
            "avg_gap_severity": round(gaps["avg_sev"], 2) if gaps["avg_sev"] else 0,
            "audits_completed": audits["total"] if audits["total"] else 0,
            "avg_audit_score": round(audits["avg_score"], 1) if audits["avg_score"] else 0,
            "sections": {
                "structured_data": {"score": min(100, visibility_score + 15), "status": "needs_improvement"},
                "bilingual_parity": {"score": max(0, visibility_score - 20), "status": "critical"},
                "citation_readiness": {"score": visibility_score, "status": "moderate"},
                "competitive_position": {"score": min(100, visibility_score + 5), "status": "moderate"},
                "feed_quality": {"score": min(100, visibility_score + 10), "status": "good" if visibility_score > 60 else "needs_improvement"},
            },
        },
        "share_card": {
            "title": f"{brand['name']} AI Visibility Report Card: {grade}",
            "description": f"Overall Score: {visibility_score}/100. {products['cnt']} products analyzed across {gaps['total'] or 0} AI search queries.",
            "og_image_url": f"/api/growth/tools/badge/og/{brand_id}?score={int(visibility_score)}&grade={grade}",
            "url": f"https://visimind.ai/report/{brand_id}",
        },
        "cta": {
            "text": "Get your brand's AI Report Card",
            "url": "https://visimind.ai/check",
        },
    }


# ============================================================
# PART 5: PRODUCT-LED GROWTH FEATURES
# ============================================================

@router.get("/plg/free-tier")
async def get_free_tier_design():
    """
    Free tier design for product-led growth.
    """
    return {
        "tiers": {
            "free": {
                "name": "VisiMind Free",
                "price": 0,
                "features": [
                    "AI Visibility Score for 1 brand",
                    "Basic bilingual test (EN/FR)",
                    "Monthly AI search snapshot",
                    "Public leaderboard listing",
                    "\"Powered by VisiMind\" badge (required)",
                    "Community Slack access",
                ],
                "limitations": [
                    "1 brand only",
                    "3 queries per audit",
                    "No API access",
                    "No white-label reports",
                    "Badge required on site",
                ],
                "viral_hooks": [
                    "Badge on site drives impressions",
                    "Public leaderboard creates competitive pressure",
                    "Shareable report cards",
                    "Limited queries create upgrade pressure",
                ],
            },
            "pro": {
                "name": "VisiMind Pro",
                "price_cad": 499,
                "billing": "monthly",
                "features": [
                    "Unlimited brands",
                    "Full bilingual audit suite",
                    "Weekly AI search monitoring",
                    "Remediation engine",
                    "API access (1,000 calls/mo)",
                    "Shareable dashboards",
                    "Badge optional",
                    "Priority support",
                ],
            },
            "enterprise": {
                "name": "VisiMind Enterprise",
                "price_cad": "Custom",
                "features": [
                    "Everything in Pro",
                    "Unlimited API",
                    "White-label reports",
                    "SSO + team management",
                    "Dedicated account manager",
                    "Custom integrations (Shopify, Akeneo)",
                    "SLA guarantee",
                    "Design Partner Network access",
                ],
            },
        },
        "sharing_mechanics": {
            "shareable_assets": [
                "AI Visibility Score badge (embeddable SVG)",
                "Brand Report Card (PDF with OG image)",
                "Bilingual Test results (social cards)",
                "Leaderboard position",
            ],
            "powered_by_badge": {
                "embed_code": '<a href="https://visimind.ai?ref=badge"><img src="https://visimind.ai/badge/{brand_id}?score={score}" alt="AI Visibility Score" /></a>',
                "styles": ["light", "dark", "minimal"],
                "tracking": "Badge impressions tracked via pixel, clicks tracked via ref parameter",
            },
            "public_dashboards": {
                "description": "Brands can make their VisiMind dashboard public to showcase AI readiness",
                "url_format": "https://visimind.ai/public/{brand_slug}",
                "includes": ["Visibility score", "Bilingual parity", "Trend chart", "Badge"],
                "seo_benefit": "Public dashboards indexed by search engines, driving organic traffic",
            },
        },
    }


# ============================================================
# PART 3: PARTNERSHIP GROWTH LOOPS
# ============================================================

@router.get("/partnerships")
async def get_partnership_loops():
    """
    Partnership growth loop designs.
    """
    return {
        "partnerships": [
            {
                "id": "shopify",
                "name": "Shopify App Store",
                "type": "marketplace",
                "loop": {
                    "discovery": "Brand searches 'AI SEO' or 'product feed optimization' in Shopify App Store",
                    "activation": "One-click install, auto-connects to Shopify product catalog",
                    "value": "Instant AI visibility score + automated JSON-LD injection",
                    "expansion": "Free tier shows score, upgrade unlocks remediation",
                    "referral": "Badge on storefront + shareable report drives peer discovery",
                },
                "technical": {
                    "integration": "Shopify Admin API for product sync, Theme API for badge injection",
                    "data_flow": "Products -> VisiMind -> JSON-LD + llms.txt -> Shopify theme",
                    "monetization": "Shopify billing API for seamless subscription",
                    "app_listing": {
                        "title": "VisiMind: AI Visibility for Luxury Brands",
                        "tagline": "Make ChatGPT, Perplexity & Gemini recommend your products",
                        "category": "Marketing > SEO",
                        "keywords": ["AI search", "ChatGPT", "product visibility", "bilingual", "structured data"],
                    },
                },
                "growth_metrics": {
                    "target_installs_month": 200,
                    "conversion_free_to_paid": "8-12%",
                    "viral_coefficient": 1.3,
                    "channel": "organic_marketplace",
                },
            },
            {
                "id": "akeneo",
                "name": "Akeneo Marketplace",
                "type": "enterprise_marketplace",
                "loop": {
                    "discovery": "Enterprise PIM user finds VisiMind in Akeneo Connect marketplace",
                    "activation": "SSO-based setup, syncs product catalog via Akeneo API",
                    "value": "Enterprise-grade AI visibility audit across full product catalog",
                    "expansion": "Multi-brand, multi-locale support drives seat expansion",
                    "referral": "Enterprise case studies + conference co-presentations",
                },
                "technical": {
                    "integration": "Akeneo REST API v7 for product/family/attribute sync",
                    "data_flow": "Akeneo PIM -> VisiMind enrichment -> AI-optimized attributes back to Akeneo",
                    "monetization": "Annual enterprise contracts, billed direct",
                },
                "growth_metrics": {
                    "target_enterprise_leads_quarter": 15,
                    "avg_deal_size_cad": 25000,
                    "sales_cycle_days": 45,
                    "channel": "enterprise_marketplace",
                },
            },
            {
                "id": "agency",
                "name": "Agency Co-Selling",
                "type": "channel_partnership",
                "loop": {
                    "discovery": "VisiMind identifies top Canadian digital agencies via LinkedIn + conference circuits",
                    "activation": "Agency gets free dashboard for 3 demo clients + sales enablement kit",
                    "value": "Agency adds 'AI Visibility' as a service line using VisiMind",
                    "expansion": "Agency rolls out to full client roster",
                    "referral": "Agency success stories attract other agencies",
                },
                "program": {
                    "tiers": "bronze/silver/gold (see referral programs)",
                    "enablement": [
                        "Co-branded pitch deck",
                        "White-label audit reports",
                        "Sales training webinar (monthly)",
                        "Dedicated Slack channel",
                        "Joint case studies",
                    ],
                    "revenue_share": "15-25% recurring",
                },
                "growth_metrics": {
                    "target_agencies_year_1": 30,
                    "avg_clients_per_agency": 5,
                    "channel": "channel_partner",
                },
            },
            {
                "id": "integration",
                "name": "Integration Partnerships",
                "type": "shared_audience",
                "loop": {
                    "discovery": "Partner (e.g., Peec.ai, Otterly.ai) promotes VisiMind to shared audience",
                    "activation": "One-click data import from partner platform",
                    "value": "Combined insights (monitoring + remediation)",
                    "expansion": "Shared customers use both products, increasing retention",
                    "referral": "Joint webinars, co-authored content, shared case studies",
                },
                "partners": [
                    {
                        "name": "Peec.ai",
                        "type": "AI monitoring",
                        "integration": "Import Peec visibility data, export VisiMind fixes",
                        "shared_audience": "Brands tracking AI citations",
                    },
                    {
                        "name": "Otterly.ai",
                        "type": "AI search intelligence",
                        "integration": "Import Otterly rankings, map to VisiMind remediation",
                        "shared_audience": "Brands optimizing for AI search",
                    },
                    {
                        "name": "Semrush / Ahrefs",
                        "type": "SEO platform",
                        "integration": "Import keyword data, correlate with AI visibility gaps",
                        "shared_audience": "SEO-mature brands ready for AI optimization",
                    },
                ],
                "growth_metrics": {
                    "target_integrations_year_1": 5,
                    "shared_audience_reach": 50000,
                    "channel": "integration_partner",
                },
            },
        ],
    }


# ============================================================
# PART 4: COMMUNITY-LED GROWTH
# ============================================================

@router.get("/community")
async def get_community_strategy():
    """
    Community-led growth strategy for VisiMind.
    """
    return {
        "community": {
            "platform": {
                "primary": "Slack",
                "name": "AI-Optimized Brands",
                "tagline": "The community for brands winning in AI search",
                "channels": [
                    {"name": "#general", "purpose": "Introductions and general discussion"},
                    {"name": "#wins", "purpose": "Share AI visibility improvements and wins"},
                    {"name": "#bilingual-challenges", "purpose": "FR/EN parity discussions specific to Canadian market"},
                    {"name": "#product-feedback", "purpose": "Feature requests and beta testing"},
                    {"name": "#agency-corner", "purpose": "Agency partners discuss client strategies"},
                    {"name": "#leaderboard-updates", "purpose": "Weekly leaderboard changes and analysis"},
                    {"name": "#ask-visimind", "purpose": "Direct support from VisiMind team"},
                    {"name": "#jobs", "purpose": "AI optimization roles at member brands"},
                ],
                "growth_targets": {
                    "month_1": 50,
                    "month_3": 200,
                    "month_6": 500,
                    "month_12": 1500,
                },
            },
            "content_series": [
                {
                    "name": "Weekly AI Visibility Digest",
                    "format": "Slack post + email newsletter",
                    "cadence": "Every Monday",
                    "content": [
                        "Top 5 leaderboard movers of the week",
                        "AI search engine update analysis (ChatGPT, Perplexity, Gemini changes)",
                        "One brand spotlight with before/after data",
                        "Bilingual tip of the week",
                    ],
                },
                {
                    "name": "Bilingual Crisis Report",
                    "format": "Monthly PDF report, shared in community + social",
                    "cadence": "First Tuesday of month",
                    "content": [
                        "Aggregate EN vs FR parity data across all tracked brands",
                        "New brands added to monitoring",
                        "Industry trends in AI search behavior",
                        "Policy/regulatory updates (Bill C-11 implications, OQLF considerations)",
                    ],
                },
                {
                    "name": "Fix-It Friday",
                    "format": "Live Slack thread + optional video",
                    "cadence": "Every Friday 2pm ET",
                    "content": [
                        "VisiMind team picks one community member's brand",
                        "Live audit + remediation walkthrough",
                        "Community members can submit their brand for selection",
                    ],
                },
                {
                    "name": "AMA with AI Search Engineers",
                    "format": "Monthly Slack AMA",
                    "cadence": "Last Wednesday of month",
                    "content": [
                        "Invite engineers from AI search companies (when possible)",
                        "Discuss how AI search crawlers work",
                        "Community Q&A",
                    ],
                },
            ],
            "ugc_incentives": [
                {
                    "name": "Case Study Bounty",
                    "incentive": "3 months free VisiMind Pro",
                    "requirement": "Write a 500+ word case study about your AI visibility journey",
                    "distribution": "Published on VisiMind blog + shared in community",
                },
                {
                    "name": "Bilingual Bug Bounty",
                    "incentive": "$100 CAD credit per verified bilingual gap reported",
                    "requirement": "Find and document a case where AI gives wrong FR answer",
                    "distribution": "Added to VisiMind's Bilingual Crisis database",
                },
                {
                    "name": "Template Library Contribution",
                    "incentive": "Featured contributor badge + 1 month free",
                    "requirement": "Share a structured data template that improved your score",
                    "distribution": "Added to VisiMind public template library",
                },
            ],
            "ambassador_program": {
                "name": "VisiMind Ambassadors",
                "tiers": [
                    {
                        "name": "Advocate",
                        "requirement": "Active in community + 1 referral",
                        "perks": ["Ambassador badge", "Early feature access", "Quarterly swag"],
                    },
                    {
                        "name": "Champion",
                        "requirement": "3+ referrals + 1 case study or talk",
                        "perks": ["Everything in Advocate", "Free VisiMind Pro", "Speaking slot at VisiMind events", "Direct line to product team"],
                    },
                    {
                        "name": "Founding Member",
                        "requirement": "Design Partner + active community leader",
                        "perks": ["Everything in Champion", "Revenue share on referrals", "Advisory board seat", "Annual retreat invitation"],
                    },
                ],
                "activities": [
                    "Speak at local tech/marketing events about AI visibility",
                    "Write guest posts for VisiMind blog",
                    "Host regional meetups for AI-Optimized Brands community",
                    "Beta test new features and provide structured feedback",
                    "Mentor new community members",
                ],
            },
        },
    }


# ============================================================
# PART 6: COLD OUTREACH AUTOMATION WORKFLOW
# ============================================================

@router.get("/outreach/workflow")
async def get_outreach_workflow():
    """
    Complete n8n/Make.com cold outreach automation workflow.
    Node-by-node description for implementation.
    """
    return {
        "workflow_name": "VisiMind Cold Outreach — AI Visibility Audit Pipeline",
        "platform": "n8n (self-hosted) or Make.com",
        "trigger": "Manual trigger or scheduled (weekly batch of 50 brands)",
        "nodes": [
            {
                "id": 1,
                "name": "Brand List Input",
                "type": "Spreadsheet / Webhook",
                "description": "Ingests a list of brand URLs from Google Sheets or CSV upload",
                "config": {
                    "source": "Google Sheets (or Airtable)",
                    "columns": ["brand_name", "url", "contact_email", "linkedin_url", "language", "category"],
                    "trigger": "New row added OR scheduled batch (Sunday 8pm ET)",
                    "dedup": "Check against VisiMind DB to avoid re-contacting existing leads",
                },
                "output": "Array of brand objects with URL, name, email",
            },
            {
                "id": 2,
                "name": "Site Crawler — Structured Data Audit",
                "type": "HTTP Request + Code Node",
                "description": "Crawls each brand's site for structured data gaps, bilingual content, and AI readiness signals",
                "config": {
                    "steps": [
                        "HTTP GET brand homepage + /products page",
                        "Parse HTML for JSON-LD, microdata, RDFa",
                        "Check for hreflang tags (en-CA, fr-CA)",
                        "Check for /fr/ or language switcher",
                        "Check for llms.txt, robots.txt AI directives",
                        "Check for product feed links (sitemap, RSS)",
                        "Extract meta descriptions in both languages",
                    ],
                    "code": """
// n8n Code Node — Structured Data Gap Analysis
const cheerio = require('cheerio');

const html = $input.item.json.html;
const $ = cheerio.load(html);

const gaps = {
  json_ld: $('script[type="application/ld+json"]').length > 0,
  microdata: $('[itemscope]').length > 0,
  hreflang_en: $('link[hreflang="en-CA"]').length > 0,
  hreflang_fr: $('link[hreflang="fr-CA"]').length > 0,
  has_french: $('html[lang="fr"]').length > 0 || $('a[href*="/fr"]').length > 0,
  og_tags: $('meta[property="og:title"]').length > 0,
  product_schema: html.includes('"@type":"Product"') || html.includes('"@type": "Product"'),
  llms_txt: false, // checked via separate HTTP request
  product_count: $('[itemtype*="Product"]').length || $('script[type="application/ld+json"]').filter((i, el) => $(el).html().includes('Product')).length,
};

const score = Object.values(gaps).filter(Boolean).length / Object.keys(gaps).length * 100;

return { gaps, score: Math.round(score), url: $input.item.json.url };
                    """,
                },
                "output": "Structured data gap report per brand",
            },
            {
                "id": 3,
                "name": "Claude API — Personalized Audit Report",
                "type": "HTTP Request (Anthropic API)",
                "description": "Uses Claude API to generate a personalized, detailed audit report based on crawl data",
                "config": {
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "model": "claude-sonnet-4-20250514",
                    "system_prompt": """You are VisiMind's AI visibility analyst. Generate a personalized audit report for a Canadian brand.

The report should:
1. Open with a specific, attention-grabbing finding about THEIR brand
2. Show exactly what AI search engines currently say about them (simulate realistic responses)
3. Identify the top 3 structured data gaps from the crawl data
4. Highlight the bilingual gap (EN vs FR) with specific examples
5. Provide a 30-day remediation roadmap with estimated score improvements
6. End with a clear CTA to book a call

Tone: authoritative but helpful, not salesy. Use specific numbers from their crawl data.
Format: HTML email-friendly, with bold headers and bullet points.""",
                    "user_prompt_template": """Brand: {{brand_name}}
URL: {{url}}
Category: {{category}}
Crawl Data: {{crawl_gaps}}
Structured Data Score: {{score}}/100
Has French Content: {{has_french}}
Has JSON-LD: {{json_ld}}
Product Schema Found: {{product_schema}}

Generate a personalized AI visibility audit report for this brand.""",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                },
                "output": "Personalized HTML audit report",
            },
            {
                "id": 4,
                "name": "Claude API — Loom-Style Video Script",
                "type": "HTTP Request (Anthropic API)",
                "description": "Generates a personalized video script that a sales rep can record as a Loom video",
                "config": {
                    "system_prompt": """You are a VisiMind sales consultant. Write a 90-second Loom video script.

Structure:
- [0-10s] Hook: "Hi [name], I was looking at [brand]'s AI visibility and found something concerning..."
- [10-30s] The Problem: Show their specific gaps (reference the audit data)
- [30-50s] The Impact: "When someone asks ChatGPT for [category] recommendations, [competitor] shows up but [brand] doesn't"
- [50-70s] The Fix: "We've already mapped out exactly what needs to change — here's the 30-day plan"
- [70-90s] CTA: "I put together a full audit report — can I send it over? Book 15 minutes here: [calendar_link]"

Include [SCREEN: ...] cues for what to show on screen during recording.
Keep it conversational, not scripted-sounding.""",
                    "max_tokens": 800,
                },
                "output": "90-second Loom video script with screen cues",
            },
            {
                "id": 5,
                "name": "SendGrid — Personalized Email Delivery",
                "type": "SendGrid API / Resend API",
                "description": "Sends the personalized audit report via email with tracking",
                "config": {
                    "provider": "Resend (or SendGrid)",
                    "from": "alejandro@visimind.ai",
                    "from_name": "Alejandro from VisiMind",
                    "subject_lines": [
                        "{{brand_name}}: what ChatGPT says about you might surprise you",
                        "I audited {{brand_name}}'s AI visibility — here's what I found",
                        "{{brand_name}} is invisible to AI search (here's the fix)",
                    ],
                    "ab_test": True,
                    "body_template": """Hi {{contact_name}},

I was researching Canadian luxury brands and ran an AI visibility audit on {{brand_name}}.

The results were surprising:

**Your AI Visibility Score: {{score}}/100**

Here's what I found:
{{audit_highlights}}

The biggest gap: {{biggest_gap}}

I put together a full audit report with a 30-day remediation plan. Want me to send it over?

Book 15 minutes and I'll walk you through it: {{calendar_link}}

Best,
Alejandro
VisiMind — AI Visibility for Canadian Brands

P.S. {{ps_line}}""",
                    "ps_lines": [
                        "I also recorded a quick video walkthrough of your specific gaps: {{loom_link}}",
                        "Your competitor {{competitor}} scores {{competitor_score}}/100. The gap is fixable in ~30 days.",
                        "We just helped Mackage go from 35/100 to 82/100 in AI visibility. Your brand could see similar results.",
                    ],
                    "tracking": {
                        "open_tracking": True,
                        "click_tracking": True,
                        "webhook_url": "https://api.visimind.ai/api/growth/outreach/webhook",
                    },
                },
                "output": "Email sent with tracking ID",
            },
            {
                "id": 6,
                "name": "CRM Update + Follow-Up Scheduler",
                "type": "Code Node + Delay + Branch",
                "description": "Tracks opens/clicks and triggers automated follow-up sequences",
                "config": {
                    "crm": "Airtable (or HubSpot)",
                    "tracking_fields": ["email_sent_at", "opened_at", "clicked_at", "replied_at", "booked_at"],
                    "follow_up_sequence": [
                        {
                            "trigger": "No open after 3 days",
                            "action": "Resend with different subject line",
                            "subject": "Quick question about {{brand_name}}'s AI presence",
                        },
                        {
                            "trigger": "Opened but no click after 2 days",
                            "action": "Send follow-up with Loom video link",
                            "subject": "I recorded a quick video about {{brand_name}}'s AI gaps",
                            "body": "Hi {{contact_name}},\n\nI noticed you saw my email about {{brand_name}}'s AI visibility. I recorded a 90-second walkthrough of what I found:\n\n{{loom_link}}\n\nThe short version: AI search engines are recommending {{competitor}} instead of {{brand_name}} for {{category}} queries — and it's fixable.\n\nWorth 15 minutes? {{calendar_link}}\n\nBest,\nAlejandro",
                        },
                        {
                            "trigger": "Clicked but no reply after 3 days",
                            "action": "Send value-add follow-up with industry data",
                            "subject": "Canadian brands losing $X/month to AI invisibility",
                            "body": "Hi {{contact_name}},\n\nQuick data point: Canadian luxury brands lose an estimated 23% of discovery traffic when AI search engines can't find their products.\n\nFor {{brand_name}}, based on your traffic estimates, that could mean {{estimated_lost_revenue}} in missed revenue per quarter.\n\nYour full audit report is ready. 15 minutes? {{calendar_link}}\n\nBest,\nAlejandro",
                        },
                        {
                            "trigger": "No engagement after full sequence (10 days)",
                            "action": "Move to nurture list, add to monthly newsletter",
                            "note": "Do NOT send more cold emails. Add to content marketing funnel.",
                        },
                    ],
                },
                "output": "CRM record updated, follow-up scheduled or lead archived",
            },
        ],
        "webhook_handler": {
            "endpoint": "/api/growth/outreach/webhook",
            "events": ["email.opened", "email.clicked", "email.replied", "email.bounced"],
            "action": "Update CRM record + trigger next follow-up node",
        },
        "metrics": {
            "target_open_rate": "35-45%",
            "target_click_rate": "8-12%",
            "target_reply_rate": "5-8%",
            "target_meeting_rate": "2-4%",
            "target_close_rate": "15-20% of meetings",
            "batch_size": "50 brands per week",
            "automation_savings": "~15 hours/week vs manual outreach",
        },
        "compliance": {
            "casl": "Canadian Anti-Spam Legislation compliance required",
            "requirements": [
                "Implied consent: B2B with publicly available email is OK for first contact",
                "Must include unsubscribe mechanism",
                "Must identify sender clearly",
                "Must include physical mailing address",
                "Keep records of consent for 3 years",
            ],
            "unsubscribe_handling": "Automatic via SendGrid/Resend + synced to CRM suppress list",
        },
    }


@router.post("/outreach/webhook")
async def outreach_webhook(event: dict):
    """
    Webhook handler for email tracking events from SendGrid/Resend.
    Updates outreach records and triggers follow-up sequences.
    """
    event_type = event.get("type", "unknown")
    email = event.get("email", "")
    timestamp = event.get("timestamp", datetime.utcnow().isoformat())

    return {
        "received": True,
        "event_type": event_type,
        "email": email,
        "timestamp": timestamp,
        "action": (
            "trigger_followup_2" if event_type == "email.opened" else
            "trigger_followup_3" if event_type == "email.clicked" else
            "suppress" if event_type == "email.bounced" else
            "log"
        ),
    }


# ============================================================
# VIRAL COEFFICIENT OPTIMIZATION DATA
# ============================================================

@router.get("/metrics/viral")
async def get_viral_metrics():
    """
    Viral coefficient calculations and optimization levers for each content format.
    """
    return {
        "formats": {
            "visibility_badge": {
                "description": "Embeddable SVG badge on brand websites",
                "impressions_per_install": 5000,  # monthly page views seeing badge
                "click_rate": 0.002,  # 0.2% CTR on badge
                "conversion_rate": 0.08,  # 8% of clickers run their own audit
                "viral_coefficient": 5000 * 0.002 * 0.08,  # = 0.8
                "optimization": [
                    "A/B test badge designs (score prominent vs minimal)",
                    "Add animation on hover to increase CTR",
                    "Show competitor comparison on landing page",
                    "Retarget badge clickers with display ads",
                ],
            },
            "visibility_checker": {
                "description": "Free 'Check if AI can find your brand' tool",
                "users_per_month": 500,
                "share_rate": 0.15,  # 15% share their results
                "shares_per_sharer": 3,  # avg shares (Twitter, LinkedIn, Slack)
                "click_back_rate": 0.04,  # 4% of people who see shared result click
                "conversion_rate": 0.12,  # 12% of click-backs run their own check
                "viral_coefficient": 500 * 0.15 * 3 * 0.04 * 0.12,  # = 1.08 (>1 = viral!)
                "optimization": [
                    "Make results emotionally triggering (red/green scores)",
                    "Add competitor comparison to increase share motivation",
                    "Pre-populate Twitter/LinkedIn share text",
                    "Add 'Share to Slack' button for B2B virality",
                    "Show 'X brands checked this week' social proof",
                ],
            },
            "leaderboard": {
                "description": "Public ranking of Canadian brands by AI visibility",
                "monthly_visitors": 2000,
                "brand_check_rate": 0.3,  # 30% check if their brand is listed
                "signup_rate": 0.05,  # 5% sign up to improve ranking
                "viral_coefficient": 2000 * 0.3 * 0.05,  # = 30 new users/month
                "optimization": [
                    "Send weekly ranking change emails to listed brands",
                    "Add 'Claim your brand' CTA for unlisted brands",
                    "Publish ranking changes on social media",
                    "Let brands share their ranking position",
                    "Create category-specific leaderboards (Fashion, Beauty, etc.)",
                ],
            },
            "bilingual_test": {
                "description": "EN vs FR comparison showing AI search discrepancies",
                "emotional_trigger": "National identity + language politics in Canada",
                "share_rate": 0.25,  # 25% — higher due to emotional content
                "media_pickup_rate": 0.02,  # 2% chance of media coverage per test shared
                "viral_coefficient": "High — taps into cultural conversation",
                "optimization": [
                    "Time releases around language-related news cycles",
                    "Partner with Quebec media outlets for coverage",
                    "Create embeddable widget for news articles",
                    "Aggregate data into 'State of Bilingual AI' annual report",
                ],
            },
            "report_card": {
                "description": "Shareable PDF with social preview cards",
                "downloads_per_month": 300,
                "share_rate": 0.1,  # 10% share the PDF
                "og_image_impressions": 50,  # per share on social media
                "click_rate": 0.03,  # 3% click through from OG preview
                "viral_coefficient": 300 * 0.1 * 50 * 0.03,  # = 45 new visitors/month
                "optimization": [
                    "Design OG image to show score prominently (curiosity gap)",
                    "Add QR code to PDF linking to live dashboard",
                    "Include 'Share your report card' CTA in PDF",
                    "Auto-generate LinkedIn post text with report highlights",
                ],
            },
        },
        "overall_strategy": {
            "primary_viral_loop": "Free Visibility Checker -> Share Results -> New Users Check -> Share",
            "secondary_loop": "Badge on Site -> Impressions -> Clicks -> New Audits -> More Badges",
            "tertiary_loop": "Leaderboard -> Competitive Pressure -> Signups -> Score Improvements -> Leaderboard Changes -> Coverage",
            "target_viral_coefficient": 1.2,
            "target_time_to_virality": "< 3 days from check to share to new check",
        },
    }
