from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ProjectPaths:
    root: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = root / "data"
    outputs_dir: Path = root / "outputs"
    images_dir: Path = root / "images"
    reports_dir: Path = root / "reports"

PATHS = ProjectPaths()
