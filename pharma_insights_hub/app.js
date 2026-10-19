/**
 * Interactive Client Application for PharmaInsights Hub
 * Meridian BioPharma Global Operations Governance Suite
 * [CONFIDENTIAL - 100% SYNTHETIC DATA FOR SIMULATION]
 */

// Sample Data injected from DQ Audit Suite for fast client-side rendering
const AUDIT_METRICS = {
  totalRecords: 1500,
  cleanRecords: 1171,
  flaggedRecords: 329,
  accuracyPct: 78.07,
  auditedSpend: 224371770.23,
  sunshineExposureSpend: 13746683.80,
  exposurePct: 6.13,
  delinquentRosters: 184
};

// Representative Sample Meetings for Interactive Table
const SAMPLE_MEETINGS = [
  { id: "MTG-2026-10014", name: "Oncology Advisory Board Q2", bu: "Oncology", country: "US", type: "Advisory_Board", spend: 94500, hcp: 14, npis: "1948291048;1849102934", cvent: "CVT-491024", fmv: "Y", rosterDays: 6, cardRecon: "Y", errors: [], status: "CLEAN" },
  { id: "MTG-2026-10022", name: "Immunology Clinical Investigator Summit", bu: "Immunology_Inflammation", country: "US", type: "Investigator_Meeting", spend: 215000, hcp: 22, npis: "", cvent: "CVT-902184", fmv: "Y", rosterDays: 9, cardRecon: "Y", errors: ["R06_HCP_NPI_COMPLETENESS"], status: "CRITICAL" },
  { id: "MTG-2026-10038", name: "Rare Disease Medical Symposium", bu: "Rare_Disease", country: "DE", type: "Medical_Symposium", spend: 148000, hcp: 18, npis: "EFPIA-DE-491029", cvent: "", fmv: "Y", rosterDays: 8, cardRecon: "Y", errors: ["R05_CVENT_SMM_BINDING"], status: "CRITICAL" },
  { id: "MTG-2026-10045", name: "Vaccines Regional Launch Strategy", bu: "Vaccines_Infectious", country: "GB", type: "Commercial_Launch", spend: 285000, hcp: 26, npis: "EFPIA-GB-819201", cvent: "CVT-104928", fmv: "Y", rosterDays: 45, cardRecon: "Y", errors: ["R13_POST_EVENT_ROSTER_LAG"], status: "CRITICAL" },
  { id: "MTG-2026-10059", name: "Oncology Phase III Study Kickoff", bu: "Oncology", country: "US", type: "Investigator_Meeting", spend: 182000, hcp: 20, npis: "1849201948;1902849102", cvent: "CVT-392019", fmv: "Y", rosterDays: 7, cardRecon: "N", errors: ["R10_VIRTUAL_CARD_AGING_RECON"], status: "HIGH" },
  { id: "MTG-2026-10068", name: "Immunology Satellite Symposium", bu: "Immunology_Inflammation", country: "FR", type: "Satellite_Symposium", spend: 62000, hcp: 12, npis: "EFPIA-FR-102948", cvent: "CVT-849102", fmv: "N", rosterDays: 8, cardRecon: "Y", errors: ["R08_FMV_HONORARIA_VERIFICATION"], status: "HIGH" },
  { id: "MTG-2026-10074", name: "Internal Commercial Sales Rally", bu: "Vaccines_Infectious", country: "US", type: "Internal_Sales_Rally", spend: 115000, hcp: 0, npis: "", cvent: "CVT-501928", fmv: "N/A", rosterDays: 3, cardRecon: "Y", errors: [], status: "CLEAN" },
  { id: "MTG-2026-10089", name: "Rare Disease Patient Advisory Forum", bu: "Rare_Disease", country: "CH", type: "Advisory_Board", spend: 89000, hcp: 10, npis: "EFPIA-CH-774819", cvent: "CVT-772910", fmv: "Y", rosterDays: 5, cardRecon: "Y", errors: [], status: "CLEAN" },
  { id: "MTG-2026-10095", name: "Global Vaccines Medical Expert Panel", bu: "Vaccines_Infectious", country: "US", type: "Advisory_Board", spend: 105000, hcp: 15, npis: "NPI_UNKNOWN_99", cvent: "CVT-664910", fmv: "Y", rosterDays: 9, cardRecon: "Y", errors: ["R07_NPI_SYNTAX_VALIDITY"], status: "HIGH" },
  { id: "MTG-2026-10112", name: "Oncology Key Opinion Leader Roundtable", bu: "Oncology", country: "US", type: "Advisory_Board", spend: 91000, hcp: 12, npis: "1928471029;1827401928", cvent: "CVT-392011", fmv: "Y", rosterDays: 5, cardRecon: "Y", errors: [], status: "CLEAN" },
  { id: "MTG-2026-10125", name: "Immunology Regional Congress Symposium", bu: "Immunology_Inflammation", country: "DE", type: "Medical_Symposium", spend: 155000, hcp: 24, npis: "EFPIA-DE-559102", cvent: "CVT-449102", fmv: "Y", rosterDays: 52, cardRecon: "Y", errors: ["R13_POST_EVENT_ROSTER_LAG"], status: "CRITICAL" },
  { id: "MTG-2026-10134", name: "Rare Disease Clinical Trial Review", bu: "Rare_Disease", country: "US", type: "Investigator_Meeting", spend: 230000, hcp: 25, npis: "1839201948;1749201948", cvent: "CVT-992014", fmv: "Y", rosterDays: 6, cardRecon: "Y", errors: [], status: "CLEAN" }
];

