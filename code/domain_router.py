from typing import Dict

DOMAINS = ["hackerrank", "claude", "visa"]


def detect_domain(ticket: Dict[str, str]) -> str:
    company = (ticket.get("company") or "").strip().lower()
    issue_text = f"{ticket.get('subject', '')} {ticket.get('issue', '')}".lower()

    if company in DOMAINS:
        return company.capitalize() if company != "hackerrank" else "HackerRank"

    for domain in DOMAINS:
        if domain in issue_text:
            return domain.capitalize() if domain != "hackerrank" else "HackerRank"

    return "Unknown"
