from __future__ import annotations
from pathlib import Path
import pandas as pd

def generate_basic_insights(df: pd.DataFrame, summary: dict) -> list[str]:
    insights: list[str] = []

    # Trend insight: Close vs SMA_50
    if "SMA_50" in df.columns and df["SMA_50"].notna().any():
        latest_close = df["Close"].iloc[-1]
        latest_sma50 = df["SMA_50"].dropna().iloc[-1]
        if latest_close > latest_sma50:
            insights.append("Latest close is above the 50-day SMA (possible bullish trend).")
        else:
            insights.append("Latest close is below the 50-day SMA (possible bearish/weak trend).")

    # Volatility insight
    vol = summary.get("volatility_20_latest")
    if vol == vol:  # not NaN
        if vol > 0.03:
            insights.append("Rolling volatility is relatively high (risk is elevated).")
        elif vol > 0.015:
            insights.append("Rolling volatility is moderate (normal risk conditions).")
        else:
            insights.append("Rolling volatility is low (price changes have been relatively stable).")

    # Drawdown insight
    dd = summary.get("max_drawdown")
    if dd == dd:
        insights.append(f"Maximum drawdown during the period was about {dd:.2%} (peak-to-trough decline).")

    return insights

def generate_markdown_report(summary: dict, insights: list[str], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    md = []
    md.append(f"# Stock Market Data Analyzer Report — {summary['ticker']}\n")
    md.append("## Disclaimer\n")
    md.append("This project is for **educational purposes only** and **not financial advice**.\n")

    md.append("## Data Range\n")
    md.append(f"- Start Date: **{summary['start_date']}**")
    md.append(f"- End Date: **{summary['end_date']}**")
    md.append(f"- Rows: **{summary['num_rows']}**\n")

    md.append("## Key Statistics\n")
    md.append(f"- Highest Close: **{summary['highest_close']:.2f}** on **{summary['highest_close_date']}**")
    md.append(f"- Lowest Close: **{summary['lowest_close']:.2f}** on **{summary['lowest_close_date']}**")
    md.append(f"- Mean Daily Return: **{summary['mean_daily_return']:.6f}**")
    md.append(f"- Std Daily Return: **{summary['std_daily_return']:.6f}**")
    md.append(f"- Latest 20D Volatility: **{summary['volatility_20_latest']:.6f}**")
    md.append(f"- Max Drawdown (min): **{summary['max_drawdown']:.4f}**\n")

    md.append("## Insights (Auto-generated)\n")
    for i, ins in enumerate(insights, start=1):
        md.append(f"{i}. {ins}")

    report_path.write_text("\n".join(md), encoding="utf-8")