from src.graph.state import (
    IncidentState
)


LOW_CONFIDENCE_THRESHOLD = 0.40

MAX_SAFE_LLM_CALLS = 3


def governance_node(
    state: IncidentState
) -> IncidentState:

    governance_flags = []

    retrieval_confidence = state.get(
        "retrieval_confidence",
        0.0
    )

    confirmed_matches = state.get(
        "confirmed_matches",
        []
    )

    llm_calls = state.get(
        "llm_calls",
        0
    )

    # Retrieval quality validation
    if retrieval_confidence < (
        LOW_CONFIDENCE_THRESHOLD
    ):

        governance_flags.append(
            "LOW_RETRIEVAL_CONFIDENCE"
        )

    # Limited historical grounding
    if len(confirmed_matches) == 0:

        governance_flags.append(
            "NO_CONFIRMED_MATCHES"
        )

    # LLM usage monitoring
    if llm_calls > MAX_SAFE_LLM_CALLS:

        governance_flags.append(
            "HIGH_LLM_USAGE"
        )

    # Contextual grounding assessment
    if (
        "LOW_RETRIEVAL_CONFIDENCE"
        in governance_flags
    ):

        grounding_confidence = "LOW"

    elif (
        "NO_CONFIRMED_MATCHES"
        in governance_flags
    ):

        grounding_confidence = "MEDIUM"

    else:

        grounding_confidence = "HIGH"

    # Update shared state
    state["governance_flags"] = (
        governance_flags
    )

    state["grounding_confidence"] = (
        grounding_confidence
    )

    # Observability
    state["execution_path"].append(
        "governance_node"
    )

    state["processing_logs"].append(
        "Governance evaluation completed"
    )

    print("GROUNDING DEBUG:", state["grounding_confidence"])

    return state