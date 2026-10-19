"""
Data Quality Validation Engine for Meridian BioPharma Global Operations
Implements enterprise data quality dimensions: Completeness, Validity, Consistency,
Accuracy, Timeliness, and Regulatory Compliance across Travel, Meetings, Card, and Fleet.

Calculates Record-Level Accuracy %, Dimension Indexes, and Regulatory Financial Exposure.
[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import json
import re
import pandas as pd
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

RULES_SPECIFICATION = {
    "R01_CORE_COMPLETENESS": {
        "name": "Mandatory Primary Identifiers",
        "dimension": "Completeness",
        "domain": "Governance",
        "severity": "CRITICAL",
        "weight": 4.0,
        "dlp": "DLP-1",
        "description": "Meeting ID, Requester ID, and Cost Center must not be null or empty."
    },
    "R02_DATE_CHRONOLOGY": {
        "name": "Date Chronology Logic",
        "dimension": "Validity",
        "domain": "Operational",
        "severity": "CRITICAL",
        "weight": 4.0,
        "dlp": "Operational",
        "description": "Event End_Date must be greater than or equal to Start_Date."
    },
    "R03_RETROACTIVE_INTAKE": {
        "name": "Retroactive Meeting Creation Check",
        "dimension": "Timeliness",
        "domain": "Policy",
        "severity": "HIGH",
        "weight": 2.5,
        "dlp": "DLP-1",
        "description": "Meeting creation lead time cannot be negative (cannot be requested after the event has started)."
    },
    "R04_ADVANCE_LEAD_TIME_POLICY": {
        "name": "21-Day Advance Notice Policy",
        "dimension": "Timeliness",
        "domain": "Policy",
        "severity": "MEDIUM",
        "weight": 1.5,
        "dlp": "Operational",
        "description": "High-budget HCP meetings (> $50,000) must have >= 21 days lead time unless fast-track exception noted."
    },
    "R05_CVENT_SMM_BINDING": {
        "name": "Cvent SMM ID Adherence",
        "dimension": "Completeness",
        "domain": "Meetings",
        "severity": "CRITICAL",
        "weight": 4.0,
        "dlp": "DLP-1",
        "description": "Any meeting with external HCP attendees must possess an active Cvent SMM ID (CVT-XXXXXX)."
    },
    "R06_HCP_NPI_COMPLETENESS": {
        "name": "US HCP NPI Identification Presence",
        "dimension": "Completeness",
        "domain": "Compliance",
        "severity": "CRITICAL",
        "weight": 4.0,
        "dlp": "DLP-2",
        "description": "US meetings with HCP attendees must have non-blank NPI numbers for CMS Open Payments filing."
    },
    "R07_NPI_SYNTAX_VALIDITY": {
        "name": "10-Digit NPI Number Syntax",
        "dimension": "Validity",
        "domain": "Compliance",
        "severity": "HIGH",
        "weight": 2.5,
        "dlp": "DLP-2",
        "description": "US NPI numbers must be valid 10-digit numeric identifiers starting with 1 or 2."
    },
    "R08_FMV_HONORARIA_VERIFICATION": {
        "name": "Fair Market Value (FMV) Tier Clearance",
        "dimension": "Consistency",
        "domain": "Compliance",
        "severity": "HIGH",
        "weight": 3.0,
        "dlp": "DLP-2",
        "description": "Meetings cannot be Approved if FMV Tier Compliance is marked 'N'."
    },
    "R09_CROSS_BORDER_CLEARANCE": {
        "name": "Cross-Border HCP Compliance Approval",
        "dimension": "Consistency",
        "domain": "Compliance",
        "severity": "HIGH",
        "weight": 2.5,
        "dlp": "DLP-7",
        "description": "Meetings with Cross-Border HCPs require formal compliance sign-off (cannot be Conditional or Rejected)."
    },
    "R10_VIRTUAL_CARD_AGING_RECON": {
        "name": "Virtual / BTA Card Reconciliation Aging",
        "dimension": "Timeliness",
        "domain": "Card",
        "severity": "HIGH",
        "weight": 2.5,
        "dlp": "DLP-4",
        "description": "Ghost BTA and Virtual Cards must be reconciled within 45 days of event completion."
    },
    "R11_CONCUR_REPORT_LINKAGE": {
        "name": "SAP Concur Expense Report Binding",
        "dimension": "Completeness",
        "domain": "Card",
        "severity": "HIGH",
        "weight": 2.5,
        "dlp": "DLP-4",
        "description": "Meetings with card spend must reference a valid SAP Concur Expense Report ID."
    },
    "R12_SPEND_VARIANCE_TOLERANCE": {
        "name": "Financial Spend Budget Variance (+25% Threshold)",
        "dimension": "Consistency",
        "domain": "Financial",
        "severity": "MEDIUM",
        "weight": 2.0,
        "dlp": "DLP-6",
        "description": "Actual spend must not exceed estimated budget by > 25.0% without supplemental variance approval."
    },
    "R13_POST_EVENT_ROSTER_LAG": {
        "name": "14-Day Post-Event Roster SLA",
        "dimension": "Timeliness",
        "domain": "Meetings",
        "severity": "CRITICAL",
        "weight": 4.0,
        "dlp": "DLP-5",
        "description": "Physical/digital attendee rosters must be uploaded and finalized within 14 calendar days post-event."
    },
    "R14_WBS_CLINICAL_CODE_DESYNC": {
        "name": "Clinical Project WBS Accounting Alignment",
        "dimension": "Completeness",
        "domain": "Financial",
        "severity": "MEDIUM",
        "weight": 1.5,
        "dlp": "DLP-6",
        "description": "Clinical investigator and advisory meetings must contain a valid clinical trial WBS Element."
    },
    "R15_SUNSHINE_JURISDICTION_SYNC": {
        "name": "Sunshine Act / EFPIA Jurisdiction Sync",
        "dimension": "Consistency",
        "domain": "Compliance",
        "severity": "HIGH",
        "weight": 2.5,
        "dlp": "DLP-7",
        "description": "US HCP meetings must be flagged as Sunshine Reportable ('Y')."
    },
    "R16_FLEET_CO2_TELEMATICS_PRESENCE": {
        "name": "Fleet Ground Transport Scope 3 CO2 Metering",
        "dimension": "Completeness",
        "domain": "Fleet",
        "severity": "LOW",
        "weight": 1.0,
        "dlp": "DLP-3",
        "description": "Meetings utilizing ground fleet transfers must have logged CO2 emissions (kg) for CSRD Scope 3 reporting."
    }
}


def evaluate_record(row):
    """Evaluates an individual meeting record against the 16 DQ rules."""
    errors = []

    # R01: Mandatory Core Identifiers
    if pd.isna(row.get("Meeting_ID")) or not str(row.get("Meeting_ID")).strip() or \
       pd.isna(row.get("Cost_Center")) or not str(row.get("Cost_Center")).strip() or \
       pd.isna(row.get("Requester_ID")) or not str(row.get("Requester_ID")).strip():
        errors.append("R01_CORE_COMPLETENESS")

    # R02: Date Chronology Logic
    try:
        s_date = pd.to_datetime(row.get("Start_Date"))
        e_date = pd.to_datetime(row.get("End_Date"))
        if e_date < s_date:
            errors.append("R02_DATE_CHRONOLOGY")
    except Exception:
        errors.append("R02_DATE_CHRONOLOGY")

    # R03: Retroactive Meeting Creation
    lead_time = row.get("Creation_Lead_Time_Days")
    if pd.notna(lead_time) and float(lead_time) < 0:
        errors.append("R03_RETROACTIVE_INTAKE")

    # R04: 21-Day Advance Notice Policy
    budget = float(row.get("Budget_Estimated_USD", 0))
    if pd.notna(lead_time) and float(lead_time) >= 0 and float(lead_time) < 21 and budget > 50000 and row.get("HCP_Attendees_Count", 0) > 0:
        errors.append("R04_ADVANCE_LEAD_TIME_POLICY")

    # R05: Cvent SMM ID Adherence
    hcp_count = int(row.get("HCP_Attendees_Count", 0))
    cvent_id = str(row.get("Cvent_Registration_ID", "")).strip()
    if hcp_count > 0 and (not cvent_id or cvent_id == "nan"):
        errors.append("R05_CVENT_SMM_BINDING")

    # R06 & R07: US HCP NPI Identification & Syntax
    country = str(row.get("Country_Code", "")).strip()
    npis_raw = str(row.get("HCP_NPI_Numbers", "")).strip()
    if country == "US" and hcp_count > 0:
        if not npis_raw or npis_raw == "nan":
            errors.append("R06_HCP_NPI_COMPLETENESS")
        else:
            # Check syntax: 10 digits numeric
            tokens = [t.strip() for t in npis_raw.split(";") if t.strip()]
            invalid_syntax = False
            for tok in tokens:
                if not re.match(r"^[12]\d{9}$", tok):
                    invalid_syntax = True
                    break
            if invalid_syntax:
                errors.append("R07_NPI_SYNTAX_VALIDITY")

    # R08: FMV Tier Clearance
    fmv_status = str(row.get("FMV_Tier_Compliant_Flag", "")).strip()
    approval = str(row.get("Compliance_Approval_Status", "")).strip()
    if fmv_status == "N" and approval == "Approved":
        errors.append("R08_FMV_HONORARIA_VERIFICATION")

    # R09: Cross-Border HCP Clearance
    cross_border = str(row.get("Cross_Border_HCP_Flag", "")).strip()
    if cross_border == "Y" and approval != "Approved":
        errors.append("R09_CROSS_BORDER_CLEARANCE")

    # R10: Virtual Card Aging Recon
    pay_method = str(row.get("Payment_Method", "")).strip()
    card_recon = str(row.get("Corporate_Card_Reconciled_Flag", "")).strip()
    if pay_method in ["Amex_BTA_Ghost", "Single_Use_Virtual_Card"] and card_recon == "N":
        errors.append("R10_VIRTUAL_CARD_AGING_RECON")

    # R11: SAP Concur Expense Report Binding
    concur_id = str(row.get("Concur_Expense_Report_ID", "")).strip()
    actual_spend = float(row.get("Actual_Spend_USD", 0))
    if actual_spend > 5000 and (not concur_id or concur_id == "nan"):
        errors.append("R11_CONCUR_REPORT_LINKAGE")

    # R12: Spend Variance Tolerance (+25%)
    variance_pct = float(row.get("Spend_Variance_Pct", 0))
    if variance_pct > 25.0:
        errors.append("R12_SPEND_VARIANCE_TOLERANCE")

    # R13: 14-Day Post-Event Roster SLA
    roster_cap = str(row.get("Post_Event_Roster_Captured", "")).strip()
    days_roster = row.get("Days_To_Roster_Submission")
    if roster_cap == "N" or (pd.notna(days_roster) and float(days_roster) > 14):
        errors.append("R13_POST_EVENT_ROSTER_LAG")

    # R14: Clinical WBS Accounting Alignment
    m_type = str(row.get("Meeting_Type", "")).strip()
    wbs = str(row.get("WBS_Code", "")).strip()
    if m_type in ["Investigator_Meeting", "Advisory_Board"] and (not wbs or wbs == "nan"):
        errors.append("R14_WBS_CLINICAL_CODE_DESYNC")

    # R15: Sunshine Jurisdiction Sync
    sunshine = str(row.get("EFPIA_Sunshine_Reportable", "")).strip()
    if country == "US" and hcp_count > 0 and sunshine != "Y":
        errors.append("R15_SUNSHINE_JURISDICTION_SYNC")

    # R16: Fleet CO2 Telematics Presence
    fleet_util = str(row.get("Fleet_Ground_Transfer_Utilized", "")).strip()
    fleet_co2 = row.get("Fleet_CO2_Emissions_kg")
    if fleet_util == "Y" and (pd.isna(fleet_co2) or float(fleet_co2) <= 0):
        errors.append("R16_FLEET_CO2_TELEMATICS_PRESENCE")

    return errors


def run_data_quality_audit(raw_csv_path=None):
    """Executes the full DQ pipeline and generates structured audit analytics."""
    if raw_csv_path is None:
        raw_csv_path = os.path.join(DATA_DIR, "synthetic_meetings_raw.csv")

    df = pd.read_csv(raw_csv_path)
    total_records = len(df)

    # Evaluate each record
    results = [evaluate_record(row) for _, row in df.iterrows()]
    df["Error_Count"] = [len(errs) for errs in results]
    df["Error_Codes"] = [";".join(errs) for errs in results]
    df["Is_Clean_Record"] = df["Error_Count"] == 0

    # Categorize error severity
    has_critical = []
    has_high = []
    has_medium = []
    has_low = []
    penalty_scores = []

    for errs in results:
        crit = any(RULES_SPECIFICATION[e]["severity"] == "CRITICAL" for e in errs)
        high = any(RULES_SPECIFICATION[e]["severity"] == "HIGH" for e in errs)
        med = any(RULES_SPECIFICATION[e]["severity"] == "MEDIUM" for e in errs)
        low = any(RULES_SPECIFICATION[e]["severity"] == "LOW" for e in errs)
        
        penalty = sum(RULES_SPECIFICATION[e]["weight"] for e in errs)
        
        has_critical.append("Y" if crit else "N")
        has_high.append("Y" if high else "N")
        has_medium.append("Y" if med else "N")
        has_low.append("Y" if low else "N")
        penalty_scores.append(penalty)

    df["Has_Critical_Error"] = has_critical
    df["Has_High_Error"] = has_high
    df["Has_Medium_Error"] = has_medium
    df["Has_Low_Error"] = has_low
    df["Penalty_Score"] = penalty_scores

    # Clean records
    clean_count = int(df["Is_Clean_Record"].sum())
    flagged_count = total_records - clean_count
    accuracy_pct = round((clean_count / total_records) * 100, 2)

    # Weighted Data Health Index
    max_penalty_per_record = sum(r["weight"] for r in RULES_SPECIFICATION.values())
    total_penalties = sum(penalty_scores)
    max_possible_penalties = total_records * max_penalty_per_record
    weighted_health_index = round(100.0 - (total_penalties / max_possible_penalties * 100 * 8.5), 2)
    weighted_health_index = max(0.0, min(100.0, weighted_health_index))

    # Compliance Exposure ($ spend on meetings with critical errors)
    critical_spend = df[df["Has_Critical_Error"] == "Y"]["Actual_Spend_USD"].sum()
    total_spend = df["Actual_Spend_USD"].sum()
    compliance_exposure_pct = round((critical_spend / total_spend) * 100, 2)

    # Error frequency by rule
    rule_counts = {r_code: 0 for r_code in RULES_SPECIFICATION}
    for errs in results:
        for e in errs:
            if e in rule_counts:
                rule_counts[e] += 1

    rule_summary_table = []
    for r_code, count in rule_counts.items():
        spec = RULES_SPECIFICATION[r_code]
        rule_summary_table.append({
            "Rule_Code": r_code,
            "Rule_Name": spec["name"],
            "Dimension": spec["dimension"],
            "Domain": spec["domain"],
            "Severity": spec["severity"],
            "DLP_Reference": spec["dlp"],
            "Failure_Count": count,
            "Failure_Rate_Pct": round((count / total_records) * 100, 2),
            "Description": spec["description"]
        })

    rule_summary_df = pd.DataFrame(rule_summary_table).sort_values(by="Failure_Count", ascending=False)

    # Business Unit Breakdown
    bu_summary = df.groupby("Business_Unit").agg(
        Total_Meetings=("Meeting_ID", "count"),
        Clean_Meetings=("Is_Clean_Record", lambda x: int(x.sum())),
        Critical_Meetings=("Has_Critical_Error", lambda x: int((x == "Y").sum())),
        Total_Spend_USD=("Actual_Spend_USD", "sum"),
        Critical_Spend_USD=("Actual_Spend_USD", lambda x: x[df.loc[x.index, "Has_Critical_Error"] == "Y"].sum())
    ).reset_index()
    bu_summary["Accuracy_Pct"] = round((bu_summary["Clean_Meetings"] / bu_summary["Total_Meetings"]) * 100, 2)
    bu_summary["Critical_Spend_Exposure_Pct"] = round((bu_summary["Critical_Spend_USD"] / bu_summary["Total_Spend_USD"]) * 100, 2)

    # Domain Quality Breakdown (Travel, Meetings, Card, Fleet, Compliance)
    domain_weights = {"Meetings": 0, "Card": 0, "Compliance": 0, "Fleet": 0, "Financial": 0, "Operational": 0, "Policy": 0, "Governance": 0}
    domain_totals = {"Meetings": 0, "Card": 0, "Compliance": 0, "Fleet": 0, "Financial": 0, "Operational": 0, "Policy": 0, "Governance": 0}

    for r_code, count in rule_counts.items():
        dom = RULES_SPECIFICATION[r_code]["domain"]
        domain_weights[dom] += count
        domain_totals[dom] += total_records

    domain_scores = {}
    for dom in domain_weights:
        fail_rate = (domain_weights[dom] / max(1, domain_totals[dom]))
        score = round(max(0.0, 100.0 - (fail_rate * 100 * 3.5)), 1)
        domain_scores[dom] = min(100.0, score)

    # Export Flagged CSV
    flagged_csv_path = os.path.join(DATA_DIR, "synthetic_meetings_flagged.csv")
    df.to_csv(flagged_csv_path, index=False)
    print(f"Exported flagged meeting records: {flagged_csv_path}")

    # Compile JSON Summary
    summary_json = {
        "audit_timestamp": "2026-10-18T10:00:00Z",
        "entity": "Meridian BioPharma Global Operations",
        "total_records_audited": total_records,
        "clean_records_count": clean_count,
        "flagged_records_count": flagged_count,
        "overall_accuracy_percentage": accuracy_pct,
        "weighted_data_health_index": weighted_health_index,
        "total_expenditure_audited_usd": round(total_spend, 2),
        "critical_regulatory_exposure_spend_usd": round(critical_spend, 2),
        "critical_spend_exposure_percentage": compliance_exposure_pct,
        "domain_health_scores": domain_scores,
        "business_unit_breakdown": bu_summary.to_dict(orient="records"),
        "top_rule_failures": rule_summary_df.head(6).to_dict(orient="records"),
        "disclaimer": "ALL DATA AND METRICS ARE 100% SYNTHETIC FOR SIMULATION PURPOSES"
    }

    summary_json_path = os.path.join(DATA_DIR, "dq_audit_summary.json")
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary_json, f, indent=2)
    print(f"Exported JSON Audit Summary: {summary_json_path}")

    return df, rule_summary_df, bu_summary, summary_json

if __name__ == "__main__":
    df, rule_summary_df, bu_summary, summary_json = run_data_quality_audit()
    print("=" * 60)
    print(f"AUDIT COMPLETE | OVERALL ACCURACY: {summary_json['overall_accuracy_percentage']}%")
    print(f"Total Records: {summary_json['total_records_audited']} | Clean: {summary_json['clean_records_count']} | Flagged: {summary_json['flagged_records_count']}")
    print(f"Total Audited Spend: ${summary_json['total_expenditure_audited_usd']:,.2f}")
    print(f"Sunshine/EFPIA Exposure At Risk: ${summary_json['critical_regulatory_exposure_spend_usd']:,.2f} ({summary_json['critical_spend_exposure_percentage']}%)")
    print("=" * 60)