// Data Leakage Points Details
const DLP_DETAILS = {
  "DLP-1": {
    name: "Rogue / Off-Channel Booking",
    stage: "Meeting Initiation & SMM Intake",
    systems: "Requester -> Direct Venue (Bypassing Cvent & TMC)",
    rootCause: "Meeting organizer contacts hotel directly via phone or personal card to avoid SMM lead times.",
    impact: "Invisible spend ($35k-$150k), unvetted cancellation liability, 0% duty of care tracking for travelers.",
    detection: "SAP Concur hotel expense > $1,000 without linked Cvent Meeting ID.",
    remediation: "Hard system freeze on expense reimbursement; retroactive Cvent registration within 48h."
  },
  "DLP-2": {
    name: "HCP Identity & FMV Tier Disconnect",
    stage: "Compliance Pre-Clearance & Registration",
    systems: "Cvent Enterprise <-> CMS NPPES / Sunshine Registry",
    rootCause: "HCP attendee registered with personal email; missing 10-digit NPI or unapproved honoraria rate.",
    impact: "Immediate statutory disclosure defect under US Sunshine Act (42 CFR Part 403); civil penalties up to $1M.",
    detection: "HCP_Count > 0 AND (HCP_NPI_Numbers IS BLANK OR FMV_Tier_Compliant = 'N').",
    remediation: "Automated real-time CMS NPPES API lookup gating speaker contract issuance."
  },
  "DLP-3": {
    name: "Ground Fleet & Scope 3 ESG Blindspot",
    stage: "Travel & Fleet Logistics Dispatch",
    systems: "TMC (Amex GBT) <-> Local Ground Fleet Suppliers",
    rootCause: "Executive sedans and group shuttles booked through unvetted vendors without telematics hooks.",
    impact: "Unmetered Scope 3 Category 6 emissions, passenger manifest gap, CSRD sustainability filing omissions.",
    detection: "Fleet_Ground_Transfer_Utilized = 'Y' AND Fleet_CO2_Emissions_kg IS NULL.",
    remediation: "Mandatory corporate fleet API integration across all ground transportation vendors."
  },
  "DLP-4": {
    name: "Virtual Card / BTA Master Folio Orphan Charges",
    stage: "Master Folio Payment & Accounting",
    systems: "Hotel Merchant Interchange <-> Banking Gateway (Amex BTA)",
    rootCause: "Hotel front desk charges master folio with generic descriptor without passing Cvent ID in Level 3 data.",
    impact: "Aged unallocated card clearing balances (60-120 days); manual accounting overhead; double payment risk.",
    detection: "Payment_Method = Virtual/BTA AND Card_Reconciled = 'N' AND Days_Since_Event > 45.",
    remediation: "Mandate Level 3 Merchant Interchange field 43 embedding Cvent ID on all hotel contracts."
  },
  "DLP-5": {
    name: "Post-Event Attendee Roster Leakage",
    stage: "Event Closeout & Spend Allocation",
    systems: "On-Site Badge Scan / Sign-In Sheet <-> Cvent SMM",
    rootCause: "Meeting organizer fails to upload verified attendance roster within 14 calendar days post-event.",
    impact: "No-show physicians falsely attributed transfer of value in CMS Open Payments, triggering physician disputes.",
    detection: "Post_Event_Roster_Captured = 'N' AND Days_To_Roster_Submission > 14.",
    remediation: "Automated Day +7 alert, Day +14 DELINQUENT notice, Day +21 corporate card suspension."
  },
  "DLP-6": {
    name: "Cross-System Financial Code Desync",
    stage: "Expense Reporting & ERP Posting",
    systems: "SAP Concur <-> SAP S/4HANA ERP",
    rootCause: "Meeting expenses coded to departmental operational cost center rather than clinical trial WBS.",
    impact: "Clinical trial accounting misstatements; distorted departmental budget variance reports.",
    detection: "WBS_Code IS BLANK for Investigator/Advisory meetings.",
    remediation: "Concur pre-submission validation rule blocking expense filing without validated WBS element."
  },
  "DLP-7": {
    name: "Cross-Border Regulatory Omission",
    stage: "HCP Travel & Cross-Border Compliance",
    systems: "Origin Affiliate Compliance <-> Host Affiliate Compliance",
    rootCause: "Foreign physician invited to international symposium without bilateral compliance clearance.",
    impact: "Breach of European EFPIA cross-border disclosure provisions; local tax withholding penalty exposure.",
    detection: "Cross_Border_HCP_Flag = 'Y' AND Compliance_Approval_Status != 'Approved'.",
    remediation: "Automated ticketing freeze in Amex GBT until cross-border clearance token is attached."
  }
};

