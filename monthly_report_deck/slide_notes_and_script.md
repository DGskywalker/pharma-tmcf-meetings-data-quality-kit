# Executive Presentation Script & Speaker Notes
**Deck Title:** Global Meetings & Events Monthly Data Quality & Compliance Governance Deck  
**Presenter:** Head of Global Meetings & Events Operations  
**Audience:** Global Procurement Committee, Chief Compliance Officer, Business Unit Vice Presidents  
**Period:** September 2026 | Q3 Governance Review  
**Notice:** *CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC*

---

## Slide 1: Title Slide (Global Meetings & Events Monthly Governance Briefing)
**Duration:** 1 minute  
**Slide Purpose:** Set the governance mandate, establish high stakes of global pharma meeting compliance, and introduce cross-functional scope across Travel, SMM, Corporate Cards, and Logistics.

**Speaker Script:**
> *"Good morning, members of the Executive Committee. Today we present our September 2026 monthly governance briefing on Meetings & Events Data Quality. In our industry, meetings and medical events are far more than logistical coordination—they represent our direct interface with Healthcare Professionals (HCPs) and carry statutory compliance mandates under the US Sunshine Act, CMS Open Payments, and European EFPIA codes. 
> 
> Today, we examine our cross-system data pipeline spanning Cvent SMM, SAP Concur, Amex BTA, and our Snowflake spend lake. We will highlight critical Data Leakage Points where information is lost, assess our financial and regulatory exposure, and outline our 90-day corrective action plan."*

---

## Slide 2: Executive Scorecard: Data Accuracy & Regulatory Exposure
**Duration:** 2 minutes  
**Key Metrics:**
- **Portfolio Accuracy:** 78.1% (Enterprise Target: >= 95.0%)
- **Total Audited Spend:** $224.4M across 1,500 meetings
- **Sunshine Act Spend at Risk:** $13.7M (6.1% in non-compliant state)
- **Flagged Deficiencies:** 329 events with active compliance/financial errors

**Speaker Script:**
> *"Looking at our executive scorecard, our portfolio data accuracy currently stands at 78.1%, leaving a 16.9% gap against our enterprise threshold of 95.0%. Out of $224.4 million in audited meeting expenditures across 1,500 events, $13.7 million carries critical compliance deficiencies. 
> 
> Under CMS Open Payments and European transparency regulations, submitting inaccurate or incomplete transfer-of-value records exposes Meridian to statutory fines up to $1 million for knowing failure to report, as well as significant reputational harm. Our radar analysis shows that while Medical Compliance pre-clearance is robust, our primary vulnerabilities lie in post-event roster latency and corporate card reconciliation."*

---

## Slide 3: Process Map & Data Leakage Point (DLP) Surveillance
**Duration:** 2 minutes  
**Key Visual:** Process Map Architecture & Failure Mode Matrix

**Speaker Script:**
> *"This architecture map charts the six critical swimlanes through which a meeting travels—from Requester initiation, through Compliance pre-clearance, Cvent setup, corporate travel booking, payment reconciliation, to final ERP and transparency reporting.
> 
> Across this journey, we have pinpointed seven critical Data Leakage Points (DLPs). The most dangerous are DLP-1, where requesters bypass Cvent to book directly off-channel; DLP-2, where HCP registrations lack validated 10-digit NPIs; and DLP-5, where post-event attendance rosters are delayed beyond 14 days. Each of these breaks data continuity and creates cascading accounting and compliance liabilities."*

---

## Slide 4: Strategic Meetings (Cvent SMM): The 14-Day Attendee Roster Challenge
**Duration:** 2.5 minutes  
**Key Visual:** Roster Submission Aging Histogram (SLA = 14 Days)

**Speaker Script:**
> *"Here we examine our single largest regulatory vulnerability: post-event attendee roster submission. Company policy mandates that verified physical or badge-scan sign-in sheets be uploaded within 14 calendar days of event adjournment.
> 
> As the aging chart demonstrates, 184 meetings exceeded this 14-day SLA, with 38 events delayed beyond 30 days. When rosters are delayed, the system defaults to the preliminary invitation list. This creates what we call 'Ghost Physician Transfer of Value'—physicians who canceled or were no-shows are falsely credited with meal and travel expenditures in federal filings. When these physicians dispute the records during the CMS review window, our legal team faces extensive audit burdens. Moving forward, we are introducing automated Day +7 and +14 alerts, with a mandatory corporate card freeze at Day +21."*

