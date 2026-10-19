# Global Standard Operating Procedure: Meetings & Events Data Governance Lifecycle
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
