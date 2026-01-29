from typing import TypedDict, Optional

class AgentState(TypedDict):
    run_id: str

    # Input
    input_type: str  # text | voice | document
    user_query: Optional[str]

    # Data flags
    requires_live_data: bool
    memory_scope: str  # temp | persistent

    # Progress
    extracted: bool
    db_verified: bool
    web_verified: bool

    # Outputs
    charts_generated: bool
    decision: Optional[str]  # approve | reject | escalate
    confidence_score: Optional[float]

    # Safety
    db_write_requested: bool
    escalation_required: bool

