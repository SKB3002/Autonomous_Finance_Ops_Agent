import uuid
from graph.graph import financeops_graph


def run_agent(user_query, uploaded_file=None):
    initial_state = {
        "run_id": str(uuid.uuid4()),
        "input_type": "text",
        "user_query": user_query,
        "uploaded_file": uploaded_file,
        "persist_document": False,
        "requires_live_data": False,
        "db_write_requested": False,
        "db_write_confirmed": False,
        "extracted": False,
        "web_verified": False,
        "db_verified": False,
        "charts_generated": False,
        "validation_result": None,
        "decision": None,
        "confidence_score": None,
        "escalation_required": False,
    }

    return financeops_graph.invoke(initial_state)

