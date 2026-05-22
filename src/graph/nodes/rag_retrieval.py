#This is the LangGraph RAG Retrieval Node that orchestrates runtime retrieval by generating the current incident embedding, 
#performing vector search, calculating retrieval confidence, and updating the shared workflow state with retrieved candidates 
#and observability metadata.

from src.graph.state import IncidentState

from src.llm.embeddings import create_embedding

from src.retrieval.vector_search import (
    vector_search
)


def rag_retrieval_node(
    state: IncidentState
) -> IncidentState:

    embedding = create_embedding(
        state["normalized_text"]
    )

    candidates = vector_search(
        embedding,
        top_k=5
    )

    state["retrieved_candidates"] = candidates

    # Simple confidence approximation
    if candidates:
        state["retrieval_confidence"] = (
            1 / (1 + candidates[0]["distance"])
        )
    else:
        state["retrieval_confidence"] = 0.0

    # Observability
    state["execution_path"].append(
        "rag_retrieval_node"
    )

    state["processing_logs"].append(
        f"Retrieved {len(candidates)} "
        f"similar incidents"
    )

    return state