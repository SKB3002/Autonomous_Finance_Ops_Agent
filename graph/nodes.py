from agents.ingestion_agent import ingest_input
from agents.web_agent import fetch_live_data
from agents.db_query_agent import query_database
from agents.validation_agent import validate_data
from agents.risk_agent import assess_risk
from agents.visualization_agent import create_visualization
from agents.memory_agent import MemoryAgent
from agents.db_control_agent import request_db_change
from agents.audit_agent import log_event
from tools.file_tools import parse_document


def ingestion_node(state):
    extracted = ingest_input(
        state["run_id"],
        state["user_query"],
        state["input_type"]
    )
    state["requires_live_data"] = extracted.get("needs_live_data", False)
    state["extracted"] = True
    log_event(state["run_id"], "graph", "ingestion_complete", {}, extracted)
    return state


def file_node(state):
    if state.get("uploaded_file"):
        doc = parse_document(state["uploaded_file"])
        memory = MemoryAgent(state["run_id"])
        memory.add_to_stm("document", doc)

        if state.get("persist_document"):
            memory.request_persistence(
                key=f"document:{state['uploaded_file']}",
                value=doc,
                user_approved=True
            )
    return state


def web_node(state):
    if state["requires_live_data"]:
        web_data = fetch_live_data(state["run_id"], {"raw_query": state["user_query"]})
        memory = MemoryAgent(state["run_id"])
        memory.add_to_stm("web_data", web_data)
        state["web_verified"] = True
    return state


def db_read_node(state):
    db_data = query_database(
        state["run_id"],
        {"raw_query": state["user_query"], "mentions_invoice": True}
    )
    memory = MemoryAgent(state["run_id"])
    memory.add_to_stm("db_data", db_data)
    state["db_verified"] = True
    return state


def visualization_node(state):
    if "chart" in (state["user_query"] or "").lower():
        memory = MemoryAgent(state["run_id"])
        db_data = memory.stm.get("db_data")

        if db_data and db_data.get("invoices"):
            chart_data = {
                f"Invoice {i+1}": row[2]
                for i, row in enumerate(db_data["invoices"])
            }
            create_visualization(
                state["run_id"],
                chart_data,
                "bar",
                "Invoice Amounts"
            )
            state["charts_generated"] = True
    return state


def validation_node(state):
    validation = validate_data(
        state["run_id"],
        {},
        {},
        {}
    )
    state["validation_result"] = validation
    return state


def risk_node(state):
    decision, confidence, escalate = assess_risk(
        state["run_id"],
        state["validation_result"]
    )
    state["decision"] = decision
    state["confidence_score"] = confidence
    state["escalation_required"] = escalate
    return state


def db_write_node(state):
    if state.get("db_write_requested"):
        request_db_change(
            state["run_id"],
            state["db_write_requested"],
            state["db_write_confirmed"]
        )
    return state
