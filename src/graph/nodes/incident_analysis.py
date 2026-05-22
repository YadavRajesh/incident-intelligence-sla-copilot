from src.graph.state import IncidentState


MAX_DESCRIPTION_LENGTH = 500


def truncate_text(text: str, limit: int) -> str:

    if not text:
        return ""

    return str(text)[:limit]


def incident_analysis_node(state: IncidentState) -> IncidentState:

    short_desc = truncate_text(
        state.get("short_description", ""),
        150
    )

    description = truncate_text(
        state.get("description", ""),
        MAX_DESCRIPTION_LENGTH
    )

    # Controlled normalization for embeddings/RAG
    normalized_text = (
        f"{short_desc} {description}"
    ).strip()

    # Update shared state
    state["normalized_text"] = normalized_text

    # Observability tracking
    state["execution_path"].append(
        "incident_analysis_node"
    )

    state["processing_logs"].append(
        f"Incident analysis completed for "
        f"{state['incident_number']}"
    )

    return state