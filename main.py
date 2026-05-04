from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import pandas as pd

from src.config import PATHS
from src.yahoo_fetcher import fetch_from_yahoo
from src.data_loader import load_from_csv
from src.cleaning import clean_stock_data
from src.analytics import add_indicators, summarize
from src.viz import (
    plot_close_price,
    plot_moving_averages,
    plot_returns_distribution,
    plot_volatility,
)
from src.reporting import generate_basic_insights, generate_markdown_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stock Market Data Analyzer (Educational)")
    parser.add_argument("--ticker", type=str, default="AAPL", help="Ticker symbol (e.g., AAPL)")
    parser.add_argument("--start", type=str, default="2023-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", type=str, default=str(date.today()), help="End date YYYY-MM-DD")
    parser.add_argument("--csv", type=str, default="", help="Optional CSV fallback path")
    return parser.parse_args()


def ensure_dirs() -> None:
    PATHS.data_dir.mkdir(parents=True, exist_ok=True)
    PATHS.outputs_dir.mkdir(parents=True, exist_ok=True)
    PATHS.images_dir.mkdir(parents=True, exist_ok=True)
    PATHS.reports_dir.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    ensure_dirs()
    ticker = args.ticker.upper().strip()

    # 1) Load data
    if args.csv:
        csv_path = Path(args.csv)
        raw_df = load_from_csv(csv_path).df
        source = f"csv:{csv_path.as_posix()}"
    else:
        raw_df = fetch_from_yahoo(ticker=ticker, start=args.start, end=args.end).df
        source = "yfinance"

    print(f"[INFO] Source: {source}")
    print(f"[INFO] Raw rows: {len(raw_df)}")

    # 2) Clean data
    df = clean_stock_data(raw_df)
    print(f"[INFO] Clean rows: {len(df)} | {df.index.min().date()} -> {df.index.max().date()}")

    cleaned_path = PATHS.outputs_dir / f"{ticker}_cleaned.csv"
    df.to_csv(cleaned_path)
    print(f"[OK] Saved cleaned CSV: {cleaned_path.as_posix()}")

    # 3) Analytics
    df = add_indicators(df)
    summary = summarize(df, ticker=ticker)
    summary_df = pd.DataFrame([summary])

    summary_path = PATHS.outputs_dir / f"{ticker}_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"[OK] Saved summary CSV: {summary_path.as_posix()}")

    # 4) Charts
    close_img = PATHS.images_dir / f"{ticker}_close.png"
    ma_img = PATHS.images_dir / f"{ticker}_moving_averages.png"
    ret_img = PATHS.images_dir / f"{ticker}_returns_distribution.png"
    vol_img = PATHS.images_dir / f"{ticker}_volatility.png"

    plot_close_price(df, ticker, close_img)
    plot_moving_averages(df, ticker, ma_img)
    plot_returns_distribution(df, ticker, ret_img)
    plot_volatility(df, ticker, vol_img)

    print("[OK] Saved charts:")
    print(f" - {close_img.as_posix()}")
    print(f" - {ma_img.as_posix()}")
    print(f" - {ret_img.as_posix()}")
    print(f" - {vol_img.as_posix()}")

    # 5) Report
    insights = generate_basic_insights(df, summary)
    report_path = PATHS.reports_dir / f"report_{ticker}_{summary['start_date']}_to_{summary['end_date']}.md"
    generate_markdown_report(summary, insights, report_path)
    print(f"[OK] Saved report: {report_path.as_posix()}")

    print("\n[DISCLAIMER] Educational only — not financial advice.")


if __name__ == "__main__":
    main()