from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = {"Date", "Open", "High", "Low", "Close", "Volume"}

def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- NEW: handle MultiIndex / tuple columns from yfinance ---
    # Example columns might look like: ('Close', 'AAPL') or ('AAPL', 'Close')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([str(x) for x in col if x is not None and str(x) != ""])
                      for col in df.columns.to_list()]
    else:
        df.columns = [str(c) for c in df.columns]

    # Strip whitespace safely
    df.columns = [c.strip() for c in df.columns]

    # If yfinance produced columns like "Close_AAPL", normalize back to "Close"
    # We prefer the first token before "_" if it matches expected OHLCV names.
    rename_map = {}
    for c in df.columns:
        base = c.split("_")[0]
        if base in {"Open", "High", "Low", "Close", "Adj Close", "Volume", "Date"}:
            rename_map[c] = base
    df = df.rename(columns=rename_map)

    # --- existing logic continues ---
    if "Date" not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index().rename(columns={"index": "Date"})
        else:
            raise ValueError("Data must contain a 'Date' column or have a DateTimeIndex.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(list(missing))}")

    df = df.sort_values("Date").drop_duplicates(subset=["Date"], keep="last")

    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df[numeric_cols] = df[numeric_cols].ffill()
    df = df.dropna(subset=numeric_cols)

    df = df.set_index("Date")
    return df
