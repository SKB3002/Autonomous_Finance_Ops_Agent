from tools.web_tools import web_search
from agents.audit_agent import log_event


def fetch_live_data(run_id: str, extracted_data: dict):
    query = extracted_data.get("raw_query")

    result = web_search(query)

    log_event(
        run_id,
        "web_agent",
        "web_fetch",
        {"query": query},
        result
    )

    return result

