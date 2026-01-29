import uuid
from graph.state import AgentState
from tools.sql_tools import read_from_db
from tools.web_tools import web_search
from tools.chart_tools import generate_chart
from tools.file_tools import parse_document
from memory.short_term import ShortTermMemory
from memory.long_term import write_persistent_memory
from agents.audit_agent import log_event


def run_baseline_agent(user_query: str, input_type: str = "text") -> AgentState:
    """
    Single-agent baseline.
    This function owns the entire flow end-to-end.
    """

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

    memory = ShortTermMemory(run_id)
    memory.add("user_query", user_query)

    log_event(run_id, "orchestrator", "start", {"query": user_query}, {})

    # ---- Step 1: Detect need for live data
    if any(keyword in user_query.lower() for keyword in ["latest", "current", "today", "exchange rate"]):
        state["requires_live_data"] = True

    # ---- Step 2: Web search if needed
    if state["requires_live_data"]:
        web_result = web_search(user_query)
        memory.add("web_result", web_result)
        state["web_verified"] = True

        log_event(run_id, "orchestrator", "web_search", {"query": user_query}, web_result)

    # ---- Step 3: Database lookup
    if "vendor" in user_query.lower() or "invoice" in user_query.lower():
        db_result = read_from_db("SELECT * FROM invoices LIMIT 5;")
        memory.add("db_result", db_result)
        state["db_verified"] = True

        log_event(run_id, "orchestrator", "db_read", {}, db_result)

    # ---- Step 4: Simple decision logic
    if state["db_verified"] and state["web_verified"]:
        state["decision"] = "approve"
        state["confidence_score"] = 0.85
    elif state["db_verified"]:
        state["decision"] = "escalate"
        state["confidence_score"] = 0.55
        state["escalation_required"] = True
    else:
        state["decision"] = "reject"
        state["confidence_score"] = 0.30

    log_event(
        run_id,
        "orchestrator",
        "decision",
        {},
        {
            "decision": state["decision"],
            "confidence": state["confidence_score"]
        }
    )

    return state

