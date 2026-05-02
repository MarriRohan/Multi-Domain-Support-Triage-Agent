from classifier import classify
from domain_router import detect_domain
from responder import Responder
from retriever import CorpusRetriever
from risk_engine import assess_risk
from utils.config import (
    DATA_DIR,
    INPUT_CSV,
    LOG_FILE,
    OUTPUT_CSV,
    RETRIEVAL_CONFIDENCE_THRESHOLD,
    RETRIEVAL_TOP_K,
    SAMPLE_INPUT_CSV,
)
from utils.csv_handler import read_tickets, write_output
from utils.logger import TriageLogger
from validator import validate_response


ESCALATION_AREAS = {"fraud", "billing", "compliance", "authentication"}


def choose_input_file():
    if INPUT_CSV.exists():
        return INPUT_CSV
    if SAMPLE_INPUT_CSV.exists():
        return SAMPLE_INPUT_CSV
    return INPUT_CSV


def main() -> None:
    input_file = choose_input_file()
    tickets = read_tickets(input_file)

    retriever = CorpusRetriever(DATA_DIR)
    responder = Responder()
    logger = TriageLogger(LOG_FILE)

    output_rows = []

    for idx, ticket in enumerate(tickets, start=1):
        domain = detect_domain(ticket)
        request_type, product_area = classify(ticket)
        risk_level, risk_escalate, risk_reason = assess_risk(ticket)

        if product_area in ESCALATION_AREAS and product_area in {"fraud", "billing", "compliance"}:
            risk_escalate = True
            risk_level = "high"
            risk_reason = f"Mandatory escalation area detected: {product_area}."

        query = f"{domain} {ticket.get('subject', '')} {ticket.get('issue', '')}".strip()
        docs, confidence = retriever.retrieve(query, top_k=RETRIEVAL_TOP_K)

        response, response_reason, weak_evidence = responder.build_response(
            ticket=ticket,
            retrieved_docs=docs,
            confidence=confidence,
            threshold=RETRIEVAL_CONFIDENCE_THRESHOLD,
        )

        should_escalate = risk_escalate or weak_evidence
        status = "escalated" if should_escalate else "replied"

        valid, validation_reason = validate_response(response, docs)
        if not valid:
            status = "escalated"

        if status == "escalated" and "escalating" not in response.lower():
            response = (
                "Thanks for reaching out. For safety and accuracy, this ticket has been escalated to a human support specialist."
            )

        justification = "; ".join(
            part for part in [risk_reason, response_reason, validation_reason] if part
        )

        output_rows.append(
            {
                "status": status,
                "product_area": product_area,
                "response": response,
                "justification": justification,
                "request_type": request_type,
            }
        )

        logger.log_ticket(
            idx,
            {
                "domain": domain,
                "request_type": request_type,
                "product_area": product_area,
                "risk_level": risk_level,
                "decision": status,
                "justification": justification,
            },
        )

    write_output(OUTPUT_CSV, output_rows)


if __name__ == "__main__":
    main()
