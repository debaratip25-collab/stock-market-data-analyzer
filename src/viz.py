from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def plot_close_price(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["Close"], label="Close", linewidth=2)
    plt.title(f"{ticker} - Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()

def plot_moving_averages(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Close", linewidth=1.8)

    for window in (20, 50, 200):
        col = f"SMA_{window}"
        if col in df.columns:
            plt.plot(df.index, df[col], label=col)

    plt.title(f"{ticker} - Close Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()

def plot_returns_distribution(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    returns = df["Daily_Return"].dropna()
    plt.figure(figsize=(10, 5))
    sns.histplot(returns, bins=50, kde=True)
    plt.title(f"{ticker} - Daily Returns Distribution")
    plt.xlabel("Daily Return (decimal)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()

def plot_volatility(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["Volatility_20"], label="Rolling Volatility (20D)")
    plt.title(f"{ticker} - Rolling Volatility (20 days)")
    plt.xlabel("Date")
    plt.ylabel("Volatility (std of returns)")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()
