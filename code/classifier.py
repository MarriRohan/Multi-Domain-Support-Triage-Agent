from typing import Dict, Tuple

REQUEST_TYPE_RULES = {
    "feature_request": ["feature", "add", "support", "enhancement", "would like", "can you include"],
    "bug": ["error", "bug", "broken", "fails", "failure", "not working", "issue with"],
    "product_issue": ["how to", "unable", "can't", "cannot", "problem", "question", "help"],
}

PRODUCT_AREA_RULES = {
    "billing": ["billing", "charge", "charged", "refund", "invoice", "payment", "subscription"],
    "authentication": ["login", "signin", "sign in", "password", "2fa", "verify", "account access"],
    "fraud": ["fraud", "stolen", "unauthorized", "scam", "hacked", "breach"],
    "assessment": ["assessment", "test case", "coding test", "submission", "score"],
    "api": ["api", "integration", "token", "webhook", "sdk"],
    "compliance": ["legal", "compliance", "gdpr", "regulation", "law"],
}


def classify(ticket: Dict[str, str]) -> Tuple[str, str]:
    text = f"{ticket.get('subject', '')} {ticket.get('issue', '')}".strip().lower()

    request_type = "invalid"
    for rtype, keywords in REQUEST_TYPE_RULES.items():
        if any(k in text for k in keywords):
            request_type = rtype
            break

    product_area = "general"
    for area, keywords in PRODUCT_AREA_RULES.items():
        if any(k in text for k in keywords):
            product_area = area
            break

    return request_type, product_area