---

## Slide 5: Corporate Payment & Card Reconciliation: Clearing Aged Balances
**Duration:** 2 minutes  
**Key Metrics:**
- **Single-Use Virtual Cards:** 45% volume ($101.0M), 92.4% recon rate, 12-day avg lag.
- **Amex BTA Ghost Cards:** 30% volume ($67.3M), 74.8% recon rate, 48-day avg lag.
- **Aged Unreconciled AP (>45 days):** $9.4M across 38 events.

**Speaker Script:**
> *"Turning to payment mechanics: Virtual credit cards remain our gold standard, delivering a 92.4% reconciliation rate within 12 days. However, our Amex BTA Ghost card accounts show substantial latency, with $9.4 million aged over 45 days.
> 
> The primary root cause is the 'Hotel Restaurant Descriptor' problem. Hotel front desks bill master accounts using third-party restaurant merchant names without embedding our Cvent Meeting ID in Card Level 3 interchange data. To eliminate this, we are mandating that all master hotel agreements require Cvent ID embedding in Level 3 data, alongside direct Concur-to-Cvent nightly synchronization."*

---

## Slide 6: Healthcare Compliance & Business Unit Exposure Breakdown
**Duration:** 2 minutes  
**Key Visual:** Business Unit Accuracy & Sunshine Exposure Bar Chart

**Speaker Script:**
> *"Analyzing performance across our four operating units, Oncology demonstrated the highest discipline with an 81.4% accuracy rate, while Vaccines & Infectious Diseases lagged at 74.8%, driven by rapid launch cadence and expedited meeting turnarounds.
> 
> Crucially, US HCP National Provider Identifier (NPI) completeness currently sits at 91.2%. While high, the law requires 100%. The 24 events lacking valid NPIs must be remediated immediately. In Europe, 34 cross-border HCP sponsorships lacked host affiliate compliance notification. We are deploying automated pre-registration NPI lookup APIs to eliminate manual entry errors."*

---

## Slide 7: Root Cause Pareto Analysis: Top 8 Data Quality Deficiencies
**Duration:** 1.5 minutes  
**Key Visual:** Pareto Deficiencies Chart

**Speaker Script:**
> *"Our Pareto surveillance reveals a classic 80/20 distribution: three deficiencies—Roster Submission Lag, Missing HCP Identifiers, and Aged Card Reconciliation—account for 78% of all data quality failures across the portfolio.
> 
> This concentration gives us immense leverage. Rather than retraining 4,000 employees on 50 different rules, focusing automated controls on these three specific failure modes will elevate our portfolio accuracy above 92% within 60 days."*

---

## Slide 8: 90-Day Remediation Roadmap & Stakeholder Action Plan
**Duration:** 2 minutes  
**Key Deliverables:** 3-Phase Corrective and Preventive Action (CAPA) Plan

**Speaker Script:**
> *"To achieve our 95% accuracy milestone before annual CMS and EFPIA filings, we are executing a 90-day corrective action roadmap:
> 
> - **Phase 1 (Days 1–30):** Enact our 'No Cvent ID, No Payment' hard stop across Concur and Amex BTA, and activate live CMS NPPES NPI API validation at registration.
> - **Phase 2 (Days 31–60):** Deploy automated 7-day and 14-day roster escalation workflows to BU VPs, and enforce Level 3 Merchant Interchange standards across our master hotel network.
> - **Phase 3 (Days 61–90):** Integrate our live Snowflake Transparency Lake with automated anomaly alert webhooks to maintain continuous audit readiness.
> 
> We request the Committee's formal endorsement of the Day +21 corporate card suspension policy for delinquent rosters. Thank you, and I welcome your questions."*

---
*Script Version: 3.1 | Approved for Executive Committee Briefing | [100% SYNTHETIC DATA]*
