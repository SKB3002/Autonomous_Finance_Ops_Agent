from memory.short_term import ShortTermMemory
from memory.long_term import write_persistent_memory
from agents.audit_agent import log_event


class MemoryAgent:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.stm = ShortTermMemory(run_id)

    def add_to_stm(self, key, value):
        self.stm.add(key, value)
        log_event(
            self.run_id,
            "memory_agent",
            "stm_write",
            {"key": key},
            {"value": value}
        )

    def request_persistence(self, key, value, user_approved: bool):
        """
        Long-term memory requires explicit user approval.
        """
        if not user_approved:
            log_event(
                self.run_id,
                "memory_agent",
                "ltm_rejected",
                {"key": key},
                {"reason": "user_not_approved"}
            )
            return "not_persisted"

        write_persistent_memory(key, value)

        log_event(
            self.run_id,
            "memory_agent",
            "ltm_write",
            {"key": key},
            {"value": value}
        )
        return "persisted"

