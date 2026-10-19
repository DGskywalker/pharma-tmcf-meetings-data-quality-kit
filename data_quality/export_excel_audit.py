"""
Advanced Excel Workbook Exporter for Meridian BioPharma Global Operations
Builds an executive-grade, multi-tab audit workbook using openpyxl:
1. Executive_Dashboard (KPI scorecards, domain health, rule failure Pareto)
2. Flagged_Audit_Register (1,500 records with conditional formatting)
3. Business_Unit_Performance (Segmented accuracy and financial exposure)
4. Rules_Dictionary (Comprehensive DQ specifications and DLP mappings)

[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def create_styled_excel(df, rule_summary_df, bu_summary, summary_json):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Corporate Color Palette
    NAVY_HEADER = "0F172A"
    SLATE_SUB = "1E293B"
    TEAL_ACCENT = "0D9488"
    LIGHT_BG = "F8FAFC"
    CARD_BG = "F1F5F9"
    BORDER_COLOR = "CBD5E1"
    
    CRIT_FILL = "FEE2E2"
    CRIT_TEXT = "991B1B"
    WARN_FILL = "FEF3C7"
    WARN_TEXT = "92400E"
    CLEAN_FILL = "DCFCE7"
    CLEAN_TEXT = "166534"

    font_title = Font(name="Calibri", size=16, bold=True, color="0F172A")
    font_subtitle = Font(name="Calibri", size=10, italic=True, color="64748B")
    font_card_num = Font(name="Calibri", size=20, bold=True, color="0F172A")
    font_card_lbl = Font(name="Calibri", size=9, bold=True, color="475569")
    font_tbl_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
    font_regular = Font(name="Calibri", size=10, color="1E293B")

    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )

    header_fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    teal_fill = PatternFill(start_color=TEAL_ACCENT, end_color=TEAL_ACCENT, fill_type="solid")
    card_fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    # ==========================================
    # SHEET 1: EXECUTIVE DASHBOARD
    # ==========================================
    ws_dash = wb.create_sheet(title="Executive_Dashboard")
    ws_dash.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_dash.merge_cells("B2:J2")
    ws_dash["B2"] = "MERIDIAN BIOPHARMA GLOBAL OPERATIONS | DATA QUALITY & ENGAGEMENT AUDIT"
    ws_dash["B2"].font = font_title

    ws_dash.merge_cells("B3:J3")
    ws_dash["B3"] = "Automated Health Scorecard, Compliance Exposure & Data Leakage Point (DLP) Surveillance | [SYNTHETIC DATA]"
    ws_dash["B3"].font = font_subtitle

    # KPI Scorecard Cards
    kpis = [
        ("OVERALL ACCURACY", f"{summary_json['overall_accuracy_percentage']}%", "B5:C6", "B5", "B6"),
        ("HEALTH INDEX", f"{summary_json['weighted_data_health_index']}/100", "D5:E6", "D5", "D6"),
        ("TOTAL AUDITED SPEND", f"${summary_json['total_expenditure_audited_usd']:,.0f}", "F5:G6", "F5", "F6"),
        ("SUNSHINE EXPOSURE", f"${summary_json['critical_regulatory_exposure_spend_usd']:,.0f}", "H5:I5", "H5", "H6"),
        ("FLAGGED MEETINGS", f"{summary_json['flagged_records_count']} / {summary_json['total_records_audited']}", "J5:K6", "J5", "J6"),
    ]

    for title, val, rng, cell_lbl, cell_val in kpis:
        c1, c2 = rng.split(":")
        col1 = c1[0]
        col2 = c2[0] if len(c2) == 2 else c2[:2]
        
        # Merge for title
        ws_dash[f"{col1}5"] = title
        ws_dash[f"{col1}5"].font = font_card_lbl
        ws_dash[f"{col1}5"].alignment = Alignment(horizontal="center", vertical="center")
        
        # Merge for value
        ws_dash[f"{col1}6"] = val
        ws_dash[f"{col1}6"].font = font_card_num
        ws_dash[f"{col1}6"].alignment = Alignment(horizontal="center", vertical="center")

        for row in range(5, 7):
            for col_idx in range(openpyxl.utils.column_index_from_string(col1), openpyxl.utils.column_index_from_string(col2) + 1):
                cell = ws_dash.cell(row=row, column=col_idx)
                cell.fill = card_fill
                cell.border = thin_border

    # Table 1: Top Rule Failures Pareto
    ws_dash.cell(row=8, column=2, value="TOP DATA QUALITY DEFICIENCIES (PARETO SURVEILLANCE)").font = font_bold
    
    rule_headers = ["Rule Code", "Rule Name", "Dimension", "Domain", "Severity", "DLP Ref", "Failures", "Fail %"]
    for c_idx, h_text in enumerate(rule_headers, start=2):
        cell = ws_dash.cell(row=9, column=c_idx, value=h_text)
        cell.font = font_tbl_hdr
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center" if c_idx in [6, 7, 8, 9] else "left")

    for r_idx, (_, r_data) in enumerate(rule_summary_df.head(10).iterrows(), start=10):
        ws_dash.cell(row=r_idx, column=2, value=r_data["Rule_Code"]).font = font_regular
        ws_dash.cell(row=r_idx, column=3, value=r_data["Rule_Name"]).font = font_regular
        ws_dash.cell(row=r_idx, column=4, value=r_data["Dimension"]).font = font_regular
        ws_dash.cell(row=r_idx, column=5, value=r_data["Domain"]).font = font_regular
        
        sev_cell = ws_dash.cell(row=r_idx, column=6, value=r_data["Severity"])
        sev_cell.alignment = Alignment(horizontal="center")
        if r_data["Severity"] == "CRITICAL":
            sev_cell.fill = PatternFill(start_color=CRIT_FILL, end_color=CRIT_FILL, fill_type="solid")
            sev_cell.font = Font(name="Calibri", size=10, bold=True, color=CRIT_TEXT)
        elif r_data["Severity"] == "HIGH":
            sev_cell.fill = PatternFill(start_color=WARN_FILL, end_color=WARN_FILL, fill_type="solid")
            sev_cell.font = Font(name="Calibri", size=10, bold=True, color=WARN_TEXT)
        else:
            sev_cell.font = font_regular

        ws_dash.cell(row=r_idx, column=7, value=r_data["DLP_Reference"]).font = font_regular
        ws_dash.cell(row=r_idx, column=8, value=r_data["Failure_Count"]).font = font_bold
        ws_dash.cell(row=r_idx, column=8).alignment = Alignment(horizontal="right")
        ws_dash.cell(row=r_idx, column=9, value=f"{r_data['Failure_Rate_Pct']}%").font = font_regular
        ws_dash.cell(row=r_idx, column=9).alignment = Alignment(horizontal="right")

        for col_idx in range(2, 10):
            ws_dash.cell(row=r_idx, column=col_idx).border = thin_border

    # Table 2: Business Unit Performance Summary
    start_bu_row = 22
    ws_dash.cell(row=start_bu_row, column=2, value="BUSINESS UNIT HEALTH & REGULATORY SPEND AT RISK").font = font_bold
    
    bu_headers = ["Business Unit", "Audited Meetings", "Clean Meetings", "Accuracy %", "Total Spend ($)", "Spend at Risk ($)", "Exposure %"]
    for c_idx, h_text in enumerate(bu_headers, start=2):
        cell = ws_dash.cell(row=start_bu_row + 1, column=c_idx, value=h_text)
        cell.font = font_tbl_hdr
        cell.fill = teal_fill
        cell.alignment = Alignment(horizontal="center" if c_idx in [3, 4, 5, 8] else "left")

    for r_idx, (_, b_data) in enumerate(bu_summary.iterrows(), start=start_bu_row + 2):
        ws_dash.cell(row=r_idx, column=2, value=b_data["Business_Unit"]).font = font_regular
        ws_dash.cell(row=r_idx, column=3, value=int(b_data["Total_Meetings"])).font = font_regular
        ws_dash.cell(row=r_idx, column=4, value=int(b_data["Clean_Meetings"])).font = font_regular
        
        acc_cell = ws_dash.cell(row=r_idx, column=5, value=f"{b_data['Accuracy_Pct']}%")
        acc_cell.font = font_bold
        acc_cell.alignment = Alignment(horizontal="right")
        
        ws_dash.cell(row=r_idx, column=6, value=f"${b_data['Total_Spend_USD']:,.2f}").font = font_regular
        ws_dash.cell(row=r_idx, column=6).alignment = Alignment(horizontal="right")

        ws_dash.cell(row=r_idx, column=7, value=f"${b_data['Critical_Spend_USD']:,.2f}").font = font_bold
        ws_dash.cell(row=r_idx, column=7).alignment = Alignment(horizontal="right")

        exp_cell = ws_dash.cell(row=r_idx, column=8, value=f"{b_data['Critical_Spend_Exposure_Pct']}%")
        exp_cell.font = Font(name="Calibri", size=10, bold=True, color=CRIT_TEXT)
        exp_cell.alignment = Alignment(horizontal="right")

        for col_idx in range(2, 9):
            ws_dash.cell(row=r_idx, column=col_idx).border = thin_border

    # Adjust Dashboard Column Widths
    for col in ws_dash.columns:
        col_letter = get_column_letter(col[0].column)
        ws_dash.column_dimensions[col_letter].width = 18

    # ==========================================
    # SHEET 2: FLAGGED AUDIT REGISTER
    # ==========================================
    ws_reg = wb.create_sheet(title="Flagged_Audit_Register")
    ws_reg.views.sheetView[0].showGridLines = True

    # Order of columns to display
    display_cols = [
        "Meeting_ID", "Business_Unit", "Meeting_Type", "Country_Code", "Start_Date", "End_Date",
        "Creation_Lead_Time_Days", "Budget_Estimated_USD", "Actual_Spend_USD", "Spend_Variance_Pct",
        "Payment_Method", "Corporate_Card_Reconciled_Flag", "HCP_Attendees_Count", "HCP_NPI_Numbers",
        "FMV_Tier_Compliant_Flag", "Cross_Border_HCP_Flag", "Cvent_Registration_ID", "Concur_Expense_Report_ID",
        "Post_Event_Roster_Captured", "Days_To_Roster_Submission", "EFPIA_Sunshine_Reportable",
        "Fleet_Ground_Transfer_Utilized", "Fleet_CO2_Emissions_kg", "Compliance_Approval_Status",
        "Is_Clean_Record", "Error_Count", "Error_Codes", "Has_Critical_Error", "Penalty_Score"
    ]

    # Write Headers
    for c_idx, col_name in enumerate(display_cols, start=1):
        cell = ws_reg.cell(row=1, column=c_idx, value=col_name)
        cell.font = font_tbl_hdr
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Write Data with Conditional Formatting
    for r_idx, (_, row) in enumerate(df.iterrows(), start=2):
        is_clean = row["Is_Clean_Record"]
        has_crit = row["Has_Critical_Error"] == "Y"
        has_hi = row["Has_High_Error"] == "Y"

        row_fill = None
        text_color = "000000"
        if has_crit:
            row_fill = PatternFill(start_color=CRIT_FILL, end_color=CRIT_FILL, fill_type="solid")
            text_color = CRIT_TEXT
        elif has_hi:
            row_fill = PatternFill(start_color=WARN_FILL, end_color=WARN_FILL, fill_type="solid")
            text_color = WARN_TEXT
        elif is_clean:
            row_fill = PatternFill(start_color=CLEAN_FILL, end_color=CLEAN_FILL, fill_type="solid")
            text_color = CLEAN_TEXT

        for c_idx, col_name in enumerate(display_cols, start=1):
            val = row[col_name]
            cell = ws_reg.cell(row=r_idx, column=c_idx)
            
            # Format types
            if pd.isna(val):
                cell.value = ""
            elif isinstance(val, (int, np.integer)):
                cell.value = int(val)
            elif isinstance(val, (float, np.floating)):
                cell.value = round(float(val), 2)
            elif isinstance(val, bool):
                cell.value = "TRUE" if val else "FALSE"
            else:
                cell.value = str(val)

            cell.font = Font(name="Calibri", size=9, color=text_color if c_idx in [1, 25, 26, 27, 28] else "0F172A")
            if row_fill and c_idx in [1, 25, 26, 27, 28]:
                cell.fill = row_fill
            cell.border = thin_border

    # Auto-filter on register
    ws_reg.auto_filter.ref = f"A1:{get_column_letter(len(display_cols))}{len(df) + 1}"

    for col in ws_reg.columns:
        col_letter = get_column_letter(col[0].column)
        ws_reg.column_dimensions[col_letter].width = 15

    # ==========================================
    # SHEET 3: RULES DICTIONARY
    # ==========================================
    ws_rules = wb.create_sheet(title="Rules_Dictionary")
    ws_rules.views.sheetView[0].showGridLines = True

    rule_cols = ["Rule_Code", "Rule_Name", "Dimension", "Domain", "Severity", "Penalty_Weight", "DLP_Reference", "Description"]
    for c_idx, col_name in enumerate(rule_cols, start=1):
        cell = ws_rules.cell(row=1, column=c_idx, value=col_name)
        cell.font = font_tbl_hdr
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    from dq_rules_engine import RULES_SPECIFICATION
    for r_idx, (r_code, r_meta) in enumerate(RULES_SPECIFICATION.items(), start=2):
        ws_rules.cell(row=r_idx, column=1, value=r_code).font = font_bold
        ws_rules.cell(row=r_idx, column=2, value=r_meta["name"]).font = font_regular
        ws_rules.cell(row=r_idx, column=3, value=r_meta["dimension"]).font = font_regular
        ws_rules.cell(row=r_idx, column=4, value=r_meta["domain"]).font = font_regular
        
        sev_c = ws_rules.cell(row=r_idx, column=5, value=r_meta["severity"])
        sev_c.alignment = Alignment(horizontal="center")
        if r_meta["severity"] == "CRITICAL":
            sev_c.fill = PatternFill(start_color=CRIT_FILL, end_color=CRIT_FILL, fill_type="solid")
            sev_c.font = Font(name="Calibri", size=10, bold=True, color=CRIT_TEXT)
        elif r_meta["severity"] == "HIGH":
            sev_c.fill = PatternFill(start_color=WARN_FILL, end_color=WARN_FILL, fill_type="solid")
            sev_c.font = Font(name="Calibri", size=10, bold=True, color=WARN_TEXT)
        else:
            sev_c.font = font_regular

        ws_rules.cell(row=r_idx, column=6, value=r_meta["weight"]).font = font_regular
        ws_rules.cell(row=r_idx, column=6).alignment = Alignment(horizontal="right")
        ws_rules.cell(row=r_idx, column=7, value=r_meta["dlp"]).font = font_regular
        ws_rules.cell(row=r_idx, column=8, value=r_meta["description"]).font = font_regular

        for c_idx in range(1, 9):
            ws_rules.cell(row=r_idx, column=c_idx).border = thin_border

    for col in ws_rules.columns:
        col_letter = get_column_letter(col[0].column)
        ws_rules.column_dimensions[col_letter].width = 22
    ws_rules.column_dimensions["H"].width = 50

    # Save Workbook
    out_xlsx_path = os.path.join(DATA_DIR, "synthetic_meetings_audit.xlsx")
    wb.save(out_xlsx_path)
    print(f"Generated Executive Multi-Tab Audit Workbook: {out_xlsx_path}")
    return out_xlsx_path

if __name__ == "__main__":
    from dq_rules_engine import run_data_quality_audit
    df, rule_summary_df, bu_summary, summary_json = run_data_quality_audit()
    create_styled_excel(df, rule_summary_df, bu_summary, summary_json)
