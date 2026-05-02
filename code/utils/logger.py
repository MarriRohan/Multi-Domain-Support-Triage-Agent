from pathlib import Path
from typing import Dict


class TriageLogger:
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file.write_text("", encoding="utf-8")

    def log_ticket(self, ticket_id: int, payload: Dict[str, str]) -> None:
        lines = [
            f"Ticket ID: {ticket_id}",
            f"Domain: {payload.get('domain', 'Unknown')}",
            f"Request Type: {payload.get('request_type', 'invalid')}",
            f"Product Area: {payload.get('product_area', 'general')}",
            f"Risk Level: {payload.get('risk_level', 'low')}",
            f"Decision: {payload.get('decision', 'escalated')}",
            f"Justification: {payload.get('justification', '')}",
            "-" * 40,
        ]
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
