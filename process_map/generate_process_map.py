"""
Process Map Generator for Meridian BioPharma Global Operations
Generates:
1. meetings_events_lifecycle.drawio (Native Draw.io / diagrams.net XML)
2. meetings_events_lifecycle.svg (High-resolution interactive SVG)
3. data_leakage_points_matrix.json (Structured DLP Failure Mode Registry)
4. PROCESS_SPECIFICATION.md (Enterprise Standard Operating Procedure & FMEA)

[CONFIDENTIAL - MERIDIAN BIOPHARMA SIMULATION - 100% SYNTHETIC DATA]
"""

import json
import os
import xml.etree.ElementTree as ET

PROCESS_DIR = os.path.dirname(os.path.abspath(__file__))

# Structured Data Leakage Points (DLPs)
DLP_DATA = [
    {
        "id": "DLP-1",
        "name": "Off-Channel / Rogue Booking",
        "stage": "Meeting Intake & Initiation",
        "system_boundary": "Requester -> Direct Venue",
        "root_cause": "Requester bypasses Cvent SMM intake to book hotel/venue directly via phone or personal card to avoid procurement lead time.",
        "missing_data": ["Cvent Meeting ID", "Master Service Agreement (MSA)", "Negotiated Cancellation Terms", "Initial Budget Approval"],
        "downstream_impact": "Invisible spend ($35K-$150K), unmitigated cancellation liability, zero duty of care tracking for attendees.",
        "severity": "CRITICAL",
        "compliance_risk": "High (Anti-Kickback, Unapproved venue amenity risks)",
        "detection_rule": "Concur hotel expense > $1,000 without linked Cvent Meeting ID",
        "remediation_sla": "Immediate freeze on reimbursement; retroactive intake required within 48h."
    },
    {
        "id": "DLP-2",
        "name": "HCP Identity & FMV Tier Disconnect",
        "stage": "Compliance Pre-Clearance & Registration",
        "system_boundary": "Cvent <-> Veeva CRM / Sunshine Registry",
        "root_cause": "HCP attendee registered with nickname or personal Gmail; missing 10-digit NPI (US) or National Tax/Medical Council ID (EU).",
        "missing_data": ["National Provider Identifier (NPI)", "Fair Market Value (FMV) Tier Approval", "State Medical License #", "Cross-Border Approval ID"],
        "downstream_impact": "Inability to aggregate Transfer of Value (ToV); mandatory CMS Open Payments / EFPIA disclosure failures.",
        "severity": "CRITICAL",
        "compliance_risk": "Extreme (Statutory fines up to $1,000,000 under US Sunshine Act for knowing failure)",
        "detection_rule": "HCP_Attendees_Count > 0 AND (HCP_NPI_Numbers IS BLANK OR FMV_Tier_Compliant = 'N')",
        "remediation_sla": "Speaker contract paused until NPI is verified in CMS NPPES database."
    },
    {
        "id": "DLP-3",
        "name": "Ground Fleet & Scope 3 Telematics Blindspot",
        "stage": "Travel & Logistics Booking",
        "system_boundary": "TMC (Amex GBT) <-> Local Ground Suppliers",
        "root_cause": "Airport transfers, VIP sedans, or group coaches booked via unvetted local vendors without corporate fleet telematics integration.",
        "missing_data": ["Fleet Booking Confirmation", "Passenger Manifest", "Vehicle Powertrain / EV Flag", "Distance (km) & CO2e (kg)"],
        "downstream_impact": "Duty of care failure during traveler transit; incomplete Scope 3 Category 6 (Business Travel) ESG sustainability filings.",
        "severity": "MEDIUM",
        "compliance_risk": "Moderate (CSRD / ESG reporting gaps, traveler safety liability)",
        "detection_rule": "Fleet_Ground_Transfer_Utilized = 'Y' AND Fleet_CO2_Emissions_kg IS NULL",
        "remediation_sla": "Automated monthly fleet partner vendor reconciliation."
    },
    {
        "id": "DLP-4",
        "name": "Virtual Card / BTA Master Folio Orphan Charges",
        "stage": "Payment & Master Folio Billing",
        "system_boundary": "Hotel Merchant <-> Banking Gateway (Amex BTA / Virtual Card)",
        "root_cause": "Hotel front desk charges master account with generic descriptor (e.g. 'HOTEL REST CO') without passing Cvent Meeting ID in Card Level 3 data.",
        "missing_data": ["Level 3 Merchant Data", "Cvent Meeting ID Reference", "Itemized Banquet Event Order (BEO)", "Tax / VAT Breakdown"],
        "downstream_impact": "Aged unallocated card balances (60-120 days); manual accounting overhead; risk of duplicate payment via direct invoice.",
        "severity": "HIGH",
        "compliance_risk": "High (Financial audit restatement risk, SOX 404 internal control deficiency)",
        "detection_rule": "Payment_Method IN ('Amex_BTA_Ghost', 'Single_Use_Virtual_Card') AND Corporate_Card_Reconciled_Flag = 'N' AND Days_Since_Event > 30",
        "remediation_sla": "Virtual card automated push notification to hotel finance within 72h."
    },
    {
        "id": "DLP-5",
        "name": "Post-Event Attendee Roster Leakage",
        "stage": "Event Closeout & Actual Spend Allocation",
        "system_boundary": "On-Site Badge Scan / Sign-In <-> Cvent SMM",
        "root_cause": "Meeting organizer fails to upload verified physical/virtual sign-in sheet within 14 calendar days; no-shows remain unadjusted.",
        "missing_data": ["Verified Physical Attendance Sheet", "No-Show / Cancellation Flags", "Per-Capita F&B Actual Spend", "HCP Sign-Off Signatures"],
        "downstream_impact": "Per-capita F&B allocated to no-show HCPs results in false Sunshine Act reporting or under-reporting for attending HCPs.",
        "severity": "CRITICAL",
        "compliance_risk": "Extreme (False Claims Act exposure, reputational damage, physician dispute disputes)",
        "detection_rule": "Post_Event_Roster_Captured = 'N' AND Days_To_Roster_Submission > 14",
        "remediation_sla": "Automatic weekly escalation to BU Vice President and temporary block on future meeting approvals."
    },
    {
        "id": "DLP-6",
        "name": "Cross-System Financial Code Desync",
        "stage": "Expense Reporting & ERP Posting",
        "system_boundary": "SAP Concur <-> SAP S/4HANA ERP",
        "root_cause": "Meeting expenses filed under operational Cost Center instead of clinical trial WBS code, breaking project ledger reconciliation.",
        "missing_data": ["WBS Code Validation", "Cost Center Cross-Charge Approval", "Internal Order Number"],
        "downstream_impact": "Misstated clinical trial trial budgets; distorted departmental variance reports; manual GL journal adjustments.",
        "severity": "HIGH",
        "compliance_risk": "Moderate (Internal managerial accounting distortions)",
        "detection_rule": "WBS_Code IS BLANK OR Cost_Center DOES NOT MATCH Requester Department Profile",
        "remediation_sla": "Automated Concur pre-submission validation rule blocking expense report submission."
    },
    {
        "id": "DLP-7",
        "name": "Cross-Border Regulatory Disclosure Omission",
        "stage": "HCP Engagement & Travel Crossing",
        "system_boundary": "Origin Affiliate <-> Host Affiliate Compliance Office",
        "root_cause": "European or Japanese HCP brought into US symposium without cross-border notification to home affiliate compliance officer.",
        "missing_data": ["Cross-Border Notification Form (CBNF)", "Home Country Data Privacy Consent", "Withholding Tax Certificate"],
        "downstream_impact": "Breach of EFPIA cross-border disclosure provisions; local tax authority withholding penalties.",
        "severity": "HIGH",
        "compliance_risk": "High (Cross-border European data privacy and EFPIA code infringement)",
        "detection_rule": "Cross_Border_HCP_Flag = 'Y' AND Compliance_Approval_Status != 'Approved'",
        "remediation_sla": "Automated lock on airline ticketing until Cross-Border clearance token is issued."
    }
]


