from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = (BASE_DIR / "../support_issues/support_tickets.csv").resolve()
SAMPLE_INPUT_CSV = (BASE_DIR / "../support_issues/sample_support_tickets.csv").resolve()
OUTPUT_CSV = (BASE_DIR / "../output.csv").resolve()
LOG_FILE = (BASE_DIR / "../log.txt").resolve()
DATA_DIR = (BASE_DIR / "../data").resolve()

RETRIEVAL_TOP_K = 3
RETRIEVAL_CONFIDENCE_THRESHOLD = 0.12
