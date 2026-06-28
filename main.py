"""
╔══════════════════════════════════════════════════════╗
║      AI SALES REPORTING AUTOMATION SYSTEM           ║
║      Built by Yaseer Al-Harbi                       ║
║      Powered by Python + Claude AI                  ║
╚══════════════════════════════════════════════════════╝

PIPELINE:
  1. Generate realistic sales data (2,000 records)
  2. Run analytics pipeline → KPIs + Anomaly Detection
  3. Generate Excel report (6 sheets + charts)
  4. Generate AI narrative report (Claude API)
  5. Generate interactive HTML dashboard

OUTPUTS (in /reports folder):
  • Sales_Report_2024.xlsx  — Full Excel report with charts
  • AI_Narrative_Report.txt — Claude AI analysis
  • Dashboard.html          — Interactive web dashboard
  • summary.json            — Structured data (for integrations)
"""

import os
import sys
import time

def separator(title=""):
    print(f"\n{'─'*55}")
    if title:
        print(f"  {title}")
    print('─'*55)


def main():
    print("""
╔══════════════════════════════════════════════════════╗
║      AI SALES REPORTING AUTOMATION SYSTEM           ║
╚══════════════════════════════════════════════════════╝""")

    start = time.time()

    # ── STEP 1: Generate Data ──────────────────────────────
    separator("STEP 1 — Generating Sales Data")
    from data_generator import generate_sales_data, save_data
    df = generate_sales_data(n_records=2000)
    save_data(df, output_dir="data")

    # ── STEP 2: Run Analytics Pipeline ────────────────────
    separator("STEP 2 — Running Analytics Pipeline")
    from analytics import run_pipeline
    kpis, breakdowns, anomalies, excel_path = run_pipeline(
        data_path="data/sales_data.csv",
        output_dir="reports"
    )

    # ── STEP 3: Generate Dashboard ─────────────────────────
    separator("STEP 3 — Building Interactive Dashboard")
    from dashboard import generate_dashboard
    dash_path = generate_dashboard(
        summary_json="reports/summary.json",
        output_path="reports/Dashboard.html"
    )

    # ── STEP 4: AI Narrative Report ────────────────────────
    separator("STEP 4 — Generating AI Narrative (Claude API)")
    try:
        from ai_report import generate_full_ai_report
        ai_path = generate_full_ai_report(
            summary_json_path="reports/summary.json",
            output_path="reports/AI_Narrative_Report.txt"
        )
    except Exception as e:
        print(f"  ⚠️  AI Report skipped (API unavailable): {e}")
        ai_path = None

    # ── SUMMARY ────────────────────────────────────────────
    elapsed = time.time() - start
    separator("✅ PIPELINE COMPLETE")

    print(f"""
  Duration        : {elapsed:.1f} seconds
  Records         : {kpis['total_orders']:,} orders processed
  Total Revenue   : ${kpis['total_revenue']:,.0f}
  Total Profit    : ${kpis['total_profit']:,.0f}
  Avg Margin      : {kpis['avg_profit_margin']}%
  Anomalies Found : {len(anomalies)}

  OUTPUT FILES:
  ✅ reports/Sales_Report_2024.xlsx
  ✅ reports/Dashboard.html
  ✅ reports/summary.json
  {'✅ reports/AI_Narrative_Report.txt' if ai_path else '⚠️  AI Narrative skipped'}

  → Open Dashboard.html in your browser to explore!
  → Open Sales_Report_2024.xlsx in Excel for full report.
""")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
