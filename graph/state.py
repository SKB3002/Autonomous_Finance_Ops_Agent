from typing import TypedDict, Optional, Dict, Any


class AgentState(TypedDict):
    # Run metadata
    run_id: str

    # Input
    input_type: str              # text | voice | document
    user_query: Optional[str]
    uploaded_file: Optional[str]

    # Memory control
    persist_document: bool

    # Flags
    requires_live_data: bool
    db_write_requested: bool
    db_write_confirmed: bool

    # Progress flags
    extracted: bool
    web_verified: bool
    db_verified: bool
    charts_generated: bool

    # Results
    validation_result: Optional[Dict[str, Any]]
    decision: Optional[str]
    confidence_score: Optional[float]
    escalation_required: bool
