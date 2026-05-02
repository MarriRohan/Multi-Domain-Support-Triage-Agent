from typing import Dict, List, Tuple

UNSAFE_PHRASES = [
    "we have refunded",
    "your account is now secure",
    "guaranteed",
    "definitely",
]


def validate_response(response: str, retrieved_docs: List[Dict[str, str]]) -> Tuple[bool, str]:
    lower_resp = response.lower()

    if any(phrase in lower_resp for phrase in UNSAFE_PHRASES):
        return False, "Response contains potentially unsupported or unsafe claim."

    if "support documentation" in lower_resp and not retrieved_docs:
        return False, "Response references documentation but no documents were retrieved."

    return True, "Response validated successfully."
