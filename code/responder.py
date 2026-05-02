from typing import Dict, List, Tuple


class Responder:
    def build_response(
        self,
        ticket: Dict[str, str],
        retrieved_docs: List[Dict[str, str]],
        confidence: float,
        threshold: float,
    ) -> Tuple[str, str, bool]:
        if not retrieved_docs or confidence < threshold:
            return (
                "I’m escalating this ticket to a human support specialist because I could not find strong matching guidance in the approved support corpus.",
                "Insufficient corpus evidence for a safe grounded response.",
                True,
            )

        best = retrieved_docs[0]
        snippet = best["text"].replace("\n", " ").strip()
        if len(snippet) > 350:
            snippet = snippet[:347] + "..."

        response = (
            "Based on our support documentation, here is the most relevant guidance: "
            f"{snippet}"
        )
        justification = (
            f"Grounded in corpus source {best['source']} with confidence {confidence:.3f}."
        )
        return response, justification, False
