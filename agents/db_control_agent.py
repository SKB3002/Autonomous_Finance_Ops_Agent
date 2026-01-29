
from tools.sql_tools import propose_db_write
from agents.audit_agent import log_event


def request_db_change(run_id: str, sql_statement: str, user_confirmed: bool):
    """
    DB mutations are NEVER auto-executed.
    """
    log_event(
        run_id,
        "db_control_agent",
        "db_write_requested",
        {"statement": sql_statement},
        {}
    )

    if not user_confirmed:
        log_event(
            run_id,
            "db_control_agent",
            "db_write_blocked",
            {},
            {"reason": "user_not_confirmed"}
        )
        return {
            "status": "blocked",
            "reason": "confirmation_required"
        }

    proposal = propose_db_write(sql_statement)

    log_event(
        run_id,
        "db_control_agent",
        "db_write_proposed",
        {},
        proposal
    )

    return proposal