let currentFilter = "ALL";

function renderTable() {
  const tbody = document.getElementById("tableBody");
  const searchVal = document.getElementById("searchInput").value.toLowerCase();
  tbody.innerHTML = "";

  const filtered = SAMPLE_MEETINGS.filter(m => {
    // Tab filter
    if (currentFilter === "CRITICAL" && m.status !== "CRITICAL") return false;
    if (currentFilter === "CLEAN" && m.status !== "CLEAN") return false;
    if (currentFilter === "ROSTER" && !m.errors.includes("R13_POST_EVENT_ROSTER_LAG")) return false;
    if (currentFilter === "CVENT" && !m.errors.includes("R05_CVENT_SMM_BINDING")) return false;
    if (currentFilter === "NPI" && !m.errors.includes("R06_HCP_NPI_COMPLETENESS") && !m.errors.includes("R07_NPI_SYNTAX_VALIDITY")) return false;
    if (currentFilter === "CARD" && !m.errors.includes("R10_VIRTUAL_CARD_AGING_RECON")) return false;

    // Search filter
    if (searchVal) {
      const match = m.id.toLowerCase().includes(searchVal) ||
                    m.name.toLowerCase().includes(searchVal) ||
                    m.bu.toLowerCase().includes(searchVal) ||
                    m.country.toLowerCase().includes(searchVal);
      if (!match) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 24px; color: var(--slate-light);">No matching meeting records found.</td></tr>`;
    return;
  }

  filtered.forEach(m => {
    const tr = document.createElement("tr");
    if (m.status === "CRITICAL") tr.classList.add("row-critical");
    if (m.status === "CLEAN") tr.classList.add("row-clean");

    let statusBadge = "";
    if (m.status === "CRITICAL") statusBadge = `<span class="badge badge-crit">CRITICAL (${m.errors.length})</span>`;
    else if (m.status === "HIGH") statusBadge = `<span class="badge badge-warn">WARNING (${m.errors.length})</span>`;
    else statusBadge = `<span class="badge badge-clean">CLEAN</span>`;

    tr.innerHTML = `
      <td><strong>${m.id}</strong></td>
      <td>${m.name}</td>
      <td>${m.bu.replace("_", " ")}</td>
      <td><strong>${m.country}</strong></td>
      <td>$${m.spend.toLocaleString()}</td>
      <td>${m.hcp}</td>
      <td>${m.cvent ? m.cvent : '<span style="color:var(--red); font-weight:bold;">MISSING</span>'}</td>
      <td>${statusBadge}</td>
    `;
    tbody.appendChild(tr);
  });
}

function setupFilters() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      currentFilter = tab.getAttribute("data-filter");
      renderTable();
    });
  });

  document.getElementById("searchInput").addEventListener("input", renderTable);
}

