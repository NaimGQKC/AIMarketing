"""
VisiMind -- PDF Scary Report Generator

Generates a professional, alarming audit PDF designed to be shared with VPs.
Dark color scheme with cyan accents and red for critical findings.
"""
import io
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# -- Brand colors --
DARK_BG = colors.HexColor("#0a0e1a")
CYAN_ACCENT = colors.HexColor("#00e5ff")
RED_CRITICAL = colors.HexColor("#ff4c6a")
AMBER_WARNING = colors.HexColor("#ffb347")
GREEN_HEALTHY = colors.HexColor("#00e676")
WHITE = colors.white
LIGHT_GRAY = colors.HexColor("#e0e0e0")
MID_GRAY = colors.HexColor("#888888")
DARK_ROW = colors.HexColor("#121828")
DARK_ROW_ALT = colors.HexColor("#1a2236")


def _grade_color(grade: str) -> colors.Color:
    if grade == "RED":
        return RED_CRITICAL
    elif grade == "YELLOW":
        return AMBER_WARNING
    return GREEN_HEALTHY


def _score_color(score: int) -> colors.Color:
    if score < 40:
        return RED_CRITICAL
    elif score < 70:
        return AMBER_WARNING
    return GREEN_HEALTHY


def _build_styles() -> dict:
    """Build all custom paragraph styles."""
    base = getSampleStyleSheet()
    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title",
        parent=base["Title"],
        fontSize=32,
        leading=38,
        textColor=CYAN_ACCENT,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    styles["cover_brand"] = ParagraphStyle(
        "cover_brand",
        parent=base["Title"],
        fontSize=26,
        leading=32,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    styles["cover_sub"] = ParagraphStyle(
        "cover_sub",
        parent=base["Normal"],
        fontSize=12,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["section_header"] = ParagraphStyle(
        "section_header",
        parent=base["Heading1"],
        fontSize=22,
        leading=28,
        textColor=CYAN_ACCENT,
        spaceAfter=14,
        spaceBefore=6,
    )
    styles["subsection"] = ParagraphStyle(
        "subsection",
        parent=base["Heading2"],
        fontSize=16,
        leading=20,
        textColor=WHITE,
        spaceAfter=8,
    )
    styles["body"] = ParagraphStyle(
        "body",
        parent=base["Normal"],
        fontSize=11,
        leading=15,
        textColor=LIGHT_GRAY,
        spaceAfter=8,
    )
    styles["body_bold"] = ParagraphStyle(
        "body_bold",
        parent=base["Normal"],
        fontSize=11,
        leading=15,
        textColor=WHITE,
        spaceAfter=8,
    )
    styles["score_big"] = ParagraphStyle(
        "score_big",
        parent=base["Title"],
        fontSize=60,
        leading=66,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles["finding_type"] = ParagraphStyle(
        "finding_type",
        parent=base["Heading3"],
        fontSize=14,
        leading=18,
        textColor=WHITE,
        spaceAfter=4,
        spaceBefore=12,
    )
    styles["snippet"] = ParagraphStyle(
        "snippet",
        parent=base["Code"],
        fontSize=9,
        leading=12,
        textColor=LIGHT_GRAY,
        backColor=DARK_ROW,
        borderPadding=6,
        spaceAfter=6,
    )
    styles["recommendation"] = ParagraphStyle(
        "recommendation",
        parent=base["Normal"],
        fontSize=12,
        leading=17,
        textColor=WHITE,
        spaceAfter=10,
        leftIndent=20,
        bulletIndent=6,
        bulletFontSize=14,
    )
    styles["table_header"] = ParagraphStyle(
        "table_header",
        parent=base["Normal"],
        fontSize=11,
        textColor=CYAN_ACCENT,
        alignment=TA_LEFT,
    )
    styles["table_cell"] = ParagraphStyle(
        "table_cell",
        parent=base["Normal"],
        fontSize=11,
        textColor=LIGHT_GRAY,
    )
    styles["footer_note"] = ParagraphStyle(
        "footer_note",
        parent=base["Normal"],
        fontSize=9,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        spaceBefore=30,
    )
    return styles


def _dark_bg_canvas(canvas, doc):
    """Draw dark background on every page."""
    canvas.saveState()
    canvas.setFillColor(DARK_BG)
    canvas.rect(0, 0, letter[0], letter[1], fill=True, stroke=False)
    # Footer line
    canvas.setStrokeColor(CYAN_ACCENT)
    canvas.setLineWidth(0.5)
    canvas.line(0.75 * inch, 0.5 * inch, letter[0] - 0.75 * inch, 0.5 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(0.75 * inch, 0.3 * inch, "VisiMind AI Visibility Audit -- Confidential")
    canvas.drawRightString(
        letter[0] - 0.75 * inch,
        0.3 * inch,
        f"Page {doc.page}",
    )
    canvas.restoreState()


def _finding_type_label(ftype: str) -> str:
    labels = {
        "ghosting": "Ghosting -- Brand Invisible",
        "rank_disparity": "Rank Disparity -- EN/FR Gap",
        "spec_dilution": "Spec Dilution -- Detail Loss",
        "competitor_hijacking": "Competitor Hijacking",
        "no_data": "Insufficient Data",
    }
    return labels.get(ftype, ftype.replace("_", " ").title())


def _severity_badge(severity: str) -> str:
    if severity == "critical":
        return f'<font color="{RED_CRITICAL.hexval()}"><b>CRITICAL</b></font>'
    return f'<font color="{AMBER_WARNING.hexval()}"><b>WARNING</b></font>'


def _truncate(text: str, max_len: int = 300) -> str:
    if not text:
        return "(no response captured)"
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def generate_audit_pdf(
    brand_profile: dict,
    ias_data: dict,
    revenue_impact: dict,
    probe_results: list,
) -> bytes:
    """
    Generate a full scary-report PDF and return the raw bytes.

    Args:
        brand_profile: dict with brand_name, primary_url, etc.
        ias_data: dict with score, grade, findings, breakdown, probes_analyzed, etc.
        revenue_impact: dict from estimate_revenue_impact()
        probe_results: list of probe result dicts

    Returns:
        bytes -- the PDF file content
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    styles = _build_styles()
    story = []

    score = ias_data.get("score", 0)
    grade = ias_data.get("grade", "RED")
    findings = ias_data.get("findings", [])
    breakdown = ias_data.get("breakdown", {})
    brand_name = brand_profile.get("brand_name", "Unknown Brand")
    score_clr = _score_color(score)

    # =============================================
    # PAGE 1: COVER
    # =============================================
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("AI Visibility Audit Report", styles["cover_title"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(brand_name, styles["cover_brand"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        datetime.now().strftime("%B %d, %Y"),
        styles["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Generated by VisiMind", styles["cover_sub"]))
    story.append(Spacer(1, 0.8 * inch))

    # IAS score badge
    score_style = ParagraphStyle(
        "score_display",
        parent=styles["score_big"],
        textColor=score_clr,
    )
    story.append(Paragraph(f"{score}", score_style))
    story.append(Paragraph(
        f'<font color="{score_clr.hexval()}">Inference Alignment Score</font>',
        styles["cover_sub"],
    ))
    story.append(Spacer(1, 0.15 * inch))

    grade_clr = _grade_color(grade)
    story.append(Paragraph(
        f'<font color="{grade_clr.hexval()}" size="18"><b>{grade}</b></font>',
        ParagraphStyle("grade_badge", parent=styles["cover_sub"], fontSize=18),
    ))

    story.append(PageBreak())

    # =============================================
    # PAGE 2: EXECUTIVE SUMMARY
    # =============================================
    story.append(Paragraph("Executive Summary", styles["section_header"]))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph(
        f'Your brand has an Inference Alignment Score of '
        f'<font color="{score_clr.hexval()}"><b>{score}/100</b></font>.',
        styles["body_bold"],
    ))
    story.append(Spacer(1, 0.1 * inch))

    # Grade explanation
    grade_explanations = {
        "RED": "Your brand suffers from <b>critical misalignment</b> in AI inference engines. "
               "AI assistants are actively failing to recommend, describe, or even mention your brand "
               "to potential customers -- especially in French-language queries.",
        "YELLOW": "Your brand has <b>moderate alignment issues</b>. While AI assistants recognize your brand "
                  "in some contexts, significant gaps exist in bilingual coverage, spec accuracy, or "
                  "competitive positioning.",
        "GREEN": "Your brand has <b>healthy alignment</b> across AI inference engines. Minor optimization "
                 "opportunities may still exist.",
    }
    story.append(Paragraph(
        f'<font color="{grade_clr.hexval()}"><b>Grade: {grade}</b></font> -- '
        f'{grade_explanations.get(grade, "")}',
        styles["body"],
    ))
    story.append(Spacer(1, 0.2 * inch))

    # Revenue impact
    lost_annual = revenue_impact.get("lost_revenue_annual", 0)
    lost_monthly = revenue_impact.get("lost_revenue_monthly", 0)
    vis_loss = revenue_impact.get("visibility_loss_pct", 0)

    story.append(Paragraph("Revenue Impact", styles["subsection"]))
    story.append(Paragraph(
        f'Estimated <font color="{RED_CRITICAL.hexval()}"><b>${lost_annual:,.0f}/year</b></font> '
        f'in lost revenue from AI visibility gaps '
        f'(${lost_monthly:,.0f}/month).',
        styles["body"],
    ))
    story.append(Paragraph(
        f'Your AI visibility loss is approximately <b>{vis_loss}%</b>, meaning that '
        f'percentage of AI-driven discovery queries fail to surface your brand.',
        styles["body"],
    ))
    story.append(Spacer(1, 0.2 * inch))

    # Probe stats
    probes_total = ias_data.get("probes_analyzed", len(probe_results))
    en_probes = ias_data.get("en_probes", 0)
    fr_probes = ias_data.get("fr_probes", 0)
    providers_tested = set()
    for p in probe_results:
        if isinstance(p, dict) and p.get("provider"):
            providers_tested.add(p["provider"])
    num_providers = len(providers_tested) if providers_tested else 1

    story.append(Paragraph("Audit Scope", styles["subsection"]))
    story.append(Paragraph(
        f'<b>{probes_total}</b> probes executed across <b>{num_providers}</b> AI provider(s). '
        f'<b>{en_probes}</b> English probes, <b>{fr_probes}</b> French probes.',
        styles["body"],
    ))

    story.append(PageBreak())

    # =============================================
    # PAGE 3: KEY FINDINGS
    # =============================================
    story.append(Paragraph("Key Findings", styles["section_header"]))
    story.append(Spacer(1, 0.1 * inch))

    if not findings:
        story.append(Paragraph(
            "No specific findings were flagged during this audit cycle.",
            styles["body"],
        ))
    else:
        for i, finding in enumerate(findings):
            ftype = finding.get("type", "unknown")
            severity = finding.get("severity", "warning")
            message = finding.get("message", "")
            detail_en = finding.get("detail_en", "")
            detail_fr = finding.get("detail_fr", "")

            # Finding header with severity badge
            story.append(Paragraph(
                f'{i + 1}. {_finding_type_label(ftype)} -- {_severity_badge(severity)}',
                styles["finding_type"],
            ))
            story.append(Paragraph(message, styles["body_bold"]))

            # EN snippet
            if detail_en:
                story.append(Paragraph(
                    f'<b>EN Response:</b>',
                    styles["body"],
                ))
                safe_en = _truncate(detail_en).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(safe_en, styles["snippet"]))

            # FR snippet
            if detail_fr:
                story.append(Paragraph(
                    f'<b>FR Response:</b>',
                    styles["body"],
                ))
                safe_fr = _truncate(detail_fr).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(safe_fr, styles["snippet"]))

            story.append(Spacer(1, 0.1 * inch))

    story.append(PageBreak())

    # =============================================
    # PAGE 4: SCORE BREAKDOWN
    # =============================================
    story.append(Paragraph("Score Breakdown", styles["section_header"]))
    story.append(Spacer(1, 0.15 * inch))

    breakdown_rows = [
        ("Component", "Score", "Max"),
        ("Brand in FR Search", str(breakdown.get("brand_in_fr_search", 0)), "30"),
        ("Rank Parity (EN/FR)", str(breakdown.get("rank_parity", 0)), "20"),
        ("Specs Preserved in FR", str(breakdown.get("specs_preserved", 0)), "20"),
        ("No Competitor Hijacking", str(breakdown.get("no_hijacking", 0)), "15"),
        ("Pricing Accurate", str(breakdown.get("pricing_accurate", 0)), "15"),
        ("TOTAL", str(score), "100"),
    ]

    # Build table with Paragraph cells for styling
    table_data = []
    for row_idx, row in enumerate(breakdown_rows):
        styled_row = []
        for col_idx, cell in enumerate(row):
            if row_idx == 0:
                styled_row.append(Paragraph(f"<b>{cell}</b>", styles["table_header"]))
            elif row_idx == len(breakdown_rows) - 1:
                # Total row
                clr = score_clr.hexval()
                styled_row.append(Paragraph(
                    f'<font color="{clr}"><b>{cell}</b></font>',
                    styles["table_cell"],
                ))
            else:
                # Data rows -- color the score column
                if col_idx == 1:
                    val = int(cell)
                    max_val = int(row[2])
                    ratio = val / max_val if max_val > 0 else 0
                    if ratio >= 0.7:
                        clr = GREEN_HEALTHY.hexval()
                    elif ratio >= 0.4:
                        clr = AMBER_WARNING.hexval()
                    else:
                        clr = RED_CRITICAL.hexval()
                    styled_row.append(Paragraph(
                        f'<font color="{clr}"><b>{cell}</b></font>',
                        styles["table_cell"],
                    ))
                else:
                    styled_row.append(Paragraph(cell, styles["table_cell"]))
        table_data.append(styled_row)

    col_widths = [3.5 * inch, 1.5 * inch, 1.5 * inch]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), DARK_ROW),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        # Alternating rows
        *[
            ("BACKGROUND", (0, i), (-1, i), DARK_ROW if i % 2 == 0 else DARK_ROW_ALT)
            for i in range(1, len(breakdown_rows))
        ],
        # Total row bottom border
        ("LINEABOVE", (0, -1), (-1, -1), 1.5, CYAN_ACCENT),
        # General padding
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        # Grid
        ("LINEBELOW", (0, 0), (-1, 0), 1, CYAN_ACCENT),
        ("LINEBELOW", (0, -1), (-1, -1), 1, CYAN_ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)

    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(
        "Each component reflects a distinct dimension of AI inference alignment. "
        "Scores are computed from live probe responses across multiple AI providers.",
        styles["body"],
    ))

    story.append(PageBreak())

    # =============================================
    # PAGE 5: RECOMMENDATIONS
    # =============================================
    story.append(Paragraph("Recommendations", styles["section_header"]))
    story.append(Spacer(1, 0.15 * inch))

    story.append(Paragraph(
        "Based on this audit, the following actions will improve your AI visibility:",
        styles["body"],
    ))
    story.append(Spacer(1, 0.1 * inch))

    recommendations = [
        (
            "Deploy MCP Feed",
            "Publish a machine-readable product feed (JSON-LD + MCP format) that AI crawlers "
            "can ingest directly. This is the single highest-impact action for AI visibility."
        ),
        (
            "Add JSON-LD Structured Data",
            "Ensure every product page includes Schema.org Product markup in both English and French. "
            "AI models rely heavily on structured data for factual grounding."
        ),
        (
            "Check robots.txt for AI Bot Blocks",
            "Review your robots.txt and verify that AI crawlers (GPTBot, ClaudeBot, PerplexityBot, "
            "Google-Extended) are not inadvertently blocked. Blocking these bots makes your brand invisible."
        ),
        (
            "Bilingual Content Parity",
            "Ensure French product descriptions, specifications, and category pages match the depth "
            "and detail of English content. AI models trained on thinner French corpora need stronger signals."
        ),
        (
            "Monitor and Re-Audit",
            "AI model knowledge refreshes on a 2-8 week cycle. Re-run this audit monthly to track "
            "score improvements and catch regressions."
        ),
    ]

    for idx, (title, desc) in enumerate(recommendations):
        num = idx + 1
        story.append(Paragraph(
            f'<font color="{CYAN_ACCENT.hexval()}"><b>{num}.</b></font> '
            f'<b>{title}</b>',
            styles["subsection"],
        ))
        story.append(Paragraph(desc, styles["body"]))
        story.append(Spacer(1, 0.05 * inch))

    story.append(Spacer(1, 0.5 * inch))

    # CTA
    cta_style = ParagraphStyle(
        "cta",
        parent=styles["body_bold"],
        fontSize=14,
        textColor=CYAN_ACCENT,
        alignment=TA_CENTER,
        spaceBefore=20,
    )
    story.append(Paragraph(
        "Contact VisiMind for implementation support",
        cta_style,
    ))
    story.append(Paragraph(
        "eng@visimind.ai | visimind.ai",
        ParagraphStyle("cta_email", parent=styles["cover_sub"], textColor=MID_GRAY),
    ))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "This report is confidential and intended for internal use by the recipient organization. "
        "Scores reflect AI model behavior at the time of audit and may change as models are updated.",
        styles["footer_note"],
    ))

    # Build
    doc.build(story, onFirstPage=_dark_bg_canvas, onLaterPages=_dark_bg_canvas)
    return buf.getvalue()
