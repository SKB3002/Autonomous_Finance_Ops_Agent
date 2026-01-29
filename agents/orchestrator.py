import uuid
from graph.state import AgentState

from agents.ingestion_agent import ingest_input
from agents.db_query_agent import query_database
from agents.web_agent import fetch_live_data
from agents.validation_agent import validate_data
from agents.risk_agent import assess_risk
from agents.audit_agent import log_event

from agents.memory_agent import MemoryAgent
from agents.db_control_agent import request_db_change
from agents.visualization_agent import create_visualization

from tools.file_tools import parse_document


def run_multi_agent_system(
    user_query: str,
    input_type: str = "text",
    uploaded_file: str | None = None,
    persist_document: bool = False,
    db_write_request: str | None = None,
    db_write_confirmed: bool = False,
):
    """
    Fully integrated orchestrator.
    """

    run_id = str(uuid.uuid4())

    # ---------------- INITIAL STATE ----------------
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
        "escalation_required": False,
    }

    log_event(run_id, "orchestrator", "start", {"query": user_query}, {})

    # ---------------- MEMORY AGENT ----------------
    memory = MemoryAgent(run_id)
    memory.add_to_stm("user_query", user_query)

    # ---------------- FILE INGESTION ----------------
    extracted_document = None
    if uploaded_file:
        extracted_document = parse_document(uploaded_file)
        memory.add_to_stm("uploaded_document", extracted_document)

        if persist_document:
            memory.request_persistence(
                key=f"document:{uploaded_file}",
                value=extracted_document,
                user_approved=True,
            )

    # ---------------- INGESTION AGENT ----------------
    extracted_signals = ingest_input(run_id, user_query, input_type)
    state["extracted"] = True

    # ---------------- LIVE INTERNET ----------------
    web_data = None
    if extracted_signals.get("needs_live_data"):
        state["requires_live_data"] = True
        web_data = fetch_live_data(run_id, extracted_signals)
        state["web_verified"] = True
        memory.add_to_stm("web_data", web_data)

    # ---------------- DATABASE READ ----------------
    db_data = query_database(run_id, extracted_signals)
    state["db_verified"] = True
    memory.add_to_stm("db_data", db_data)

    # ---------------- OPTIONAL VISUALIZATION ----------------
    if "chart" in user_query.lower() and db_data:
        # Example: visualize invoice amounts
        invoice_rows = db_data.get("invoices", [])
        if invoice_rows:
            chart_data = {
                f"Invoice {i+1}": row[2]  # amount column
                for i, row in enumerate(invoice_rows)
            }

            chart_path = create_visualization(
                run_id,
                data=chart_data,
                chart_type="bar",
                title="Recent Invoice Amounts",
            )
            state["charts_generated"] = True
            memory.add_to_stm("chart_path", chart_path)

    # ---------------- VALIDATION ----------------
    validation_result = validate_data(
        run_id,
        extracted_signals,
        db_data,
        web_data,
    )

    # ---------------- RISK & DECISION ----------------
    decision, confidence, escalate = assess_risk(run_id, validation_result)

    state["decision"] = decision
    state["confidence_score"] = confidence
    state["escalation_required"] = escalate

    # ---------------- SAFE DB WRITE ----------------
    if db_write_request:
        state["db_write_requested"] = True
        db_write_response = request_db_change(
            run_id,
            sql_statement=db_write_request,
            user_confirmed=db_write_confirmed,
        )
        memory.add_to_stm("db_write_response", db_write_response)

    # ---------------- FINAL AUDIT ----------------
    log_event(
        run_id,
        "orchestrator",
        "end",
        {},
        {
            "decision": decision,
            "confidence": confidence,
            "escalation": escalate,
            "charts_generated": state["charts_generated"],
            "db_write_requested": state["db_write_requested"],
        },
    )

    return state
