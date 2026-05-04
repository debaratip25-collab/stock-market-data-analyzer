from __future__ import annotations
import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds analytics columns:
    - Daily_Return
    - SMA_20, SMA_50, SMA_200
    - Volatility_20 (rolling std of daily returns)
    - Drawdown
    """
    df = df.copy()

    df["Daily_Return"] = df["Close"].pct_change()

    for window in (20, 50, 200):
        df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()

    df["Volatility_20"] = df["Daily_Return"].rolling(window=20).std()

    df["Cumulative_Max_Close"] = df["Close"].cummax()
    df["Drawdown"] = (df["Close"] / df["Cumulative_Max_Close"]) - 1.0

    return df

def summarize(df: pd.DataFrame, ticker: str) -> dict:
    close = df["Close"]
    daily_ret = df["Daily_Return"].dropna()

    summary = {
        "ticker": ticker,
        "start_date": df.index.min().date().isoformat(),
        "end_date": df.index.max().date().isoformat(),
        "num_rows": int(df.shape[0]),

        "highest_close": float(close.max()),
        "highest_close_date": str(close.idxmax().date().isoformat()),
        "lowest_close": float(close.min()),
        "lowest_close_date": str(close.idxmin().date().isoformat()),

        "mean_daily_return": float(daily_ret.mean()) if len(daily_ret) else np.nan,
        "std_daily_return": float(daily_ret.std()) if len(daily_ret) else np.nan,

        "volatility_20_latest": float(df["Volatility_20"].dropna().iloc[-1]) if df["Volatility_20"].notna().any() else np.nan,
        "max_drawdown": float(df["Drawdown"].min()) if "Drawdown" in df.columns else np.nan,
    }
    return summary