function setupDlpCards() {
  const cards = document.querySelectorAll(".dlp-card");
  cards.forEach(card => {
    card.addEventListener("click", () => {
      cards.forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      const dlpId = card.getAttribute("data-dlp");
      const dlp = DLP_DETAILS[dlpId];
      if (!dlp) return;

      const detailBox = document.getElementById("dlpDetailBox");
      detailBox.innerHTML = `
        <div style="background:#ffffff; border:1px solid var(--border); border-radius:var(--radius-md); padding:20px; box-shadow:var(--shadow-sm);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="color:var(--red); font-weight:800; font-size:1.1rem;">${dlpId}: ${dlp.name}</span>
            <span class="badge badge-crit">SEVERITY: CRITICAL</span>
          </div>
          <p style="font-size:0.85rem; margin-bottom:8px;"><strong>Lifecycle Stage:</strong> ${dlp.stage}</p>
          <p style="font-size:0.85rem; margin-bottom:8px;"><strong>Systems Involved:</strong> ${dlp.systems}</p>
          <p style="font-size:0.85rem; margin-bottom:8px;"><strong>Root Cause:</strong> ${dlp.rootCause}</p>
          <p style="font-size:0.85rem; margin-bottom:8px; color:var(--red);"><strong>Downstream Impact:</strong> ${dlp.impact}</p>
          <p style="font-size:0.85rem; margin-bottom:8px;"><strong>Automated Detection Rule:</strong> <code>${dlp.detection}</code></p>
          <div style="background:var(--teal-light); border-left:4px solid var(--teal); padding:10px 14px; border-radius:4px; font-size:0.82rem; margin-top:10px;">
            <strong>Standard Operating Procedure (SOP) Remediation:</strong> ${dlp.remediation}
          </div>
        </div>
      `;
    });
  });
}

function runSimulator() {
  const mType = document.getElementById("simType").value;
  const country = document.getElementById("simCountry").value;
  const hcpCount = parseInt(document.getElementById("simHcpCount").value) || 0;
  const cventId = document.getElementById("simCventId").value.trim();
  const npi = document.getElementById("simNpi").value.trim();
  const rosterDays = parseInt(document.getElementById("simRosterDays").value) || 0;
  const cardRecon = document.getElementById("simCardRecon").value;
  const variance = parseFloat(document.getElementById("simVariance").value) || 0;

  const errors = [];

  // R05: Cvent SMM ID
  if (hcpCount > 0 && !cventId) {
    errors.push("R05_CVENT_SMM_BINDING: External HCP meeting lacks mandatory Cvent SMM ID (DLP-1)");
  }

  // R06 & R07: US NPI check
  if (country === "US" && hcpCount > 0) {
    if (!npi) {
      errors.push("R06_HCP_NPI_COMPLETENESS: Missing US HCP National Provider Identifier (DLP-2)");
    } else if (!/^[12]\d{9}$/.test(npi)) {
      errors.push("R07_NPI_SYNTAX_VALIDITY: NPI number syntax invalid (must be 10 numeric digits starting with 1 or 2)");
    }
  }

  // R10: Card Recon
  if (cardRecon === "N") {
    errors.push("R10_VIRTUAL_CARD_AGING_RECON: Virtual/BTA card spend unreconciled past 45-day SLA (DLP-4)");
  }

  // R12: Spend Variance
  if (variance > 25.0) {
    errors.push(`R12_SPEND_VARIANCE_TOLERANCE: Actual spend exceeds budget by ${variance}% (Max allowed: 25%)`);
  }

  // R13: Roster Lag
  if (hcpCount > 0 && rosterDays > 14) {
    errors.push(`R13_POST_EVENT_ROSTER_LAG: Attendee roster submitted in ${rosterDays} days (SLA = 14 days) (DLP-5)`);
  }

  const resDiv = document.getElementById("simResult");
  resDiv.style.display = "block";

  if (errors.length === 0) {
    resDiv.innerHTML = `
      <div style="background:var(--green-light); border:1px solid #86efac; color:#14532d; padding:16px; border-radius:6px;">
        <h4 style="font-weight:800; font-size:1rem; margin-bottom:4px;">VALIDATION PASSED: 100% CLEAN RECORD</h4>
        <p style="font-size:0.85rem;">This meeting record satisfies all 16 enterprise data quality and compliance standards. Safe for automated CMS Open Payments & EFPIA transparency submission.</p>
      </div>
    `;
  } else {
    let errListHtml = errors.map(e => `<li style="margin-bottom:6px;">${e}</li>`).join("");
    resDiv.innerHTML = `
      <div style="background:var(--red-light); border:1px solid #fca5a5; color:#7f1d1d; padding:16px; border-radius:6px;">
        <h4 style="font-weight:800; font-size:1rem; margin-bottom:8px;">VALIDATION FAILED: ${errors.length} CRITICAL DEFICIENCIES FLAGGED</h4>
        <ul style="font-size:0.85rem; padding-left:20px; line-height:1.5;">${errListHtml}</ul>
        <p style="font-size:0.8rem; margin-top:10px; font-weight:bold;">Action Required: Resolve flagged exceptions before financial closeout.</p>
      </div>
    `;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderTable();
  setupFilters();
  setupDlpCards();
  document.getElementById("btnRunSim").addEventListener("click", runSimulator);
});
