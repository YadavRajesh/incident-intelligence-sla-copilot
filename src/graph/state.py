from typing import TypedDict, List, Dict, Any


class IncidentState(TypedDict):

    # =========================
    # INCIDENT METADATA
    # =========================
    incident_number: str
    short_description: str
    description: str
    urgency: str
    state: str
    opened_at: str
    sla_due: str
    assignment_group: str
    business_service: str
    cmdb_ci: str

    # =========================
    # INCIDENT ANALYSIS
    # =========================
    normalized_text: str

    # =========================
    # RAG RETRIEVAL
    # =========================
    retrieved_candidates: List[Dict[str, Any]]
    retrieval_confidence: float

    # =========================
    # LLM REASONING
    # =========================
    confirmed_matches: List[str]
    possible_matches: List[str]
    match_summary: str

    # =========================
    # SLA ANALYSIS
    # =========================
    progress_pct: float
    sla_total_hours: float
    sla_elapsed_hours: float
    sla_remaining_hours: float
    alert_type: str

    # =========================
    # GOVERNANCE & EVALUATION
    # =========================
    governance_flags: List[str]
    hallucination_risk: str
    llm_calls: int

    # =========================
    # OBSERVABILITY
    # =========================
    execution_path: List[str]
    processing_logs: List[str]

    # =========================
    # FINAL OUTPUT
    # =========================
    final_alert_payload: Dict[str, Any]