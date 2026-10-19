"""
Native Excel Formula & Conditional Formatting Validator Generator
Creates a standalone Excel workbook (excel_vba_formula_check.xlsx)
where all Data Quality checks and accuracy percentages are computed
PURELY USING NATIVE EXCEL FORMULAS without needing Python runtime!

[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def create_formula_audit_workbook():
    raw_csv = os.path.join(DATA_DIR, "synthetic_meetings_raw.csv")
    df = pd.read_csv(raw_csv).head(100) # 100 sample records for pure formula demonstration

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Native_Excel_Formula_Audit"
    ws.views.sheetView[0].showGridLines = True

    # Styling
    NAVY = "0F172A"
    TEAL = "0D9488"
    CRIT_FILL = "FEE2E2"
    CRIT_TEXT = "991B1B"
    CLEAN_FILL = "DCFCE7"
    CLEAN_TEXT = "166534"
    CARD_BG = "F1F5F9"
    BORDER_COLOR = "CBD5E1"

    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )

    # Title
    ws.merge_cells("A1:K1")
    ws["A1"] = "MERIDIAN BIOPHARMA GLOBAL OPERATIONS | PURE NATIVE EXCEL FORMULA AUDITOR"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="0F172A")

    ws.merge_cells("A2:K2")
    ws["A2"] = "Live formula-driven audit demonstrating client-side Excel validation rules without Python backend"
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="64748B")

    # Formula Summary KPI Cards
    # Total Records: =COUNTA(A7:A106)
    # Clean Records: =COUNTIF(AF7:AF106, "CLEAN")
    # Accuracy %: =COUNTIF(AF7:AF106, "CLEAN")/COUNTA(A7:A106)
    kpis = [
        ("TOTAL MEETINGS", "=COUNTA(A7:A106)", "A4:B4", "0"),
        ("CLEAN RECORDS", '=COUNTIF(AF7:AF106, "CLEAN")', "C4:D4", "0"),
        ("FLAGGED DEFICIENCIES", '=COUNTIF(AF7:AF106, "FLAGGED")', "E4:F4", "0"),
        ("PORTFOLIO ACCURACY %", '=COUNTIF(AF7:AF106, "CLEAN")/COUNTA(A7:A106)', "G4:H4", "0.0%"),
    ]

    for title, formula, rng, num_fmt in kpis:
        c1, c2 = rng.split(":")
        col1 = c1[0]
        col2 = c2[0]
        ws[f"{col1}3"] = title
        ws[f"{col1}3"].font = Font(name="Calibri", size=9, bold=True, color="475569")
        ws[f"{col1}3"].alignment = Alignment(horizontal="center")
        
        ws[f"{col1}4"] = formula
        ws[f"{col1}4"].font = Font(name="Calibri", size=16, bold=True, color=TEAL if "%" in num_fmt else NAVY)
        ws[f"{col1}4"].number_format = num_fmt
        ws[f"{col1}4"].alignment = Alignment(horizontal="center")

        for r in range(3, 5):
            for c in range(openpyxl.utils.column_index_from_string(col1), openpyxl.utils.column_index_from_string(col2) + 1):
                cell = ws.cell(row=r, column=c)
                cell.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
                cell.border = thin_border

    # Headers at Row 6
    data_cols = [
        ("Meeting_ID", "A"), ("Business_Unit", "B"), ("Meeting_Type", "C"), ("Cost_Center", "D"),
        ("WBS_Code", "E"), ("Country_Code", "F"), ("Start_Date", "G"), ("End_Date", "H"),
        ("Lead_Time_Days", "I"), ("Spend_Variance_Pct", "J"), ("Actual_Spend_USD", "K"),
        ("Budget_Estimated_USD", "L"), ("Payment_Method", "M"), ("Card_Reconciled", "N"),
        ("HCP_Count", "O"), ("HCP_NPIs", "P"), ("FMV_Compliant", "Q"), ("Cross_Border", "R"),
        ("Cvent_ID", "S"), ("Concur_ID", "T"), ("Roster_Captured", "U"), ("Days_To_Roster", "V"),
        ("Sunshine_Reportable", "W"), ("Compliance_Status", "X")
    ]

    for idx, (col_name, col_let) in enumerate(data_cols, start=1):
        cell = ws.cell(row=6, column=idx, value=col_name)
        cell.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
        cell.alignment = Alignment(horizontal="center")

    # Formula Headers (Columns Y to AF)
    formula_headers = [
        ("CHK_CORE_ID", "Y", "Check Core IDs Not Blank"),
        ("CHK_DATES", "Z", "End Date >= Start Date"),
        ("CHK_CVENT_SMM", "AA", "Cvent ID Present if HCP > 0"),
        ("CHK_US_NPI", "AB", "US NPI Present if HCP > 0"),
        ("CHK_CARD_RECON", "AC", "Ghost/Virtual Card Reconciled"),
        ("CHK_ROSTER_LAG", "AD", "Roster Captured <= 14 Days"),
        ("CHK_VARIANCE", "AE", "Spend Variance <= 25%"),
        ("RECORD_STATUS", "AF", "Live Formula Quality Flag")
    ]

    for col_title, col_let, tooltip in formula_headers:
        col_idx = openpyxl.utils.column_index_from_string(col_let)
        cell = ws.cell(row=6, column=col_idx, value=col_title)
        cell.font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=TEAL, end_color=TEAL, fill_type="solid")
        cell.alignment = Alignment(horizontal="center")

    # Populate Data & Live Excel Formulas
    for r_idx, (_, row) in enumerate(df.iterrows(), start=7):
        # Raw data insertion
        ws[f"A{r_idx}"] = str(row["Meeting_ID"])
        ws[f"B{r_idx}"] = str(row["Business_Unit"])
        ws[f"C{r_idx}"] = str(row["Meeting_Type"])
        ws[f"D{r_idx}"] = str(row["Cost_Center"])
        ws[f"E{r_idx}"] = str(row["WBS_Code"]) if pd.notna(row["WBS_Code"]) else ""
        ws[f"F{r_idx}"] = str(row["Country_Code"])
        ws[f"G{r_idx}"] = str(row["Start_Date"])
        ws[f"H{r_idx}"] = str(row["End_Date"])
        ws[f"I{r_idx}"] = int(row["Creation_Lead_Time_Days"]) if pd.notna(row["Creation_Lead_Time_Days"]) else 0
        ws[f"J{r_idx}"] = round(float(row["Spend_Variance_Pct"]), 2)
        ws[f"K{r_idx}"] = round(float(row["Actual_Spend_USD"]), 2)
        ws[f"L{r_idx}"] = round(float(row["Budget_Estimated_USD"]), 2)
        ws[f"M{r_idx}"] = str(row["Payment_Method"])
        ws[f"N{r_idx}"] = str(row["Corporate_Card_Reconciled_Flag"])
        ws[f"O{r_idx}"] = int(row["HCP_Attendees_Count"])
        ws[f"P{r_idx}"] = str(row["HCP_NPI_Numbers"]) if pd.notna(row["HCP_NPI_Numbers"]) else ""
        ws[f"Q{r_idx}"] = str(row["FMV_Tier_Compliant_Flag"])
        ws[f"R{r_idx}"] = str(row["Cross_Border_HCP_Flag"])
        ws[f"S{r_idx}"] = str(row["Cvent_Registration_ID"]) if pd.notna(row["Cvent_Registration_ID"]) else ""
        ws[f"T{r_idx}"] = str(row["Concur_Expense_Report_ID"]) if pd.notna(row["Concur_Expense_Report_ID"]) else ""
        ws[f"U{r_idx}"] = str(row["Post_Event_Roster_Captured"])
        ws[f"V{r_idx}"] = int(row["Days_To_Roster_Submission"]) if pd.notna(row["Days_To_Roster_Submission"]) else 0
        ws[f"W{r_idx}"] = str(row["EFPIA_Sunshine_Reportable"])
        ws[f"X{r_idx}"] = str(row["Compliance_Approval_Status"])

        # PURE NATIVE EXCEL FORMULAS:
        # Y: CHK_CORE_ID -> =IF(OR(ISBLANK(A{r}), ISBLANK(D{r}), ISBLANK(E{r})), "FAIL", "PASS")
        ws[f"Y{r_idx}"] = f'=IF(OR(ISBLANK(A{r_idx}), ISBLANK(D{r_idx}), ISBLANK(E{r_idx})), "FAIL", "PASS")'
        
        # Z: CHK_DATES -> =IF(H{r} < G{r}, "FAIL", "PASS")
        ws[f"Z{r_idx}"] = f'=IF(H{r_idx}<G{r_idx}, "FAIL", "PASS")'
        
        # AA: CHK_CVENT_SMM -> =IF(AND(O{r}>0, ISBLANK(S{r})), "FAIL", "PASS")
        ws[f"AA{r_idx}"] = f'=IF(AND(O{r_idx}>0, S{r_idx}=""), "FAIL", "PASS")'
        
        # AB: CHK_US_NPI -> =IF(AND(F{r}="US", O{r}>0, P{r}=""), "FAIL", "PASS")
        ws[f"AB{r_idx}"] = f'=IF(AND(F{r_idx}="US", O{r_idx}>0, P{r_idx}=""), "FAIL", "PASS")'
        
        # AC: CHK_CARD_RECON -> =IF(AND(OR(M{r}="Amex_BTA_Ghost", M{r}="Single_Use_Virtual_Card"), N{r}="N"), "FAIL", "PASS")
        ws[f"AC{r_idx}"] = f'=IF(AND(OR(M{r_idx}="Amex_BTA_Ghost", M{r_idx}="Single_Use_Virtual_Card"), N{r_idx}="N"), "FAIL", "PASS")'
        
        # AD: CHK_ROSTER_LAG -> =IF(OR(U{r}="N", V{r}>14), "FAIL", "PASS")
        ws[f"AD{r_idx}"] = f'=IF(OR(U{r_idx}="N", V{r_idx}>14), "FAIL", "PASS")'
        
        # AE: CHK_VARIANCE -> =IF(J{r}>25, "FAIL", "PASS")
        ws[f"AE{r_idx}"] = f'=IF(J{r_idx}>25, "FAIL", "PASS")'
        
        # AF: RECORD_STATUS -> =IF(COUNTIF(Y{r}:AE{r}, "FAIL")=0, "CLEAN", "FLAGGED")
        ws[f"AF{r_idx}"] = f'=IF(COUNTIF(Y{r_idx}:AE{r_idx}, "FAIL")=0, "CLEAN", "FLAGGED")'

        for col_idx in range(1, 33):
            cell = ws.cell(row=r_idx, column=col_idx)
            cell.border = thin_border
            cell.font = Font(name="Calibri", size=9)
            if col_idx in range(25, 32):
                cell.alignment = Alignment(horizontal="center")
            if col_idx == 32:
                cell.alignment = Alignment(horizontal="center")

    # Column widths
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = 14
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["AF"].width = 16

    out_path = os.path.join(DATA_DIR, "excel_vba_formula_check.xlsx")
    wb.save(out_path)
    print(f"Generated Pure Native Excel Formula Auditor: {out_path}")
    return out_path

if __name__ == "__main__":
    create_formula_audit_workbook()
