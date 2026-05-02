from typing import Dict, Tuple

HIGH_RISK_TERMS = [
    "fraud",
    "stolen card",
    "unauthorized",
    "hacked",
    "security",
    "refund",
    "billing dispute",
    "chargeback",
    "legal",
    "compliance",
]

MEDIUM_RISK_TERMS = ["payment", "password reset", "suspicious", "cannot login", "locked out"]


def assess_risk(ticket: Dict[str, str]) -> Tuple[str, bool, str]:
    text = f"{ticket.get('subject', '')} {ticket.get('issue', '')}".lower()

    for term in HIGH_RISK_TERMS:
        if term in text:
            return "high", True, f"High-risk keyword detected: '{term}'."

    for term in MEDIUM_RISK_TERMS:
        if term in text:
            return "medium", False, f"Medium-risk keyword detected: '{term}'."

    return "low", False, "No high-risk keyword detected."
