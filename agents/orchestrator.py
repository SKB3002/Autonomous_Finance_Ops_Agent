import uuid
from graph.state import AgentState
from agents.ingestion_agent import ingest_input
from agents.db_query_agent import query_database
from agents.web_agent import fetch_live_data
from agents.validation_agent import validate_data
from agents.risk_agent import assess_risk
from agents.audit_agent import log_event


def run_multi_agent_system(user_query: str, input_type: str = "text") -> AgentState:
    run_id = str(uuid.uuid4())

    state: AgentState = {
        "run_id": run_id,
        "input_type": input_type,
        "user_query": user_query,
        "requires_live_data": False,
        "memory_scope": "temp",
        "extracted": False,
        "db_verified": False,
        "web_verified": False,
        "charts_generated": False,
        "decision": None,
        "confidence_score": None,
        "db_write_requested": False,
        "escalation_required": False
    }

    log_event(run_id, "orchestrator", "start", {"query": user_query}, {})

    # ---- INGESTION
    extracted_data = ingest_input(run_id, user_query, input_type)
    state["extracted"] = True

    # ---- LIVE DATA CHECK
    if extracted_data.get("needs_live_data"):
        state["requires_live_data"] = True
        web_data = fetch_live_data(run_id, extracted_data)
        state["web_verified"] = True
    else:
        web_data = None

    # ---- DATABASE QUERY
    db_data = query_database(run_id, extracted_data)
    state["db_verified"] = True

    # ---- VALIDATION
    validated = validate_data(run_id, extracted_data, db_data, web_data)

    # ---- RISK ASSESSMENT
    decision, confidence, escalate = assess_risk(run_id, validated)

    state["decision"] = decision
    state["confidence_score"] = confidence
    state["escalation_required"] = escalate

    log_event(
        run_id,
        "orchestrator",
        "final_decision",
        {},
        {
            "decision": decision,
            "confidence": confidence,
            "escalation": escalate
        }
    )

    return state
