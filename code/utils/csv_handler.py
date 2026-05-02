import csv
from pathlib import Path
from typing import Dict, List


REQUIRED_OUTPUT_COLUMNS = [
    "status",
    "product_area",
    "response",
    "justification",
    "request_type",
]


def read_tickets(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []

    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def write_output(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in REQUIRED_OUTPUT_COLUMNS})
