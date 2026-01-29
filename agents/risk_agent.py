from agents.audit_agent import log_event


def assess_risk(run_id: str, validation_result: dict):
    if not validation_result["valid"]:
        decision = "escalate"
        confidence = 0.4
        escalate = True
    else:
        decision = "approve"
        confidence = 0.85
        escalate = False

    log_event(
        run_id,
        "risk_agent",
        "risk_assessment",
        validation_result,
        {
            "decision": decision,
            "confidence": confidence,
            "escalate": escalate
        }
    )

    return decision, confidence, escalate

