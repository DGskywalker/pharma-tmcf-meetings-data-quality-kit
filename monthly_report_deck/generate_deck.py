"""
Executive PowerPoint Presentation Generator for Meridian BioPharma Global Operations
Builds an 8-slide, 16:9 executive briefing deck using python-pptx with embedded
charts, KPI cards, tables, and corporate styling.

[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

DECK_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(DECK_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data_quality")

# Load Audit Summary
with open(os.path.join(DATA_DIR, "dq_audit_summary.json"), "r") as f:
    AUDIT_DATA = json.load(f)

# Corporate Colors
NAVY = RGBColor(15, 23, 42)       # #0F172A
SLATE = RGBColor(30, 41, 59)     # #1E293B
MUTED = RGBColor(100, 116, 139)  # #64748B
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
CARD_BG = RGBColor(241, 245, 249) # #F1F5F9
WHITE = RGBColor(255, 255, 255)
TEAL = RGBColor(13, 148, 136)    # #0D9488
CYAN = RGBColor(6, 182, 212)     # #06B6D4
RED = RGBColor(225, 29, 72)      # #E11D48
AMBER = RGBColor(217, 119, 6)    # #D97706
BORDER_SLATE = RGBColor(203, 213, 225)


def add_header(slide, title_text, category_text="GLOBAL MEETINGS DATA QUALITY & GOVERNANCE COMMITTEE"):
    """Adds a standard executive header to a slide."""
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(9)
    p_cat.font.bold = True
    p_cat.font.color.rgb = TEAL

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY


def add_kpi_card(slide, left, top, width, height, title, value, subtext, val_color=NAVY):
    """Adds a styled metric card."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = BORDER_SLATE
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)

    p0 = tf.paragraphs[0]
    p0.text = title.upper()
    p0.font.name = "Arial"
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = MUTED
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = str(value)
    p1.font.name = "Arial"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = val_color
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = subtext
    p2.font.name = "Arial"
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = SLATE
    p2.alignment = PP_ALIGN.CENTER


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================
    # SLIDE 1: EXECUTIVE TITLE SLIDE (Dark Navy Premium Theme)
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Title Box
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "MERIDIAN BIOPHARMA GLOBAL OPERATIONS"
    p0.font.name = "Arial"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = CYAN

    p1 = tf1.add_paragraph()
    p1.text = "Meetings & Events Data Quality\n& Compliance Governance"
    p1.font.name = "Arial"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Monthly Performance Briefing & Data Leakage Point (DLP) Surveillance | Q3 2026"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    # Footer Metadata Box
    f_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(11.0), Inches(1.0))
    tf_f = f_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Operational Architecture: Cvent Enterprise SMM • SAP Concur • Amex BTA Virtual Cards • CMS Sunshine • EFPIA • Fleet ESG"
    p_f.font.name = "Arial"
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = RGBColor(100, 116, 139)

    p_f2 = tf_f.add_paragraph()
    p_f2.text = "[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]"
    p_f2.font.name = "Arial"
    p_f2.font.size = Pt(8.5)
    p_f2.font.bold = True
    p_f2.font.color.rgb = RGBColor(245, 158, 11)

    # ==========================================================
    # SLIDE 2: EXECUTIVE SCORECARD & PORTFOLIO HEALTH INDEX
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Scorecard: Data Accuracy & Regulatory Exposure")

    # 4 Top KPI Cards
    acc_pct = AUDIT_DATA["overall_accuracy_percentage"]
    tot_spend = AUDIT_DATA["total_expenditure_audited_usd"]
    crit_spend = AUDIT_DATA["critical_regulatory_exposure_spend_usd"]
    crit_pct = AUDIT_DATA["critical_spend_exposure_percentage"]
    flagged = AUDIT_DATA["flagged_records_count"]
    tot_recs = AUDIT_DATA["total_records_audited"]

    add_kpi_card(s2, Inches(0.8), Inches(1.5), Inches(2.75), Inches(1.5), "Portfolio Accuracy", f"{acc_pct}%", "Target: >= 95.0% (-16.9% Gap)", RED if acc_pct < 85 else TEAL)
    add_kpi_card(s2, Inches(3.75), Inches(1.5), Inches(2.75), Inches(1.5), "Audited Meeting Spend", f"${tot_spend/1e6:.1f}M", f"{tot_recs:,} Total Events Tracked", NAVY)
    add_kpi_card(s2, Inches(6.7), Inches(1.5), Inches(2.75), Inches(1.5), "Sunshine Spend Exposure", f"${crit_spend/1e6:.1f}M", f"{crit_pct:.1f}% Total Portfolio at Risk", RED)
    add_kpi_card(s2, Inches(9.65), Inches(1.5), Inches(2.85), Inches(1.5), "Flagged Deficiencies", f"{flagged} / {tot_recs}", f"{AUDIT_DATA['clean_records_count']} Clean Events", AMBER)

    # Executive Callout Card (Left)
    callout = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(5.7), Inches(3.6))
    callout.fill.solid()
    callout.fill.fore_color.rgb = WHITE
    callout.line.color.rgb = BORDER_SLATE
    c_tf = callout.text_frame
    c_tf.word_wrap = True
    c_tf.margin_left = c_tf.margin_top = c_tf.margin_right = c_tf.margin_bottom = Inches(0.25)

    cp0 = c_tf.paragraphs[0]
    cp0.text = "EXECUTIVE TAKEAWAYS & GOVERNANCE ALERT"
    cp0.font.name = "Arial"
    cp0.font.size = Pt(11)
    cp0.font.bold = True
    cp0.font.color.rgb = TEAL

    points = [
        ("Post-Event Roster Lags Represent 54% of Risk:", " 184 meetings failed to submit verified attendee rosters within the mandatory 14-day SLA, directly corrupting CMS Open Payments calculations."),
        ("Cvent SMM Bypass (DLP-1):", " 42 external HCP events were booked directly off-channel, completely circumventing corporate master contracts and aggregate spend tracking."),
        ("Virtual Card Unallocated Balances:", " $9.4M in BTA/Virtual card charges exceed 45-day reconciliation windows due to missing Cvent Level 3 transaction references."),
        ("Remediation Target:", " Implement automated Concur pre-booking hard stops and 7-day BU VP escalation nudges to reach 95% accuracy by Q4.")
    ]
    for b_title, b_desc in points:
        p = c_tf.add_paragraph()
        p.space_before = Pt(8)
        run_b = p.add_run()
        run_b.text = "• " + b_title
        run_b.font.name = "Arial"
        run_b.font.size = Pt(9.5)
        run_b.font.bold = True
        run_b.font.color.rgb = NAVY
        run_t = p.add_run()
        run_t.text = b_desc
        run_t.font.name = "Arial"
        run_t.font.size = Pt(9.5)
        run_t.font.color.rgb = SLATE

    # Right: Domain Radar Chart
    radar_img = os.path.join(ASSETS_DIR, "compliance_radar.png")
    if os.path.exists(radar_img):
        s2.shapes.add_picture(radar_img, Inches(6.8), Inches(3.2), Inches(5.7), Inches(3.6))

    # ==========================================================
    # SLIDE 3: PROCESS MAP & DATA LEAKAGE POINT (DLP) SURVEILLANCE
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "End-to-End Meeting Lifecycle & Data Leakage Point (DLP) Surveillance")

    # Left: Process Map Graphic
    map_img = os.path.join(ASSETS_DIR, "process_map_overview.png")
    if os.path.exists(map_img):
        s3.shapes.add_picture(map_img, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))

    # Right: DLP Breakdown Table Card
    r_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.5), Inches(4.7), Inches(5.3))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = CARD_BG
    r_card.line.color.rgb = BORDER_SLATE
    r_tf = r_card.text_frame
    r_tf.word_wrap = True
    r_tf.margin_left = r_tf.margin_top = r_tf.margin_right = r_tf.margin_bottom = Inches(0.2)

    rp0 = r_tf.paragraphs[0]
    rp0.text = "CRITICAL DATA LEAKAGE POINTS"
    rp0.font.name = "Arial"
    rp0.font.size = Pt(11)
    rp0.font.bold = True
    rp0.font.color.rgb = RED

    dlp_highlights = [
        ("DLP-1: Rogue Direct Booking", "Requester bypasses Cvent SMM intake; unmitigated cancellation terms ($35k-$150k exposure)."),
        ("DLP-2: HCP NPI / FMV Disconnect", "Missing 10-digit NPIs or unapproved honoraria tiers; Sunshine Act disclosure penalty risk."),
        ("DLP-3: Fleet Telematics Blindspot", "Ground executive sedans booked off-contract with zero passenger manifests or Scope 3 CO2 tracking."),
        ("DLP-4: Virtual Card Orphan Charges", "Hotel master folios charged without Cvent Meeting ID reference; 60+ day unallocated AP."),
        ("DLP-5: Post-Event Roster Leakage", "Delayed actual attendee sign-in uploads; no-shows falsely reported as receiving transfer-of-value."),
        ("DLP-6: Financial WBS Desync", "Expenses coded to generic departmental cost center instead of clinical trial WBS code."),
        ("DLP-7: Cross-Border Regulatory Omission", "Foreign HCP invited without bilateral affiliate compliance clearance.")
    ]

    for d_title, d_desc in dlp_highlights:
        dp = r_tf.add_paragraph()
        dp.space_before = Pt(6)
        r_b = dp.add_run()
        r_b.text = d_title + ": "
        r_b.font.name = "Arial"
        r_b.font.size = Pt(8.5)
        r_b.font.bold = True
        r_b.font.color.rgb = NAVY
        r_t = dp.add_run()
        r_t.text = d_desc
        r_t.font.name = "Arial"
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = SLATE

    # ==========================================================
    # SLIDE 4: MEETINGS & EVENTS (CVENT SMM) DEEP DIVE: ROSTER CRISIS
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Strategic Meetings (Cvent SMM): The 14-Day Attendee Roster Challenge")

    # Left: Roster Aging Chart
    roster_img = os.path.join(ASSETS_DIR, "roster_aging.png")
    if os.path.exists(roster_img):
        s4.shapes.add_picture(roster_img, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))

    # Right: Analysis & Compliance Implications
    s4_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.3))
    s4_card.fill.solid()
    s4_card.fill.fore_color.rgb = WHITE
    s4_card.line.color.rgb = BORDER_SLATE
    s4_tf = s4_card.text_frame
    s4_tf.word_wrap = True
    s4_tf.margin_left = s4_tf.margin_top = s4_tf.margin_right = s4_tf.margin_bottom = Inches(0.25)

    s4_p0 = s4_tf.paragraphs[0]
    s4_p0.text = "ROSTER DEFICIENCY ROOT CAUSE ANALYSIS"
    s4_p0.font.name = "Arial"
    s4_p0.font.size = Pt(11)
    s4_p0.font.bold = True
    s4_p0.font.color.rgb = TEAL

    s4_points = [
        ("The 'Ghost Physician' Transfer of Value Risk:", " When organizers fail to upload physical sign-in sheets, the system defaults to the preliminary RSVP list. Physicians who canceled last minute are mistakenly credited with meal and room allocations in CMS Open Payments filings."),
        ("Physician Dispute Exposure:", " Physicians frequently dispute false transfer-of-value records during the 45-day CMS dispute review window, triggering costly legal audits and reputational friction."),
        ("Root Cause Behavior:", " Requesters treat meeting execution as the final step; post-event closeout is deprioritized once the symposium ends."),
        ("Mandatory Remediation Protocol:", " Automated Day +7 alert to meeting lead; Day +14 notice flagging meeting as DELINQUENT; Day +21 automated block on organizer corporate card privileges until roster sign-off.")
    ]
    for b_title, b_desc in s4_points:
        p = s4_tf.add_paragraph()
        p.space_before = Pt(10)
        rb = p.add_run()
        rb.text = "• " + b_title
        rb.font.name = "Arial"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = NAVY
        rt = p.add_run()
        rt.text = b_desc
        rt.font.name = "Arial"
        rt.font.size = Pt(9.5)
        rt.font.color.rgb = SLATE

    # ==========================================================
    # SLIDE 5: CORPORATE CARD & VIRTUAL PAYMENT RECONCILIATION
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Corporate Payment & Card Reconciliation: Clearing Aged Balances")

    # 3 Top Stat Cards for Card
    add_kpi_card(s5, Inches(0.8), Inches(1.5), Inches(3.6), Inches(1.4), "Virtual Card Share", "45.0% ($101.0M)", "Preferred Hotel Master Folio Gateway", TEAL)
    add_kpi_card(s5, Inches(4.7), Inches(1.5), Inches(3.6), Inches(1.4), "Amex BTA Ghost Spend", "30.0% ($67.3M)", "Centralized Air & Group Rail Charges", NAVY)
    add_kpi_card(s5, Inches(8.6), Inches(1.5), Inches(3.9), Inches(1.4), "Aged Unreconciled AP (>45d)", "$9.4M (38 Events)", "Requires Manual General Ledger Matching", RED)

    # Left Container: Payment Method Integrity Table
    tbl_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.1), Inches(5.8), Inches(3.8))
    tbl_card.fill.solid()
    tbl_card.fill.fore_color.rgb = WHITE
    tbl_card.line.color.rgb = BORDER_SLATE
    t_tf = tbl_card.text_frame
    t_tf.word_wrap = True
    t_tf.margin_left = t_tf.margin_top = t_tf.margin_right = t_tf.margin_bottom = Inches(0.2)

    tp = t_tf.paragraphs[0]
    tp.text = "PAYMENT METHOD INTEGRITY & RECONCILIATION SPEED"
    tp.font.name = "Arial"
    tp.font.size = Pt(10)
    tp.font.bold = True
    tp.font.color.rgb = TEAL

    pay_data = [
        ("Single-Use Virtual Card", "92.4%", "12 Days", "Lowest orphan risk; exact budget pre-funded."),
        ("Amex BTA Ghost Card", "74.8%", "48 Days", "Vulnerable to generic hotel merchant descriptors."),
        ("Corporate T&E Card", "81.2%", "29 Days", "Employee out-of-pocket report lag in Concur."),
        ("Direct Invoice PO", "88.0%", "34 Days", "Heavy procurement PO cross-charging overhead.")
    ]
    for m_name, m_rate, m_time, m_note in pay_data:
        p = t_tf.add_paragraph()
        p.space_before = Pt(8)
        rb = p.add_run()
        rb.text = f"{m_name} (Recon Rate: {m_rate} | Avg Lag: {m_time})\n"
        rb.font.name = "Arial"
        rb.font.size = Pt(9)
        rb.font.bold = True
        rb.font.color.rgb = NAVY
        rt = p.add_run()
        rt.text = f"  -> {m_note}"
        rt.font.name = "Arial"
        rt.font.size = Pt(8.5)
        rt.font.color.rgb = MUTED

    # Right Container: Level 3 Merchant Interchange Solution
    r_card2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.1), Inches(5.6), Inches(3.8))
    r_card2.fill.solid()
    r_card2.fill.fore_color.rgb = CARD_BG
    r_card2.line.color.rgb = BORDER_SLATE
    r2_tf = r_card2.text_frame
    r2_tf.word_wrap = True
    r2_tf.margin_left = r2_tf.margin_top = r2_tf.margin_right = r2_tf.margin_bottom = Inches(0.25)

    r2_p = r2_tf.paragraphs[0]
    r2_p.text = "LEVEL 3 MERCHANT DATA REMEDIATION"
    r2_p.font.name = "Arial"
    r2_p.font.size = Pt(10.5)
    r2_p.font.bold = True
    r2_p.font.color.rgb = NAVY

    r2_points = [
        ("The 'Hotel Restaurant Co' Descriptor Problem:", " Hotels bill Banquet Event Orders (BEOs) under local merchant entity names without passing Cvent Meeting IDs, breaking automated Concur match rules."),
        ("Mandatory Master Folio Protocol:", " Mandate that hotel contracts enforce Level 3 interchange fields containing Cvent Meeting ID (`CVT-XXXXXX`) in field 43."),
        ("Direct Concur API Integration:", " Deploy automatic Concur-to-Cvent nightly synchronization to ingest itemized hotel folios directly into event expense lines.")
    ]
    for b_t, b_d in r2_points:
        p = r2_tf.add_paragraph()
        p.space_before = Pt(10)
        rb = p.add_run()
        rb.text = "• " + b_t
        rb.font.name = "Arial"
        rb.font.size = Pt(9)
        rb.font.bold = True
        rb.font.color.rgb = NAVY
        rt = p.add_run()
        rt.text = b_d
        rt.font.name = "Arial"
        rt.font.size = Pt(9)
        rt.font.color.rgb = SLATE

    # ==========================================================
    # SLIDE 6: HEALTHCARE COMPLIANCE & BUSINESS UNIT PERFORMANCE
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Healthcare Compliance & Business Unit Exposure Breakdown")

    # Left: BU Chart
    bu_img = os.path.join(ASSETS_DIR, "accuracy_by_bu.png")
    if os.path.exists(bu_img):
        s6.shapes.add_picture(bu_img, Inches(0.8), Inches(1.5), Inches(6.2), Inches(5.3))

    # Right: Compliance Dimensions Table & Analysis
    s6_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(1.5), Inches(5.2), Inches(5.3))
    s6_card.fill.solid()
    s6_card.fill.fore_color.rgb = WHITE
    s6_card.line.color.rgb = BORDER_SLATE
    s6_tf = s6_card.text_frame
    s6_tf.word_wrap = True
    s6_tf.margin_left = s6_tf.margin_top = s6_tf.margin_right = s6_tf.margin_bottom = Inches(0.25)

    s6_p = s6_tf.paragraphs[0]
    s6_p.text = "REGULATORY JURISDICTION SURVEILLANCE"
    s6_p.font.name = "Arial"
    s6_p.font.size = Pt(11)
    s6_p.font.bold = True
    s6_p.font.color.rgb = RED

    comp_items = [
        ("US CMS Open Payments (Sunshine Act):", " 91.2% NPI completeness across US HCP meetings. 24 events flagged for missing NPI numbers prior to final attestation filing."),
        ("EFPIA Transparency Code (Europe):", " 34 cross-border HCP sponsorships lacked bilateral affiliate notifications, creating statutory disclosure deficiencies in UK, France, and Germany."),
        ("Fair Market Value (FMV) Tier Governance:", " 28 speaker agreements executed with fee amounts outside standard tier guidelines without documented Medical Compliance exception sign-off."),
        ("Business Unit Performance Ranking:", " Oncology achieved highest compliance (81.4% accuracy), while Vaccines/Infectious logged greatest roster lag (74.8% accuracy).")
    ]
    for b_t, b_d in comp_items:
        p = s6_tf.add_paragraph()
        p.space_before = Pt(8)
        rb = p.add_run()
        rb.text = "• " + b_t
        rb.font.name = "Arial"
        rb.font.size = Pt(9)
        rb.font.bold = True
        rb.font.color.rgb = NAVY
        rt = p.add_run()
        rt.text = b_d
        rt.font.name = "Arial"
        rt.font.size = Pt(9)
        rt.font.color.rgb = SLATE

    # ==========================================================
    # SLIDE 7: ROOT CAUSE PARETO & DATA DEFICIENCIES
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Root Cause Pareto Analysis: Top 8 Data Quality Deficiencies")

    # Left: Pareto Chart
    dlp_img = os.path.join(ASSETS_DIR, "dlp_breakdown.png")
    if os.path.exists(dlp_img):
        s7.shapes.add_picture(dlp_img, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))

    # Right: Deficiencies Breakdown Card
    s7_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.5), Inches(4.7), Inches(5.3))
    s7_card.fill.solid()
    s7_card.fill.fore_color.rgb = CARD_BG
    s7_card.line.color.rgb = BORDER_SLATE
    s7_tf = s7_card.text_frame
    s7_tf.word_wrap = True
    s7_tf.margin_left = s7_tf.margin_top = s7_tf.margin_right = s7_tf.margin_bottom = Inches(0.2)

    s7_p = s7_tf.paragraphs[0]
    s7_p.text = "CRITICAL PARETO INSIGHTS"
    s7_p.font.name = "Arial"
    s7_p.font.size = Pt(11)
    s7_p.font.bold = True
    s7_p.font.color.rgb = NAVY

    p_insights = [
        ("80/20 Concentration:", " 3 failure modes (Roster Lag, Missing NPIs, and Aged Card Reconciliation) account for 78% of all portfolio data quality errors."),
        ("Regulatory Multiplier:", " Although Fleet CO2 omissions represent 2.8% of errors, Roster Lags represent 12.3% of records and directly threaten federal certification."),
        ("Interdependent Failures:", " When a meeting lacks a Cvent ID (DLP-1), it systematically triggers downstream failures in Concur expense binding and Sunshine reporting."),
        ("Pre-Event Prevention:", " 65% of all flagged errors can be systematically prevented at the Cvent intake stage through form validation gating.")
    ]
    for b_t, b_d in p_insights:
        p = s7_tf.add_paragraph()
        p.space_before = Pt(8)
        rb = p.add_run()
        rb.text = "• " + b_t
        rb.font.name = "Arial"
        rb.font.size = Pt(9)
        rb.font.bold = True
        rb.font.color.rgb = NAVY
        rt = p.add_run()
        rt.text = b_d
        rt.font.name = "Arial"
        rt.font.size = Pt(9)
        rt.font.color.rgb = SLATE

    # ==========================================================
    # SLIDE 8: 90-DAY REMEDIATION ROADMAP & ACTION PLAN
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "90-Day Remediation Roadmap & Stakeholder Action Plan")

    # 3 Strategic Pillars (Columns)
    pillars = [
        ("PHASE 1: DAYS 1 - 30", "IMMEDIATE SYSTEM GATING", TEAL, [
            "Implement 'No Cvent ID, No Payment' hard stop in SAP Concur & Virtual Card portal.",
            "Deploy real-time CMS NPPES API check in Cvent registration to validate 10-digit NPIs at input.",
            "Freeze corporate card privileges for organizers with rosters delinquent >30 days."
        ]),
        ("PHASE 2: DAYS 31 - 60", "AUTOMATION & ESCALATION", CYAN, [
            "Launch automated Day +7 and Day +14 email nudges to meeting organizers and BU VPs.",
            "Mandate Level 3 Merchant Interchange standard on all Master Hotel vendor agreements.",
            "Deploy automated Concur-to-Cvent nightly synchronization to eliminate manual expense linking."
        ]),
        ("PHASE 3: DAYS 61 - 90", "ANALYTICS & GOVERNANCE", NAVY, [
            "Connect live Snowflake Transparency Data Lake with automated anomaly alert webhooks.",
            "Implement ground fleet API hook with Amex GBT for automated Scope 3 CO2 telemetry.",
            "Achieve enterprise portfolio accuracy milestone of >= 95.0% across all 4 Business Units."
        ])
    ]

    for idx, (p_phase, p_title, p_col, p_steps) in enumerate(pillars):
        left_pos = Inches(0.8 + idx * 4.0)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), Inches(3.7), Inches(5.3))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_SLATE
        
        c_tf = card.text_frame
        c_tf.word_wrap = True
        c_tf.margin_left = c_tf.margin_top = c_tf.margin_right = c_tf.margin_bottom = Inches(0.25)

        p0 = c_tf.paragraphs[0]
        p0.text = p_phase
        p0.font.name = "Arial"
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = p_col

        p1 = c_tf.add_paragraph()
        p1.text = p_title
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(4)

        for step in p_steps:
            ps = c_tf.add_paragraph()
            ps.space_before = Pt(12)
            r_dot = ps.add_run()
            r_dot.text = "- "
            r_dot.font.name = "Arial"
            r_dot.font.size = Pt(10)
            r_dot.font.bold = True
            r_dot.font.color.rgb = p_col
            r_txt = ps.add_run()
            r_txt.text = step
            r_txt.font.name = "Arial"
            r_txt.font.size = Pt(9.5)
            r_txt.font.color.rgb = SLATE

    # Save Presentation
    out_pptx_path = os.path.join(DECK_DIR, "Global_Meetings_Data_Quality_Executive_Deck.pptx")
    prs.save(out_pptx_path)
    print(f"Generated Executive PowerPoint Deck: {out_pptx_path}")
    return out_pptx_path


if __name__ == "__main__":
    build_deck()
