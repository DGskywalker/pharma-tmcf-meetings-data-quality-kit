"""
Unified Data Quality Pipeline Runner for Meridian BioPharma Global Operations
Orchestrates synthetic generation, multi-dimensional validation,
Excel reporting, and executive visualization artifact creation.

[CONFIDENTIAL - FOR SIMULATION & DEMO PURPOSES ONLY - ALL DATA IS 100% SYNTHETIC]
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generate_synthetic_data import generate_synthetic_dataset
from dq_rules_engine import run_data_quality_audit, RULES_SPECIFICATION
from export_excel_audit import create_styled_excel
from export_native_excel_formulas import create_formula_audit_workbook

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def generate_visualizations(df, rule_summary_df, bu_summary, summary_json):
    """Generates publication-quality charts for the executive report and documentation."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # Chart 1: Top Rule Deficiencies (Pareto Horizontal Bar)
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    top_rules = rule_summary_df.head(8).iloc[::-1]
    
    colors = ["#DC2626" if s == "CRITICAL" else "#F59E0B" if s == "HIGH" else "#3B82F6" for s in top_rules["Severity"]]
    bars = ax.barh(top_rules["Rule_Name"], top_rules["Failure_Count"], color=colors, edgecolor="#0F172A", height=0.65)
    
    ax.set_title("Meridian BioPharma Global Operations: Top Meeting Data Quality Deficiencies", fontsize=13, fontweight="bold", pad=15, color="#0F172A")
    ax.set_xlabel("Number of Breached Meeting Records (out of 1,500 Audited)", fontsize=10, fontweight="bold", color="#334155")
    
    for bar in bars:
        w = bar.get_width()
        pct = (w / len(df)) * 100
        ax.text(w + 5, bar.get_y() + bar.get_height()/2, f"{int(w)} ({pct:.1f}%)", va="center", ha="left", fontsize=9, fontweight="bold", color="#1E293B")

    ax.set_xlim(0, max(top_rules["Failure_Count"]) * 1.22)
    plt.tight_layout()
    chart1_path = os.path.join(ASSETS_DIR, "dlp_breakdown.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"Generated Chart: {chart1_path}")

    # Chart 2: Accuracy & Critical Compliance Exposure by Business Unit
    fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
    bu_names = [b.replace("_", " ") for b in bu_summary["Business_Unit"]]
    acc_pcts = bu_summary["Accuracy_Pct"]
    exp_pcts = bu_summary["Critical_Spend_Exposure_Pct"]

    x = np.arange(len(bu_names))
    width = 0.35

    rects1 = ax1.bar(x - width/2, acc_pcts, width, label="Data Accuracy % (Clean)", color="#0D9488", edgecolor="#0F172A")
    rects2 = ax1.bar(x + width/2, exp_pcts, width, label="Sunshine Spend Exposure %", color="#E11D48", edgecolor="#0F172A")

    ax1.set_ylabel("Percentage (%)", fontsize=10, fontweight="bold", color="#0F172A")
    ax1.set_title("Data Accuracy vs. Regulatory Spend Exposure by Business Unit", fontsize=12, fontweight="bold", pad=15, color="#0F172A")
    ax1.set_xticks(x)
    ax1.set_xticklabels(bu_names, fontsize=9, fontweight="bold")
    ax1.set_ylim(0, 100)
    ax1.legend(loc="upper right", frameon=True)

    for rect in rects1:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#0D9488")
    for rect in rects2:
        h = rect.get_height()
        ax1.text(rect.get_x() + rect.get_width()/2, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#E11D48")

    plt.tight_layout()
    chart2_path = os.path.join(ASSETS_DIR, "accuracy_by_bu.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"Generated Chart: {chart2_path}")

    # Chart 3: Post-Event Attendee Roster Submission Aging
    fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
    roster_days = df[df["HCP_Attendees_Count"] > 0]["Days_To_Roster_Submission"].dropna()

    bins = [0, 7, 14, 21, 30, 60, 90]
    labels = ["0-7d (Optimal)", "8-14d (Compliant)", "15-21d (Warning)", "22-30d (Critical)", "31-60d (Delinquent)", "60d+ (Severe Breach)"]
    cuts = pd.cut(roster_days, bins=bins, labels=labels)
    cat_counts = cuts.value_counts()[labels]

    bar_colors = ["#10B981", "#34D399", "#FBBF24", "#F97316", "#EF4444", "#7F1D1D"]
    bars = ax.bar(labels, cat_counts.values, color=bar_colors, edgecolor="#0F172A", width=0.6)
    
    ax.set_title("Post-Event HCP Attendee Roster Submission Aging (SLA = 14 Days)", fontsize=12, fontweight="bold", pad=15)
    ax.set_ylabel("Number of Meetings", fontsize=10, fontweight="bold")
    ax.axvline(1.5, color="#DC2626", linestyle="--", linewidth=2, label="14-Day Mandatory Sunshine SLA")
    ax.legend(loc="upper right")
    plt.xticks(rotation=20, ha="right", fontsize=9)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 3, str(int(h)), ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart3_path = os.path.join(ASSETS_DIR, "roster_aging.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"Generated Chart: {chart3_path}")

    # Chart 4: Radar Chart across Governance Domains
    domains = ["Meetings\nSMM", "Corporate\nCard", "Medical\nCompliance", "Fleet &\nMobility", "Financial\nLedger", "Policy &\nTimeliness"]
    domain_keys = ["Meetings", "Card", "Compliance", "Fleet", "Financial", "Policy"]
    scores = [summary_json["domain_health_scores"].get(k, 80.0) for k in domain_keys]

    angles = np.linspace(0, 2 * np.pi, len(domains), endpoint=False).tolist()
    scores += scores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), dpi=300)
    ax.plot(angles, scores, color="#0D9488", linewidth=2.5, linestyle="solid")
    ax.fill(angles, scores, color="#0D9488", alpha=0.25)

    target_scores = [95.0] * (len(domains) + 1)
    ax.plot(angles, target_scores, color="#E11D48", linewidth=1.5, linestyle="dashed", label="Enterprise Target (95%)")

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(domains, fontsize=10, fontweight="bold", color="#1E293B")
    ax.set_title("Enterprise Domain Data Quality Radar Scorecard", fontsize=12, fontweight="bold", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    chart4_path = os.path.join(ASSETS_DIR, "compliance_radar.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"Generated Chart: {chart4_path}")


def run_full_pipeline():
    print("=" * 65)
    print("STARTING MERIDIAN BIOPHARMA GLOBAL MEETINGS DATA QUALITY PIPELINE")
    print("=" * 65)

    # 1. Generate Synthetic Dataset
    print("\n[STEP 1/4] Generating 1,500 synthetic meeting records...")
    df_raw = generate_synthetic_dataset(num_records=1500, anomaly_rate=0.26)

    # 2. Execute DQ Engine
    print("\n[STEP 2/4] Executing 16-Rule Multi-Dimensional DQ Engine...")
    df_flagged, rule_summary_df, bu_summary, summary_json = run_data_quality_audit()

    # 3. Export Excel Workbooks
    print("\n[STEP 3/4] Exporting formatted multi-tab audit workbooks...")
    xlsx_path = create_styled_excel(df_flagged, rule_summary_df, bu_summary, summary_json)
    formula_xlsx_path = create_formula_audit_workbook()

    # 4. Generate Visualizations
    print("\n[STEP 4/4] Generating executive analytics visualization suite...")
    generate_visualizations(df_flagged, rule_summary_df, bu_summary, summary_json)

    print("\n" + "=" * 65)
    print("PIPELINE EXECUTION COMPLETE | SUMMARY METRICS:")
    print(f"-> Audited Records: {summary_json['total_records_audited']}")
    print(f"-> Portfolio Accuracy: {summary_json['overall_accuracy_percentage']}% (Clean: {summary_json['clean_records_count']}, Flagged: {summary_json['flagged_records_count']})")
    print(f"-> Total Audited Spend: ${summary_json['total_expenditure_audited_usd']:,.2f}")
    print(f"-> Sunshine Act Exposure Spend: ${summary_json['critical_regulatory_exposure_spend_usd']:,.2f} ({summary_json['critical_spend_exposure_percentage']}%)")
    print(f"-> Master Excel Audit: {xlsx_path}")
    print(f"-> Native Formula Workbook: {formula_xlsx_path}")
    print("=" * 65)


if __name__ == "__main__":
    run_full_pipeline()
