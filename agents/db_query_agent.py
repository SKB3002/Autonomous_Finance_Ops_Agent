
from tools.sql_tools import read_from_db
from agents.audit_agent import log_event


def query_database(run_id: str, extracted_data: dict):
    results = {}

    if extracted_data.get("mentions_invoice"):
        invoices = read_from_db("SELECT * FROM invoices ORDER BY created_at DESC LIMIT 5;")
        results["invoices"] = invoices

    if extracted_data.get("mentions_vendor"):
        vendors = read_from_db("SELECT * FROM vendors;")
        results["vendors"] = vendors

    log_event(
        run_id,
        "db_query_agent",
        "db_read",
        extracted_data,
        results
    )

    return results
