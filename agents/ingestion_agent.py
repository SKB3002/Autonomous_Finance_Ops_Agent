from agents.audit_agent import log_event


def ingest_input(run_id: str, user_query: str, input_type: str):
    extracted = {
        "raw_query": user_query,
        "needs_live_data": False,
        "mentions_invoice": False,
        "mentions_vendor": False
    }

    lowered = user_query.lower()

    if any(word in lowered for word in ["latest", "current", "today", "exchange"]):
        extracted["needs_live_data"] = True

    if "invoice" in lowered:
        extracted["mentions_invoice"] = True

    if "vendor" in lowered:
        extracted["mentions_vendor"] = True

    log_event(
        run_id,
        "ingestion_agent",
        "parsed_input",
        {"query": user_query},
        extracted
    )

    return extracted

