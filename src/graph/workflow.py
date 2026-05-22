from langgraph.graph import (
    StateGraph,
    END
)

from src.graph.state import (
    IncidentState
)

from src.graph.nodes.incident_analysis import (
    incident_analysis_node
)

from src.graph.nodes.rag_retrieval import (
    rag_retrieval_node
)

from src.graph.nodes.similarity_reasoning import (
    similarity_reasoning_node
)

from src.graph.nodes.sla_analysis import (
    sla_analysis_node
)

from src.graph.nodes.governance import (
    governance_node 
)

from src.graph.nodes.alert_generation import (
    alert_generation_node
)


workflow = StateGraph(
    IncidentState
)#Creates the LangGraph orchestration graph. This tells LangGraph: “All nodes in this workflow will share and propagate IncidentState.” This is the foundation of stateful orchestration.


# =====================================
# REGISTER NODES
# =====================================

workflow.add_node(
    "incident_analysis",
    incident_analysis_node
)#Registers the Incident Analysis Node inside the graph.

workflow.add_node(
    "rag_retrieval",
    rag_retrieval_node
)

workflow.add_node(
    "similarity_reasoning",
    similarity_reasoning_node
)

workflow.add_node(
    "sla_analysis",
    sla_analysis_node
)

workflow.add_node(
    "governance",
    governance_node
)

workflow.add_node(
    "alert_generation",
    alert_generation_node
)


# =====================================
# GRAPH FLOW
# =====================================

workflow.set_entry_point(
    "incident_analysis"
)#Defines where workflow execution begins.

workflow.add_edge(
    "incident_analysis",
    "rag_retrieval"
)#Defines workflow transition. After the Incident Analysis Node completes, the workflow state is passed to the RAG Retrieval Node, which then executes.


# =====================================
# CONDITIONAL ROUTING
# =====================================

def routing_decision(state): #Defines dynamic workflow routing logic.This function decides: which node should execute next based on runtime workflow state. This is one of LangGraph’s strongest features.

    retrieval_confidence = state.get(
        "retrieval_confidence",
        0.0
    )

    if retrieval_confidence < 0.30: #Checks whether semantic retrieval confidence is weak. If retrieval confidence is low: skip expensive LLM reasoning directly move to governance validation. This optimizes: cost, latency, execution safety very enterprise-grade.

        return "governance"

    return "similarity_reasoning"


workflow.add_conditional_edges(
    "rag_retrieval",
    routing_decision,
    {
        "similarity_reasoning":
            "similarity_reasoning",

        "governance":
            "governance"
    }
)#Tells LangGraph: “after rag_retrieval, call routing_decision()” to dynamically decide next node.


workflow.add_edge(
    "similarity_reasoning",
    "sla_analysis"
)

workflow.add_edge(
    "sla_analysis",
    "governance"
)

workflow.add_edge(
    "governance",
    "alert_generation"
)

workflow.add_edge(
    "alert_generation",
    END
) #Marks workflow completion. After alert_generation executes, the workflow ends and no further nodes execute. This is important for controlling workflow lifecycle.


# =====================================
# COMPILE GRAPH
# =====================================

app = workflow.compile() #Compiles the LangGraph workflow into an executable application.