def generate_drawio_xml():
    """Generates standard Draw.io / diagrams.net XML file."""
    root = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-18T10:00:00.000Z", agent="MeridianGlobal/2.0", version="24.0.0", type="device")
    diagram = ET.SubElement(root, "diagram", id="meridian_meetings_lifecycle", name="Global Meetings Lifecycle & Data Leakage Map")
    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1920", pageHeight="1080", math="0", shadow="0")
    root_cell = ET.SubElement(mxGraphModel, "root")
    
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    # Background Header Banner
    header = ET.SubElement(root_cell, "mxCell", id="hdr_1", value="<b>MERIDIAN BIOPHARMA GLOBAL OPERATIONS | STRATEGIC MEETINGS & EVENTS DATA LIFECYCLE</b><br/><font color='#64748B'>End-to-End Governance Architecture & Critical Data Leakage Point (DLP) Matrix | [SYNTHETIC DEMO PURPOSES ONLY]</font>", style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#1E293B;fontColor=#F8FAFC;fontSize=15;align=center;", vertex="1", parent="1")
    header_geo = ET.SubElement(header, "mxGeometry", attrib={"x": "40", "y": "20", "width": "1840", "height": "60", "as": "geometry"})

    # Swimlanes definition
    swimlanes = [
        {"id": "lane_req", "y": 90, "h": 140, "name": "1. REQUESTER & BUSINESS UNIT (Commercial / Medical Affairs)", "color": "#1E293B", "fontColor": "#38BDF8"},
        {"id": "lane_comp", "y": 240, "h": 140, "name": "2. MEDICAL COMPLIANCE & LEGAL (FMV / Sunshine / Transparency)", "color": "#1E293B", "fontColor": "#A78BFA"},
        {"id": "lane_smm", "y": 390, "h": 140, "name": "3. SMM ENTERPRISE ENGINE (Cvent Enterprise / Intake)", "color": "#1E293B", "fontColor": "#34D399"},
        {"id": "lane_tmc", "y": 540, "h": 140, "name": "4. TRAVEL & LOGISTICS (Corporate Travel & Ground Fleet)", "color": "#1E293B", "fontColor": "#FBBF24"},
        {"id": "lane_card", "y": 690, "h": 140, "name": "5. PAYMENT & EXPENSE RECONCILIATION (Virtual Card / SAP Concur)", "color": "#1E293B", "fontColor": "#F472B6"},
        {"id": "lane_erp", "y": 840, "h": 150, "name": "6. ERP & AGGREGATE SPEND LAKE (SAP S/4HANA / CMS Sunshine / EFPIA)", "color": "#1E293B", "fontColor": "#FB7185"},
    ]

    for lane in swimlanes:
        cell = ET.SubElement(root_cell, "mxCell", id=lane["id"], value=f"<b>{lane['name']}</b>", style=f"swimlane;horizontal=0;whiteSpace=wrap;html=1;fillColor={lane['color']};strokeColor=#334155;fontColor={lane['fontColor']};fontSize=11;startSize=30;", vertex="1", parent="1")
        geo = ET.SubElement(cell, "mxGeometry", attrib={"x": "40", "y": str(lane["y"]), "width": "1840", "height": str(lane["h"]), "as": "geometry"})

    # Add Process Nodes
    nodes = [
        # Requester lane
        {"id": "n1", "lane": "1", "x": 100, "y": 120, "w": 180, "h": 70, "label": "<b>Meeting Initiation</b><br/>Define Purpose, Budget,<br/>Target Dates & Cost Center", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#1E3A8A;strokeColor=#3B82F6;fontColor=#FFFFFF;"},
        {"id": "n7", "lane": "1", "x": 1060, "y": 120, "w": 180, "h": 70, "label": "<b>Event Execution</b><br/>Host Symposium & Manage<br/>Physical/Virtual Attendees", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#1E3A8A;strokeColor=#3B82F6;fontColor=#FFFFFF;"},
        {"id": "n8", "lane": "1", "x": 1290, "y": 120, "w": 190, "h": 70, "label": "<b>Post-Event Closeout</b><br/>Collect Actual Sign-In<br/>Roster & Reconcile No-Shows", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#1E3A8A;strokeColor=#3B82F6;fontColor=#FFFFFF;"},
        
        # Compliance lane
        {"id": "n2", "lane": "1", "x": 330, "y": 270, "w": 190, "h": 70, "label": "<b>Compliance Review</b><br/>FMV Honoraria Tiering,<br/>Anti-Kickback & Cross-Border", "style": "rhombus;whiteSpace=wrap;html=1;fillColor=#4C1D95;strokeColor=#8B5CF6;fontColor=#FFFFFF;"},
        {"id": "n12", "lane": "1", "x": 1690, "y": 270, "w": 170, "h": 70, "label": "<b>Sunshine / EFPIA Audit</b><br/>Final Attestation &<br/>Regulatory Sign-Off", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#4C1D95;strokeColor=#8B5CF6;fontColor=#FFFFFF;"},

        # SMM lane
        {"id": "n3", "lane": "1", "x": 570, "y": 420, "w": 190, "h": 70, "label": "<b>Cvent SMM Setup</b><br/>Issue Meeting ID, Configure<br/>Registration & NPI Validation", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;fontColor=#FFFFFF;"},
        {"id": "n4", "lane": "1", "x": 810, "y": 420, "w": 190, "h": 70, "label": "<b>HCP Registration</b><br/>Capture 10-Digit NPI, Tax ID,<br/>Dietary & Flight Requests", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;fontColor=#FFFFFF;"},

        # Travel & Fleet lane
        {"id": "n5", "lane": "1", "x": 810, "y": 570, "w": 190, "h": 70, "label": "<b>Corporate Travel Ticketing</b><br/>Air, Rail, Hotel Room Block<br/>via Amex GBT Profile", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#78350F;strokeColor=#F59E0B;fontColor=#FFFFFF;"},
        {"id": "n6", "lane": "1", "x": 1060, "y": 570, "w": 190, "h": 70, "label": "<b>Ground Fleet Dispatch</b><br/>Executive Shuttles & EVs,<br/>Telematics CO2e Logging", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#78350F;strokeColor=#F59E0B;fontColor=#FFFFFF;"},

        # Payment & Card lane
        {"id": "n9", "lane": "1", "x": 570, "y": 720, "w": 190, "h": 70, "label": "<b>Virtual Card Issuance</b><br/>Generate Single-Use Card<br/>Tied to Cvent Meeting ID", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#831843;strokeColor=#EC4899;fontColor=#FFFFFF;"},
        {"id": "n10", "lane": "1", "x": 1290, "y": 720, "w": 190, "h": 70, "label": "<b>SAP Concur Expense</b><br/>Itemized BEO Folio Matching<br/>& Out-of-Pocket Reports", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#831843;strokeColor=#EC4899;fontColor=#FFFFFF;"},

        # ERP lane
        {"id": "n11", "lane": "1", "x": 1510, "y": 870, "w": 180, "h": 70, "label": "<b>SAP S/4HANA Posting</b><br/>Settle to WBS / Cost Center,<br/>Clear Virtual Card AP", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#881337;strokeColor=#F43F5E;fontColor=#FFFFFF;"},
        {"id": "n13", "lane": "1", "x": 1710, "y": 870, "w": 150, "h": 70, "label": "<b>Snowflake Agg Spend</b><br/>Publish US CMS & EFPIA<br/>Tax Compliance Feeds", "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#881337;strokeColor=#F43F5E;fontColor=#FFFFFF;"},
    ]

    for n in nodes:
        cell = ET.SubElement(root_cell, "mxCell", id=n["id"], value=n["label"], style=n["style"], vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", attrib={"x": str(n["x"]), "y": str(n["y"]), "width": str(n["w"]), "height": str(n["h"]), "as": "geometry"})

    # Add Data Leakage Points (Alert Badges without emojis)
    dlp_nodes = [
        {"id": "dlp1", "x": 190, "y": 85, "label": "<b>DLP-1: Rogue Booking</b><br/>Hotel direct booking;<br/>bypasses Cvent & SMM controls.", "color": "#7F1D1D", "border": "#EF4444"},
        {"id": "dlp2", "x": 420, "y": 350, "label": "<b>DLP-2: HCP NPI / FMV Disconnect</b><br/>Missing 10-digit NPI or FMV tier;<br/>Sunshine Act non-disclosure risk.", "color": "#7F1D1D", "border": "#EF4444"},
        {"id": "dlp7", "x": 480, "y": 200, "label": "<b>DLP-7: Cross-Border Omission</b><br/>Foreign HCP invited without<br/>destination affiliate clearance.", "color": "#7F1D1D", "border": "#EF4444"},
        {"id": "dlp3", "x": 950, "y": 645, "label": "<b>DLP-3: Fleet Telematics Blindspot</b><br/>Unvetted local taxi/shuttle;<br/>missing Scope 3 CO2 & duty of care.", "color": "#7F1D1D", "border": "#EF4444"},
        {"id": "dlp4", "x": 670, "y": 795, "label": "<b>DLP-4: Virtual Card Orphan Charges</b><br/>Hotel charges master folio without<br/>Meeting ID; aged unallocated AP.", "color": "#7F1D1D", "border": "#EF4444"},
        {"id": "dlp5", "x": 1380, "y": 85, "label": "<b>DLP-5: Post-Event Roster Leakage</b><br/>Sign-in sheet delayed >14 days;<br/>distorts per-capita HCP spend.", "color": "#7F1D1D", "border": "#EF4444"},
        {"id": "dlp6", "x": 1390, "y": 795, "label": "<b>DLP-6: Financial WBS Code Desync</b><br/>Expenses misallocated to BU overhead<br/>instead of Clinical Trial WBS.", "color": "#7F1D1D", "border": "#EF4444"}
    ]

    for dlp in dlp_nodes:
        cell = ET.SubElement(root_cell, "mxCell", id=dlp["id"], value=dlp["label"], style=f"rounded=1;whiteSpace=wrap;html=1;fillColor={dlp['color']};strokeColor={dlp['border']};strokeWidth=2;fontColor=#FEF2F2;fontSize=10;align=center;", vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", attrib={"x": str(dlp["x"]), "y": str(dlp["y"]), "width": "200", "height": "55", "as": "geometry"})

    # Connectors
    edges = [
        ("e1", "n1", "n2", "Submit for Approval"),
        ("e2", "n2", "n3", "Approved -> Create SMM"),
        ("e3", "n3", "n9", "Trigger Virtual Card"),
        ("e4", "n3", "n4", "Open Registration"),
        ("e5", "n4", "n5", "HCP Book Travel"),
        ("e6", "n5", "n6", "Ground Transport"),
        ("e7", "n4", "n7", "Travelers Arrive"),
        ("e8", "n7", "n8", "Event Concluded"),
        ("e9", "n8", "n10", "Submit Verified Roster"),
        ("e10", "n9", "n10", "Master Folio Billed"),
        ("e11", "n10", "n11", "Audit Approved Expense"),
        ("e12", "n11", "n13", "Ingest ERP General Ledger"),
        ("e13", "n13", "n12", "Generate CMS/EFPIA Filings"),
    ]

    for eid, src, tgt, elabel in edges:
        edge = ET.SubElement(root_cell, "mxCell", id=eid, value=elabel, style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#94A3B8;strokeWidth=2;fontColor=#CBD5E1;fontSize=9;", edge="1", parent="1", source=src, target=tgt)
        ET.SubElement(edge, "mxGeometry", attrib={"relative": "1", "as": "geometry"})

    # Write XML
    xml_str = ET.tostring(root, encoding="utf-8")
    drawio_path = os.path.join(PROCESS_DIR, "meetings_events_lifecycle.drawio")
    with open(drawio_path, "wb") as f:
        f.write(xml_str)
    print(f"Generated Draw.io XML: {drawio_path}")


def generate_svg():
    """Generates a standalone crisp SVG vector map of the end-to-end lifecycle."""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#090D16; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="50%" stop-color="#1E293B" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <linearGradient id="reqGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E3A8A" />
      <stop offset="100%" stop-color="#172554" />
    </linearGradient>
    <linearGradient id="compGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#581C87" />
      <stop offset="100%" stop-color="#3B0764" />
    </linearGradient>
    <linearGradient id="smmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#065F46" />
      <stop offset="100%" stop-color="#022C22" />
    </linearGradient>
    <linearGradient id="tmcGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#92400E" />
      <stop offset="100%" stop-color="#451A03" />
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9D174D" />
      <stop offset="100%" stop-color="#500724" />
    </linearGradient>
    <linearGradient id="erpGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#881337" />
      <stop offset="100%" stop-color="#4C0519" />
    </linearGradient>
    <linearGradient id="dlpGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#DC2626" />
      <stop offset="100%" stop-color="#7F1D1D" />
    </linearGradient>

    <filter id="dropShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <filter id="glowRed" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#EF4444" flood-opacity="0.8"/>
    </filter>
    
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8"/>
    </marker>
    <marker id="arrowAmber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B"/>
    </marker>
  </defs>

  <!-- Title Header Banner -->
  <rect x="30" y="20" width="1860" height="65" rx="10" fill="url(#headerGrad)" stroke="#334155" stroke-width="1.5" filter="url(#dropShadow)" />
  <text x="50" y="52" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.5">MERIDIAN BIOPHARMA GLOBAL OPERATIONS | STRATEGIC MEETINGS &amp; EVENTS END-TO-END LIFECYCLE</text>
  <text x="50" y="73" fill="#38BDF8" font-size="12" font-weight="600">Enterprise Process Architecture &amp; High-Risk Data Leakage Points (DLP) Matrix | [CONFIDENTIAL SYNTHETIC SIMULATION]</text>
  <rect x="1620" y="32" width="250" height="40" rx="6" fill="#1E293B" stroke="#475569" />
  <text x="1745" y="57" fill="#FCD34D" font-size="11" font-weight="700" text-anchor="middle">GOVERNANCE LEVEL: ULTRA-COMPLEX</text>

  <!-- Swimlane 1: Requester & Business Unit -->
  <g transform="translate(30, 95)">
    <rect width="1860" height="140" fill="#0B132B" stroke="#1E293B" rx="8" />
    <rect width="210" height="140" fill="#111C44" rx="8" />
    <text x="15" y="45" fill="#38BDF8" font-size="12" font-weight="700">1. REQUESTER &amp; BU</text>
    <text x="15" y="65" fill="#94A3B8" font-size="10">Commercial, Medical Affairs,</text>
    <text x="15" y="80" fill="#94A3B8" font-size="10">Clinical R&amp;D Project Owners</text>
    <text x="15" y="115" fill="#64748B" font-size="9">Tool: Intake / Cvent Portal</text>
  </g>

  <!-- Swimlane 2: Medical Compliance & Legal -->
  <g transform="translate(30, 245)">
    <rect width="1860" height="140" fill="#0B132B" stroke="#1E293B" rx="8" />
    <rect width="210" height="140" fill="#1C1438" rx="8" />
    <text x="15" y="45" fill="#C084FC" font-size="12" font-weight="700">2. COMPLIANCE &amp; LEGAL</text>
    <text x="15" y="65" fill="#94A3B8" font-size="10">FMV Honoraria Review,</text>
    <text x="15" y="80" fill="#94A3B8" font-size="10">Sunshine / Anti-Kickback</text>
    <text x="15" y="115" fill="#64748B" font-size="9">Tool: Veeva / Compliance Gate</text>
  </g>

  <!-- Swimlane 3: SMM Platform (Cvent) -->
  <g transform="translate(30, 395)">
    <rect width="1860" height="140" fill="#0B132B" stroke="#1E293B" rx="8" />
    <rect width="210" height="140" fill="#062C26" rx="8" />
    <text x="15" y="45" fill="#34D399" font-size="12" font-weight="700">3. SMM ENTERPRISE</text>
    <text x="15" y="65" fill="#94A3B8" font-size="10">Meeting Registration, NPI</text>
    <text x="15" y="80" fill="#94A3B8" font-size="10">Validation, Session Agenda</text>
    <text x="15" y="115" fill="#64748B" font-size="9">Tool: Cvent Enterprise SMM</text>
  </g>

  <!-- Swimlane 4: Travel & Logistics -->
  <g transform="translate(30, 545)">
    <rect width="1860" height="140" fill="#0B132B" stroke="#1E293B" rx="8" />
    <rect width="210" height="140" fill="#2E1C07" rx="8" />
    <text x="15" y="45" fill="#FBBF24" font-size="12" font-weight="700">4. TRAVEL &amp; LOGISTICS</text>
    <text x="15" y="65" fill="#94A3B8" font-size="10">Air, Hotel Room Block,</text>
    <text x="15" y="80" fill="#94A3B8" font-size="10">Fleet &amp; Ground Mobility</text>
    <text x="15" y="115" fill="#64748B" font-size="9">Tool: Amex GBT / Travel Portal</text>
  </g>

  <!-- Swimlane 5: Payment & Expense -->
  <g transform="translate(30, 695)">
    <rect width="1860" height="140" fill="#0B132B" stroke="#1E293B" rx="8" />
    <rect width="210" height="140" fill="#360C1E" rx="8" />
    <text x="15" y="45" fill="#F472B6" font-size="12" font-weight="700">5. PAYMENT &amp; RECON</text>
    <text x="15" y="65" fill="#94A3B8" font-size="10">Virtual Ghost Card, Hotel</text>
    <text x="15" y="80" fill="#94A3B8" font-size="10">Master Folio, Employee T&amp;E</text>
    <text x="15" y="115" fill="#64748B" font-size="9">Tool: SAP Concur / Amex BTA</text>
  </g>

  <!-- Swimlane 6: ERP & Transparency Lake -->
  <g transform="translate(30, 845)">
    <rect width="1860" height="145" fill="#0B132B" stroke="#1E293B" rx="8" />
    <rect width="210" height="145" fill="#360A16" rx="8" />
    <text x="15" y="45" fill="#FB7185" font-size="12" font-weight="700">6. ERP &amp; TRANSPARENCY</text>
    <text x="15" y="65" fill="#94A3B8" font-size="10">WBS Settle, Spend Lake,</text>
    <text x="15" y="80" fill="#94A3B8" font-size="10">CMS Sunshine &amp; EFPIA</text>
    <text x="15" y="115" fill="#64748B" font-size="9">Tool: SAP S/4HANA / Snowflake</text>
  </g>

  <!-- Flow Connectors (Bridges & Arrows) -->
  <!-- n1 to n2 -->
  <path d="M 380 165 L 430 165 L 430 275" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="440" y="220" fill="#94A3B8" font-size="10" font-weight="600">Submit Request</text>

  <!-- n2 to n3 -->
  <path d="M 520 315 L 560 315 L 560 465 L 600 465" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="568" y="380" fill="#34D399" font-size="10" font-weight="700">Compliance Approved</text>

  <!-- n3 to n9 (Virtual card issuance) -->
  <path d="M 690 500 L 690 730" fill="none" stroke="#F472B6" stroke-width="2.5" stroke-dasharray="4" marker-end="url(#arrow)" />
  <text x="700" y="615" fill="#F472B6" font-size="10" font-weight="600">Auto-Issue Virtual Card</text>

  <!-- n3 to n4 -->
  <path d="M 780 465 L 830 465" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="785" y="455" fill="#94A3B8" font-size="10" font-weight="600">Publish Event</text>

  <!-- n4 to n5 -->
  <path d="M 920 500 L 920 580" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="930" y="545" fill="#FBBF24" font-size="10" font-weight="600">HCP Travel Request</text>

  <!-- n5 to n6 -->
  <path d="M 1010 615 L 1060 615" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />

  <!-- n4 to n7 (Arrive at Event) -->
  <path d="M 1010 465 L 1150 465 L 1150 200" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="1070" y="445" fill="#94A3B8" font-size="10" font-weight="600">Travelers Check In</text>

  <!-- n7 to n8 -->
  <path d="M 1240 165 L 1290 165" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="1245" y="155" fill="#94A3B8" font-size="10" font-weight="600">Adjourned</text>

  <!-- n8 to n10 -->
  <path d="M 1380 200 L 1380 730" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="1390" y="470" fill="#F472B6" font-size="10" font-weight="700">Actual Attendee Roster Upload</text>

  <!-- n9 to n10 (Card Master Folio Charge) -->
  <path d="M 780 765 L 1290 765" fill="none" stroke="#F472B6" stroke-width="2.5" stroke-dasharray="4" marker-end="url(#arrow)" />
  <text x="960" y="755" fill="#F472B6" font-size="10" font-weight="600">Master Folio Charged (BEO &amp; Hotel Invoices)</text>

  <!-- n10 to n11 -->
  <path d="M 1470 765 L 1570 765 L 1570 880" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="1578" y="820" fill="#FB7185" font-size="10" font-weight="600">Approve &amp; Settle</text>

  <!-- n11 to n13 -->
  <path d="M 1660 915 L 1710 915" fill="none" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="1665" y="905" fill="#94A3B8" font-size="10" font-weight="600">ETL Feed</text>

  <!-- n13 to n12 -->
  <path d="M 1795 880 L 1795 350" fill="none" stroke="#C084FC" stroke-width="2.5" marker-end="url(#arrow)" />
  <text x="1805" y="600" fill="#C084FC" font-size="10" font-weight="700">Annual Audit &amp; Disclosure</text>

  <!-- Process Step Nodes -->
  <!-- Node 1: Initiation -->
  <g transform="translate(260, 130)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#reqGrad)" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Meeting Initiation</text>
    <text x="90" y="44" fill="#93C5FD" font-size="9" text-anchor="middle">Define Purpose, Budget,</text>
    <text x="90" y="58" fill="#93C5FD" font-size="9" text-anchor="middle">Dates, WBS &amp; Cost Center</text>
  </g>

  <!-- Node 2: Compliance Review -->
  <g transform="translate(390, 275)" filter="url(#dropShadow)">
    <polygon points="95,0 190,40 95,80 0,40" fill="url(#compGrad)" stroke="#A855F7" stroke-width="1.5"/>
    <text x="95" y="36" fill="#F8FAFC" font-size="10" font-weight="700" text-anchor="middle">Compliance Review</text>
    <text x="95" y="50" fill="#E9D5FF" font-size="8.5" text-anchor="middle">FMV Tiers &amp; Conflict Check</text>
  </g>

  <!-- Node 3: Cvent SMM Setup -->
  <g transform="translate(600, 430)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#smmGrad)" stroke="#10B981" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Cvent SMM Setup</text>
    <text x="90" y="44" fill="#6EE7B7" font-size="9" text-anchor="middle">Issue Meeting ID (CVT-XXX)</text>
    <text x="90" y="58" fill="#6EE7B7" font-size="9" text-anchor="middle">NPI &amp; Attendee Rules Gate</text>
  </g>

  <!-- Node 4: HCP Registration -->
  <g transform="translate(830, 430)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#smmGrad)" stroke="#10B981" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">HCP Registration</text>
    <text x="90" y="44" fill="#6EE7B7" font-size="9" text-anchor="middle">Capture 10-Digit NPI &amp; Tax ID</text>
    <text x="90" y="58" fill="#6EE7B7" font-size="9" text-anchor="middle">Travel &amp; Room Block Profile</text>
  </g>

  <!-- Node 5: TMC Booking -->
  <g transform="translate(830, 580)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#tmcGrad)" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">TMC Air &amp; Hotel</text>
    <text x="90" y="44" fill="#FDE68A" font-size="9" text-anchor="middle">Book Corporate Fares</text>
    <text x="90" y="58" fill="#FDE68A" font-size="9" text-anchor="middle">Attach Cvent Meeting ID</text>
  </g>

  <!-- Node 6: Ground Fleet Dispatch -->
  <g transform="translate(1060, 580)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#tmcGrad)" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Ground Fleet Logistics</text>
    <text x="90" y="44" fill="#FDE68A" font-size="9" text-anchor="middle">Executive Shuttles &amp; EV Fleet</text>
    <text x="90" y="58" fill="#FDE68A" font-size="9" text-anchor="middle">Telematics CO2e Recording</text>
  </g>

  <!-- Node 7: Event Execution -->
  <g transform="translate(1060, 130)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#reqGrad)" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Event Execution</text>
    <text x="90" y="44" fill="#93C5FD" font-size="9" text-anchor="middle">Badge RFID Scans &amp;</text>
    <text x="90" y="58" fill="#93C5FD" font-size="9" text-anchor="middle">Sign-In Roster Collection</text>
  </g>

  <!-- Node 8: Post-Event Closeout -->
  <g transform="translate(1290, 130)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#reqGrad)" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Roster Submission</text>
    <text x="90" y="44" fill="#93C5FD" font-size="9" text-anchor="middle">Upload Final Attendance &lt;14d</text>
    <text x="90" y="58" fill="#93C5FD" font-size="9" text-anchor="middle">Mark No-Shows &amp; Cancellations</text>
  </g>

  <!-- Node 9: Virtual Card Issuance -->
  <g transform="translate(600, 730)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#cardGrad)" stroke="#EC4899" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Virtual Card Issuance</text>
    <text x="90" y="44" fill="#FBCFE8" font-size="9" text-anchor="middle">Single-Use Pre-Funded Card</text>
    <text x="90" y="58" fill="#FBCFE8" font-size="9" text-anchor="middle">Locked to Venue Merchant</text>
  </g>

  <!-- Node 10: SAP Concur Expense -->
  <g transform="translate(1290, 730)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#cardGrad)" stroke="#EC4899" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">SAP Concur Expense</text>
    <text x="90" y="44" fill="#FBCFE8" font-size="9" text-anchor="middle">Auto-Match Virtual Card BEO</text>
    <text x="90" y="58" fill="#FBCFE8" font-size="9" text-anchor="middle">Per-Capita Meal Allocation</text>
  </g>

  <!-- Node 11: SAP S/4HANA Posting -->
  <g transform="translate(1480, 880)" filter="url(#dropShadow)">
    <rect width="180" height="70" rx="8" fill="url(#erpGrad)" stroke="#F43F5E" stroke-width="1.5"/>
    <text x="90" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">SAP S/4HANA Posting</text>
    <text x="90" y="44" fill="#FDA4AF" font-size="9" text-anchor="middle">Cost Center &amp; WBS Ledger</text>
    <text x="90" y="58" fill="#FDA4AF" font-size="9" text-anchor="middle">Clear Virtual Card Accounts</text>
  </g>

  <!-- Node 13: Snowflake Spend Lake -->
  <g transform="translate(1710, 880)" filter="url(#dropShadow)">
    <rect width="170" height="70" rx="8" fill="url(#erpGrad)" stroke="#F43F5E" stroke-width="1.5"/>
    <text x="85" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Snowflake Spend Lake</text>
    <text x="85" y="44" fill="#FDA4AF" font-size="9" text-anchor="middle">Automated NPI ToV Table</text>
    <text x="85" y="58" fill="#FDA4AF" font-size="9" text-anchor="middle">US CMS &amp; EFPIA Export</text>
  </g>

  <!-- Node 12: Compliance Audit -->
  <g transform="translate(1710, 275)" filter="url(#dropShadow)">
    <rect width="170" height="70" rx="8" fill="url(#compGrad)" stroke="#A855F7" stroke-width="1.5"/>
    <text x="85" y="28" fill="#F8FAFC" font-size="11" font-weight="700" text-anchor="middle">Transparency Sign-Off</text>
    <text x="85" y="44" fill="#E9D5FF" font-size="9" text-anchor="middle">Federal Disclosure Portal</text>
    <text x="85" y="58" fill="#E9D5FF" font-size="9" text-anchor="middle">Dispute Resolution Window</text>
  </g>

  <!-- DATA LEAKAGE POINT CALLOUTS (VIVID RED GLOW BADGES) -->
  <!-- DLP-1 -->
  <g transform="translate(250, 95)" filter="url(#glowRed)">
    <rect width="190" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="95" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">CRITICAL FAILURE: DLP-1</text>
    <text x="95" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">Rogue Direct Booking / SMM Bypass</text>
    <text x="95" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">Missing Cvent ID &amp; MSA Contracts</text>
  </g>

  <!-- DLP-7 -->
  <g transform="translate(390, 240)" filter="url(#glowRed)">
    <rect width="190" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="95" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">HIGH RISK: DLP-7</text>
    <text x="95" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">Cross-Border Regulatory Omission</text>
    <text x="95" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">Missing Host/Home Country Sign-Off</text>
  </g>

  <!-- DLP-2 -->
  <g transform="translate(390, 360)" filter="url(#glowRed)">
    <rect width="190" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="95" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">CRITICAL FAILURE: DLP-2</text>
    <text x="95" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">HCP Identity &amp; FMV Disconnect</text>
    <text x="95" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">Missing 10-Digit NPI / Unvetted Tier</text>
  </g>

  <!-- DLP-4 -->
  <g transform="translate(600, 805)" filter="url(#glowRed)">
    <rect width="190" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="95" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">HIGH RISK: DLP-4</text>
    <text x="95" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">Virtual Card Orphan Charges</text>
    <text x="95" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">Hotel Folio Missing Level 3 Data</text>
  </g>

  <!-- DLP-3 -->
  <g transform="translate(950, 655)" filter="url(#glowRed)">
    <rect width="190" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="95" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">MEDIUM RISK: DLP-3</text>
    <text x="95" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">Fleet Telematics &amp; ESG Blindspot</text>
    <text x="95" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">Unmetered Scope 3 CO2 &amp; Passenger Gap</text>
  </g>

  <!-- DLP-5 -->
  <g transform="translate(1280, 95)" filter="url(#glowRed)">
    <rect width="200" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="100" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">CRITICAL FAILURE: DLP-5</text>
    <text x="100" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">Post-Event Roster Leakage (&gt;14d)</text>
    <text x="100" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">No-Shows Distort Per-Capita Sunshine ToV</text>
  </g>

  <!-- DLP-6 -->
  <g transform="translate(1280, 805)" filter="url(#glowRed)">
    <rect width="200" height="48" rx="6" fill="url(#dlpGrad)" stroke="#EF4444" stroke-width="2"/>
    <text x="100" y="18" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">HIGH RISK: DLP-6</text>
    <text x="100" y="31" fill="#FEF2F2" font-size="8" text-anchor="middle">Financial WBS Code Desync</text>
    <text x="100" y="42" fill="#FCA5A5" font-size="7.5" text-anchor="middle">Concur Expense Mismatch vs Clinical Trial</text>
  </g>

  <!-- Legend & Metadata Footer -->
  <g transform="translate(30, 1000)">
    <rect width="1860" height="60" rx="8" fill="#0F172A" stroke="#334155" />
    <text x="25" y="35" fill="#E2E8F0" font-size="11" font-weight="700">LEGEND &amp; CONTROL GATES:</text>
    
    <circle cx="210" cy="30" r="8" fill="#3B82F6" />
    <text x="225" y="35" fill="#94A3B8" font-size="10">Requester Stage</text>

    <circle cx="340" cy="30" r="8" fill="#A855F7" />
    <text x="355" y="35" fill="#94A3B8" font-size="10">Compliance Gate</text>

    <circle cx="480" cy="30" r="8" fill="#10B981" />
    <text x="495" y="35" fill="#94A3B8" font-size="10">SMM Cvent System</text>

    <circle cx="630" cy="30" r="8" fill="#F59E0B" />
    <text x="645" y="35" fill="#94A3B8" font-size="10">Travel &amp; Logistics Agency</text>

    <circle cx="780" cy="30" r="8" fill="#EC4899" />
    <text x="795" y="35" fill="#94A3B8" font-size="10">Payment &amp; Expense</text>

    <circle cx="930" cy="30" r="8" fill="#F43F5E" />
    <text x="945" y="35" fill="#94A3B8" font-size="10">ERP S/4HANA &amp; Spend</text>

    <rect x="1100" y="20" width="22" height="20" rx="4" fill="#DC2626" />
    <text x="1130" y="35" fill="#FEF2F2" font-size="10" font-weight="700">Critical Data Leakage Point (DLP-1 to 7)</text>

    <text x="1560" y="35" fill="#64748B" font-size="10" font-weight="500">ISO 9001 / EFPIA / US Sunshine Act Audit Architecture</text>
  </g>
</svg>"""

    svg_path = os.path.join(PROCESS_DIR, "meetings_events_lifecycle.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated SVG Vector Map: {svg_path}")


def generate_matrix_json():
    """Outputs machine-readable data leakage matrix."""
    matrix_path = os.path.join(PROCESS_DIR, "data_leakage_points_matrix.json")
    with open(matrix_path, "w", encoding="utf-8") as f:
        json.dump(DLP_DATA, f, indent=2)
    print(f"Generated DLP Matrix JSON: {matrix_path}")


def generate_specification_markdown():
    """Generates the enterprise SOP and Failure Mode & Effects Analysis (FMEA)."""
    md_content = """# Global Standard Operating Procedure: Meetings & Events Data Governance Lifecycle
**Document ID:** SOP-ME-2026-08  
**Department:** Global Meetings & Events Operations  
**Entity:** Meridian BioPharma Global Operations  
**Regulatory Standards:** US CMS Open Payments (Sunshine Act 42 CFR Part 403), EFPIA Disclosure Code 2014, FCPA, UK ABPI Code, ISO 14064 (GHG Scope 3)  
**Status:** Approved Enterprise Architecture & Remediation Standard  
**Notice:** *CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC*

---

## 1. Executive Summary & Purpose
In global life sciences, medical meetings and investigator symposia represent substantial operational investments and significant statutory compliance exposure. Under the United States Physician Payments Sunshine Act and the European Federation of Pharmaceutical Industries and Associations (EFPIA) Disclosure Code, pharmaceutical manufacturers are legally mandated to track, aggregate, and report every dollar, meal, and travel expenditure transferred to covered Healthcare Professionals (HCPs) and Healthcare Organizations (HCOs).

Disjointed systems across **Meeting Planning (Cvent)**, **Travel Management (Amex GBT)**, **Payment Gateways (Amex BTA & Virtual Cards)**, **Expense Filing (SAP Concur)**, and **Core Accounting (SAP S/4HANA)** routinely generate **Data Leakage Points (DLPs)**. This SOP codifies the end-to-end lifecycle, defines the Failure Mode and Effects Analysis (FMEA), and mandates the technical controls required to maintain an enterprise data accuracy rate of **>= 95.0%**.

---

## 2. End-to-End System Architecture & Swimlanes

```
+---------------------------------------------------------------------------------------------------+
| 1. Requester & Business Unit: Meeting Intake -> Budget Allocation -> Execution -> Roster Upload   |
+---------------------------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------------------------+
| 2. Compliance & Legal Gate: Fair Market Value (FMV) Tiering -> Cross-Border Review -> Sign-Off   |
+---------------------------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------------------------+
| 3. SMM Enterprise (Cvent): Issue Cvent ID -> Agenda -> Registration -> NPI Database Validation    |
+---------------------------------------------------------------------------------------------------+
                     |                                         |
                     v                                         v
+---------------------------------------------+   +-------------------------------------------------+
| 4. Travel & Fleet: Air, Rail, Hotel & Ground|   | 5. Payment & Card: Pre-Funded Single-Use Card   |
+---------------------------------------------+   +-------------------------------------------------+
                     |                                         |
                     +--------------------+--------------------+
                                          v
+---------------------------------------------------------------------------------------------------+
| 6. ERP & Aggregate Spend (SAP S/4HANA & Snowflake): Expense Reconcile -> WBS Clear -> CMS Filing  |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Failure Mode and Effects Analysis (FMEA) & Data Leakage Points Matrix

| DLP ID | Failure Mode / Phase | Root Cause | Missing Data Elements | Downstream Compliance & Financial Impact | Severity | Risk Priority Number (RPN) |
|---|---|---|---|---|---|---|
| **DLP-1** | **Rogue / Off-Channel Booking** *(Initiation)* | Requester books direct with hotel/resort via telephone or personal credit card to circumvent lead times. | Cvent Meeting ID, Signed MSA, Master Addendum, Cancellation Penalty terms. | Unbudgeted financial liability; cancellation penalties; 100% loss of duty-of-care visibility. | **CRITICAL** | **360 / 500** |
| **DLP-2** | **HCP Identity & FMV Disconnect** *(Pre-Clearance)* | HCP registered with informal names or missing 10-digit NPI / National Tax Identifier. Speaker fees exceed FMV cap. | National Provider Identifier (NPI), State Medical License #, FMV Tier Level verification. | CMS Open Payments audit failure; Civil Monetary Penalties up to $1M for knowing failures. | **CRITICAL** | **450 / 500** |
| **DLP-3** | **Fleet & Scope 3 Telematics Blindspot** *(Logistics)* | Local executive sedans or group shuttles booked via uncontracted suppliers without fleet API hook. | Distance (km), Fuel/Powertrain Type, CO2e (kg), Traveler Passenger Manifest. | Inability to audit Scope 3 Category 6 Business Travel emissions for CSRD & SEC disclosures. | **MEDIUM** | **180 / 500** |
| **DLP-4** | **Virtual Card Orphan Charges** *(Payment)* | Hotel front desk bill-backs charged with generic descriptor without embedding Cvent ID in Level 3 data. | Level 3 Merchant Interchange Data, Cvent Meeting ID Reference, Itemized Banquet Event Order (BEO). | Aged unallocated card balances (60-120 days); manual journal reconciliation; duplicate invoicing risk. | **HIGH** | **320 / 500** |
| **DLP-5** | **Post-Event Roster Leakage** *(Closeout)* | Organizer fails to submit physical/digital sign-in sheets within 14 calendar days post-event. | Verified Physical Sign-In Sheet, Confirmed No-Show Roster, Per-Capita F&B Allocation. | Distorted Transfer of Value (ToV); no-show physicians falsely reported to CMS Open Payments. | **CRITICAL** | **480 / 500** |
| **DLP-6** | **Financial Code Desync** *(Expense)* | Organizer files Concur expense report under department overhead cost center rather than clinical trial WBS. | Validated WBS Element, Internal Order Code, Cross-Charge Authorization. | Distorts clinical trial operational budgets; SOX 404 audit non-compliance; manual reallocation entries. | **HIGH** | **280 / 500** |
| **DLP-7** | **Cross-Border Regulatory Omission** *(HCP Travel)* | Non-resident HCP brought into foreign symposium without home/host country compliance clearance. | Cross-Border Notification Form (CBNF), Local Data Privacy (GDPR) Consent, Withholding Tax Token. | European EFPIA transparency non-compliance; local tax withholding liability. | **HIGH** | **315 / 500** |

---

## 4. Remediation Standard Operating Procedures (SOPs)

### 4.1. The "No Cvent ID, No Payment" Mandate (Remediation for DLP-1 & DLP-4)
- Virtual credit cards and BTA charge accounts cannot be issued by Corporate Finance without an active, approved Cvent Meeting ID (`CVT-XXXXXX`).
- Hotel Master Folios must mandate the embedding of the Cvent Meeting ID in the Merchant Reference field of Level 3 transaction data.

### 4.2. Automated NPI / NPPES Verification API (Remediation for DLP-2)
- All US HCP registrations in Cvent Enterprise trigger a real-time REST API lookup against the CMS National Plan and Provider Enumeration System (NPPES).
- Registrations lacking a validated 10-digit NPI are blocked from receiving travel ticketing and speaker honoraria agreements.

### 4.3. The 14-Day Post-Event Roster Escalation Protocol (Remediation for DLP-5)
- **Day +7 Post-Event:** Automated email reminder to Meeting Owner and Event Lead.
- **Day +14 Post-Event:** Formal warning; meeting status flagged as `DELINQUENT_ROSTER`.
- **Day +21 Post-Event:** Automatic escalation to Business Unit Vice President; temporary suspension of corporate card booking privileges until roster is uploaded.

---

## 5. Governance RACI Matrix

| Activity | Meeting Requester | Medical Compliance | SMM / Cvent Admin | TMC (Amex GBT) | Card & Expense Admin | S/4HANA ERP Team |
|---|---|---|---|---|---|---|
| Meeting Intake & WBS Coding | **Accountable** | Consulted | Informed | Informed | Informed | Informed |
| FMV Tiering & Cross-Border Check | Responsible | **Accountable** | Informed | Informed | Informed | Informed |
| SMM Configuration & NPI Gating | Informed | Consulted | **Accountable** | Informed | Informed | Informed |
| Travel & Fleet Telematics Booking | Informed | Informed | Consulted | **Accountable** | Informed | Informed |
| Virtual Card Master Folio Charge | Informed | Informed | Informed | Consulted | **Accountable** | Informed |
| Attendee Sign-In Roster Closeout | **Accountable** | Consulted | Responsible | Informed | Informed | Informed |
| Final CMS / EFPIA Transparency Run | Informed | **Accountable** | Consulted | Informed | Consulted | Responsible |

---
*Document Version: 2.4 | Approved by: Meridian Global Compliance & Procurement Council | [100% SYNTHETIC DATA]*
"""
    spec_path = os.path.join(PROCESS_DIR, "PROCESS_SPECIFICATION.md")
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Generated Process Specification: {spec_path}")


if __name__ == "__main__":
    generate_drawio_xml()
    generate_svg()
    generate_matrix_json()
    generate_specification_markdown()
    print("Process Map Deliverables successfully generated!")
