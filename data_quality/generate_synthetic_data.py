"""
Synthetic Meeting Records Generator for Meridian BioPharma Global Operations
Generates realistic, complex pharmaceutical meeting records with deliberate,
statistically controlled data anomalies across travel, meetings, card, and fleet domains.

[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RANDOM_SEED = 42

def generate_synthetic_dataset(num_records=1500, anomaly_rate=0.26):
    np.random.seed(RANDOM_SEED)
    random.seed(RANDOM_SEED)

    business_units = [
        {"name": "Oncology", "prefix": "ONC", "cc": "CC-ONC-8821", "wbs": "WBS-ONC-302-CLIN"},
        {"name": "Immunology_Inflammation", "prefix": "IMM", "cc": "CC-IMM-4102", "wbs": "WBS-IMM-108-PH3"},
        {"name": "Rare_Disease", "prefix": "RD", "cc": "CC-RD-9014", "wbs": "WBS-RD-401-REG"},
        {"name": "Vaccines_Infectious", "prefix": "VAC", "cc": "CC-VAC-6311", "wbs": "WBS-VAC-205-GLB"},
    ]

    meeting_types = [
        {"type": "Advisory_Board", "hcp_likely": True, "avg_spend": 85000, "weight": 0.28},
        {"type": "Investigator_Meeting", "hcp_likely": True, "avg_spend": 195000, "weight": 0.22},
        {"type": "Medical_Symposium", "hcp_likely": True, "avg_spend": 140000, "weight": 0.20},
        {"type": "Commercial_Launch", "hcp_likely": True, "avg_spend": 260000, "weight": 0.12},
        {"type": "Internal_Sales_Rally", "hcp_likely": False, "avg_spend": 110000, "weight": 0.12},
        {"type": "Satellite_Symposium", "hcp_likely": True, "avg_spend": 65000, "weight": 0.06},
    ]

    countries = ["US", "GB", "DE", "FR", "JP", "CH"]
    country_weights = [0.45, 0.16, 0.14, 0.10, 0.08, 0.07]

    payment_methods = [
        ("Single_Use_Virtual_Card", 0.45),
        ("Amex_BTA_Ghost", 0.30),
        ("Corporate_T&E_Card", 0.15),
        ("Direct_Invoice_PO", 0.10),
    ]

    base_date = datetime(2026, 1, 5)
    records = []

    m_type_choices = [m["type"] for m in meeting_types]
    m_type_probs = [m["weight"] for m in meeting_types]

    pay_choices = [p[0] for p in payment_methods]
    pay_probs = [p[1] for p in payment_methods]

    for i in range(1, num_records + 1):
        bu = random.choice(business_units)
        m_type_str = np.random.choice(m_type_choices, p=m_type_probs)
        m_type_meta = next(m for m in meeting_types if m["type"] == m_type_str)
        country = np.random.choice(countries, p=country_weights)

        # Dates
        start_offset = random.randint(10, 260)
        start_date = base_date + timedelta(days=start_offset)
        duration = random.randint(1, 4)
        end_date = start_date + timedelta(days=duration)
        lead_time_days = random.randint(18, 90)

        meeting_id = f"MTG-2026-{10000 + i}"
        meeting_name = f"{bu['name'].replace('_', ' ')} {m_type_str.replace('_', ' ')} ({country})"
        requester_id = f"EMP-{random.randint(2000, 8999)}"

        # Financials
        budget = round(random.gauss(m_type_meta["avg_spend"], m_type_meta["avg_spend"] * 0.25), -2)
        budget = max(15000.0, budget)
        variance_factor = random.gauss(1.02, 0.08)
        actual_spend = round(budget * variance_factor, 2)
        variance_pct = round(((actual_spend - budget) / budget) * 100, 2)

        # HCP specifics
        is_hcp = m_type_meta["hcp_likely"]
        if is_hcp:
            hcp_count = random.randint(4, 35)
            # Generate realistic 10-digit NPIs or EFPIA IDs
            if country == "US":
                npis = ";".join([f"1{random.randint(100000000, 999999999)}" for _ in range(hcp_count)])
            else:
                npis = ";".join([f"EFPIA-{country}-{random.randint(100000, 999999)}" for _ in range(hcp_count)])
            fmv_compliant = "Y"
            cross_border = "Y" if random.random() < 0.28 else "N"
            sunshine_reportable = "Y"
        else:
            hcp_count = 0
            npis = ""
            fmv_compliant = "N/A"
            cross_border = "N"
            sunshine_reportable = "N"

        # Identifiers
        cvent_id = f"CVT-{random.randint(100000, 999999)}"
        concur_id = f"EXP-2026-{random.randint(100000, 999999)}"
        payment_method = np.random.choice(pay_choices, p=pay_probs)
        card_reconciled = "Y" if random.random() < 0.88 else "Pending"

        # Post event
        roster_captured = "Y"
        days_to_roster = random.randint(2, 11)

        # Fleet
        fleet_utilized = "Y" if random.random() < 0.45 else "N"
        if fleet_utilized == "Y":
            co2_kg = round(random.uniform(22.0, 185.0), 1)
        else:
            co2_kg = 0.0

        compliance_status = "Approved"

        # INJECT CONTROLLED ENTERPRISE ANOMALIES (approx 24-26% of records)
        if random.random() < anomaly_rate:
            anomaly_type = random.choice([
                "ROGUE_CVENT_BYPASS",
                "MISSING_HCP_NPI",
                "INVALID_NPI_FORMAT",
                "DATE_CHRONOLOGY_FLIP",
                "RETROACTIVE_REQUEST",
                "ROSTER_LAG_EXCEEDED",
                "CARD_UNRECONCILED_AGED",
                "CONCUR_ID_MISSING",
                "FMV_COMPLIANCE_BREACH",
                "CROSS_BORDER_UNAPPROVED",
                "WBS_CODE_MISSING",
                "BUDGET_OVERRUN_NO_APPROVAL",
                "FLEET_CO2_MISSING",
                "EFPIA_COUNTRY_MISMATCH"
            ])

            if anomaly_type == "ROGUE_CVENT_BYPASS" and is_hcp:
                cvent_id = ""  # DLP-1: Off-channel booking
            elif anomaly_type == "MISSING_HCP_NPI" and is_hcp and hcp_count > 0:
                npis = ""  # DLP-2: Missing HCP identifiers
            elif anomaly_type == "INVALID_NPI_FORMAT" and is_hcp and country == "US":
                npis = f"NPI_UNKNOWN_{random.randint(10, 99)}"  # Invalid format
            elif anomaly_type == "DATE_CHRONOLOGY_FLIP":
                end_date = start_date - timedelta(days=random.randint(1, 3))  # End before start
            elif anomaly_type == "RETROACTIVE_REQUEST":
                lead_time_days = -random.randint(2, 14)  # Submitted after event
            elif anomaly_type == "ROSTER_LAG_EXCEEDED":
                roster_captured = "N"
                days_to_roster = random.randint(28, 75)  # DLP-5: Delinquent roster
            elif anomaly_type == "CARD_UNRECONCILED_AGED":
                payment_method = "Amex_BTA_Ghost"
                card_reconciled = "N"  # DLP-4: Unreconciled card
            elif anomaly_type == "CONCUR_ID_MISSING":
                concur_id = ""  # Expense report never linked
                card_reconciled = "N"
            elif anomaly_type == "FMV_COMPLIANCE_BREACH" and is_hcp:
                fmv_compliant = "N"  # Approved despite non-compliant honoraria
                compliance_status = "Approved"
            elif anomaly_type == "CROSS_BORDER_UNAPPROVED" and is_hcp:
                cross_border = "Y"
                compliance_status = "Conditional"  # DLP-7: Cross-border unapproved
            elif anomaly_type == "WBS_CODE_MISSING":
                bu_wbs = ""  # DLP-6: Missing project WBS code
            elif anomaly_type == "BUDGET_OVERRUN_NO_APPROVAL":
                actual_spend = round(budget * random.uniform(1.35, 1.80), 2)
                variance_pct = round(((actual_spend - budget) / budget) * 100, 2)
            elif anomaly_type == "FLEET_CO2_MISSING":
                fleet_utilized = "Y"
                co2_kg = np.nan  # DLP-3: Unmetered CO2
            elif anomaly_type == "EFPIA_COUNTRY_MISMATCH":
                if country == "US":
                    sunshine_reportable = "N"  # Sunshine act required in US!
                else:
                    sunshine_reportable = "N"
        else:
            bu_wbs = bu["wbs"]

        wbs_val = bu_wbs if "bu_wbs" in locals() and bu_wbs else bu["wbs"]

        records.append({
            "Meeting_ID": meeting_id,
            "Meeting_Name": meeting_name,
            "Meeting_Type": m_type_str,
            "Business_Unit": bu["name"],
            "Cost_Center": bu["cc"],
            "WBS_Code": wbs_val,
            "Requester_ID": requester_id,
            "Country_Code": country,
            "Start_Date": start_date.strftime("%Y-%m-%d"),
            "End_Date": end_date.strftime("%Y-%m-%d"),
            "Creation_Lead_Time_Days": lead_time_days,
            "Budget_Estimated_USD": budget,
            "Actual_Spend_USD": actual_spend,
            "Spend_Variance_Pct": variance_pct,
            "Payment_Method": payment_method,
            "Corporate_Card_Reconciled_Flag": card_reconciled,
            "HCP_Attendees_Count": hcp_count,
            "HCP_NPI_Numbers": npis,
            "FMV_Tier_Compliant_Flag": fmv_compliant,
            "Cross_Border_HCP_Flag": cross_border,
            "Cvent_Registration_ID": cvent_id,
            "Concur_Expense_Report_ID": concur_id,
            "Post_Event_Roster_Captured": roster_captured,
            "Days_To_Roster_Submission": days_to_roster,
            "EFPIA_Sunshine_Reportable": sunshine_reportable,
            "Fleet_Ground_Transfer_Utilized": fleet_utilized,
            "Fleet_CO2_Emissions_kg": co2_kg,
            "Compliance_Approval_Status": compliance_status
        })

    df = pd.DataFrame(records)
    out_path = os.path.join(DATA_DIR, "synthetic_meetings_raw.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated synthetic meeting dataset: {out_path} ({len(df)} records)")
    return df

if __name__ == "__main__":
    generate_synthetic_dataset()
