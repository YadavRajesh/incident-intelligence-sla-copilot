from src.graph.state import (
    IncidentState
)

from src.observability.logger import (
    log_workflow_execution
)


def alert_generation_node(
    state: IncidentState
) -> IncidentState:

    final_payload = {

        "incident_number":
            state["incident_number"],

        "alert_type":
            state["alert_type"],

        "progress_pct":
            state["progress_pct"],

        "confirmed_matches":
            state["confirmed_matches"],

        "possible_matches":
            state["possible_matches"],

        "match_summary":
            state["match_summary"],

        "governance_flags":
            state["governance_flags"],

        # "grounding_confidence":
        #     state["grounding_confidence"],

        "grounding_confidence":
        state.get("grounding_confidence","UNKNOWN"),

        "retrieval_confidence":
            state["retrieval_confidence"],

        "llm_calls":
            state["llm_calls"],

        "execution_path":
            state["execution_path"]
    }

    # Update shared state
    state["final_alert_payload"] = (
        final_payload
    )

    # Structured observability logging
    log_workflow_execution(
        final_payload
    )

    # Observability tracking
    state["execution_path"].append(
        "alert_generation_node"
    )

    state["processing_logs"].append(
        "Final alert payload generated"
    )

    return state