from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class LoadResult:
    df: pd.DataFrame
    source: str

def load_from_csv(csv_path: Path) -> LoadResult:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path.as_posix()}")

    df = pd.read_csv(csv_path)
    return LoadResult(df=df, source=f"csv:{csv_path.as_posix()}")
