# The similarity_reasoning.py node compares the current incident against the top semantically retrieved historical incidents by sending both contexts to the LLM for 
# semantic reasoning and validation. The LLM then classifies each historical incident as CONFIRMED_MATCH, POSSIBLE_MATCH, or NO_MATCH, and the node updates the shared workflow state 
# with the final contextual matching results and observability metadata.

import json

from src.graph.state import IncidentState

from src.llm.llm_provider import (
    invoke_llm
)


MAX_LLM_CANDIDATES = 2


def similarity_reasoning_node(
    state: IncidentState
) -> IncidentState:

    confirmed_matches = []
    possible_matches = []

    current_incident = (
        state["normalized_text"]
    )

    candidates = state[
        "retrieved_candidates"
    ]

    for candidate in candidates[:MAX_LLM_CANDIDATES]:

        print("CANDIDATE DEBUG:", candidate)

        historical_incident = candidate[
            "incident"
        ]

        prompt = f'''
                    You are an IT incident similarity analyst.

                    Compare the following incidents.

                    CURRENT INCIDENT:
                    {current_incident}

                    HISTORICAL INCIDENT:
                    {historical_incident}

                    Classify the similarity as:
                    - CONFIRMED_MATCH
                    - POSSIBLE_MATCH
                    - NO_MATCH

                    Return ONLY valid JSON:

                    {{
                        "decision": "",
                        "reason": ""
                    }}
                    '''

        response = invoke_llm(prompt)

        try:

            result = json.loads(response)

            decision = (
            result.get("decision", "")
            .strip()
            .upper()
            )

            print("LLM DECISION:", decision)
            

            

            incident_number = historical_incident.get(
            "incident_number",
            "UNKNOWN"
            )

            print("INCIDENT NUMBER:", incident_number)

            if decision == "CONFIRMED_MATCH":

                confirmed_matches.append(
                    str(incident_number)
                )

                print("APPENDED CONFIRMED MATCH")

            elif decision == "POSSIBLE_MATCH":

                possible_matches.append(
                    str(incident_number)
                )

                print("APPENDED POSSIBLE MATCH")

        except Exception:

            state["processing_logs"].append(
                "LLM response parsing failed"
            )

    state["confirmed_matches"] = (
        confirmed_matches
    )

    state["possible_matches"] = (
        possible_matches
    )

    state["match_summary"] = (
        f"{len(confirmed_matches)} "
        f"confirmed matches, "
        f"{len(possible_matches)} "
        f"possible matches"
    )

    state["llm_calls"] = min(
        len(candidates),
        MAX_LLM_CANDIDATES
    )

    # Observability
    state["execution_path"].append(
        "similarity_reasoning_node"
    )

    state["processing_logs"].append(
        "Similarity reasoning completed"
    )

    return state