from agents.audit_agent import log_event


def validate_data(run_id: str, extracted, db_data, web_data):
    validation = {
        "valid": True,
        "issues": []
    }

    if extracted.get("mentions_invoice") and not db_data.get("invoices"):
        validation["valid"] = False
        validation["issues"].append("No invoice records found")

    if extracted.get("needs_live_data") and not web_data:
        validation["valid"] = False
        validation["issues"].append("Live data required but unavailable")

    log_event(
        run_id,
        "validation_agent",
        "validation_result",
        {},
        validation
    )

    return validation

