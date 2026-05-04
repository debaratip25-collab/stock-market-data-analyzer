from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

try:
    import yfinance as yf
except Exception:
    yf = None

@dataclass
class FetchResult:
    df: pd.DataFrame
    source: str

def fetch_from_yahoo(ticker: str, start: str, end: str) -> FetchResult:
    """
    Downloads OHLCV data from Yahoo Finance via yfinance.
    Returns a DataFrame containing Date, Open, High, Low, Close, Adj Close, Volume (depending on yfinance).
    """
    if yf is None:
        raise RuntimeError("yfinance is not available. Install it or use CSV fallback.")

    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False
    )

    if df is None or df.empty:
        raise ValueError(f"No data returned for ticker={ticker}. Check the ticker and date range.")

    df = df.reset_index()  # Date becomes a column
    return FetchResult(df=df, source="yfinance")
