**Step 1**

we established the foundational enterprise-grade project setup for Version 2 of your system, now renamed to Incident Intelligence \& SLA Copilot. We created a clean modular folder structure separating orchestration (graph/), nodes/agents (nodes/), ingestion, retrieval, LLM abstraction, observability, configuration, and API layers to support a scalable LangGraph-based multi-agent architecture.

We also initialized the Python virtual environment, added a requirements.txt file for dependency management, created a placeholder .env file to ensure secure environment-variable-based configuration instead of hardcoded secrets, and added an empty Dockerfile to prepare the project for future cloud deployment on AWS or Azure.

*This step essentially transformed the project from a standalone script-based workflow (Version 1) into a production-oriented enterprise AI application structure.*



**Step 2**

we implemented the core LangGraph orchestration foundation by creating the shared workflow state schema inside src/graph/state.py using Python TypedDict.

This IncidentState object became the centralized workflow memory and state contract for the entire multi-agent system, carrying all incident-related context, retrieval outputs, semantic reasoning results, SLA metrics, governance flags, observability telemetry, and final alert payloads across nodes during execution. *Architecturally, this step officially transitioned the system from implicit prompt-driven orchestration (Version1) to explicit state-driven orchestration, which is one of the biggest enterprise-grade improvements in Version 2.*



**Step 3**

we implemented the first LangGraph-compatible workflow node called the *Incident Analysis Node* inside src/graph/nodes/***incident\_analysis.py***.

This node introduced the core LangGraph execution pattern where a node receives the shared IncidentState, enriches it, and returns the updated state. Functionally, the node performs deterministic preprocessing by creating a controlled and normalized incident representation (normalized\_text) optimized for downstream RAG retrieval and semantic reasoning.

We also introduced payload truncation logic to prevent token explosion, reduce embedding size, improve retrieval efficiency, and control downstream LLM costs — reusing the enterprise optimization mindset from Version 1. Additionally, the node updates observability metadata such as execution\_path and processing\_logs, enabling end-to-end workflow traceability across the orchestration graph.





**Step 4**

we implemented the complete *RAG retrieval foundation of the Incident Intelligence \& SLA Copilot*.

We first created ***embeddings.py*** to generate semantic vector embeddings from incident text using Azure OpenAI embeddings.

Then in ***faiss\_index.p***y, we built a one-time historical indexing pipeline that converts past incidents into embeddings and stores them persistently inside a FAISS vector index along with incident metadata.

Next, ***vector\_search.py*** was created to load the persisted FAISS index during runtime and perform semantic similarity search by comparing the current incident embedding against historical incident embeddings to retrieve the top-k contextual matches.

Finally, in ***rag\_retrieval.py***, we implemented the LangGraph RAG Retrieval Node that orchestrates runtime retrieval by generating the current incident embedding, executing vector search, calculating retrieval confidence, and enriching the shared workflow state with retrieved candidates and observability metadata.

Conceptually, this step introduced the complete enterprise RAG lifecycle: embeddings → vector search → FAISS retrieval → semantic retrieval → contextual memory retrieval.



**Step 5**

we implemented the Similarity Reasoning Agent, which introduced true AI-driven semantic reasoning into the workflow.

We first created ***llm\_provider.py*** as a centralized LLM abstraction layer using Azure OpenAI, ensuring provider-independent and secure LLM integration without hardcoded credentials.

Then, inside ***similarity\_reasoning.py***, we built the LangGraph reasoning node that compares the current incident against the top semantically retrieved historical incidents using bounded LLM reasoning. The node sends both current and historical incident context to the LLM, which classifies each candidate as CONFIRMED\_MATCH, POSSIBLE\_MATCH, or NO\_MATCH. The workflow then updates the shared state with contextual matching results, reasoning summaries, LLM usage metrics, and observability metadata. Architecturally, this step completed the core RAG intelligence loop by separating semantic retrieval from semantic validation, enabling controlled, scalable, and enterprise-grade contextual reasoning.



**Step 6**

we implemented the ***SLA Analysis Node***, which introduced deterministic operational intelligence into the LangGraph workflow. This node reused and evolved the SLA calculation logic from Version 1 into a LangGraph-compatible orchestration node that calculates SLA progress, elapsed and remaining SLA hours, incident urgency normalization, and alert severity classification (WARNING, ESCALATION, or NONE). Unlike the Similarity Reasoning Agent, this node intentionally avoids LLM usage because SLA governance, escalation thresholds, and compliance logic should remain deterministic, explainable, and auditable in enterprise systems. The node enriches the shared workflow state with SLA metrics, alert decisions, and observability logs, completing the hybrid architecture pattern where AI handles contextual reasoning while deterministic logic controls operational policy enforcement.



**Step 7**

we implemented the ***Governance \& Evaluation Node***, which introduced enterprise-grade governance, explainability, and execution validation into the workflow. This node evaluates retrieval confidence, contextual grounding quality, confirmed match availability, and bounded LLM usage to assess the trustworthiness of the workflow before downstream operational actions are generated.

Based on these evaluations, it generates **governance flags** such as LOW\_RETRIEVAL\_CONFIDENCE, NO\_CONFIRMED\_MATCHES, and HIGH\_LLM\_USAGE, while also introducing a more accurate enterprise concept called grounding\_confidence instead of incorrectly labeling weak retrieval as hallucination risk. Architecturally, this node established a governance-aware AI validation layer that improves explainability, observability, auditability, and responsible AI behavior by validating how strongly the workflow is grounded in historical contextual evidence.



**Step 8**

we implemented the ***Alert Generation \& Observability Node***, which acts as the final operational delivery layer of the workflow. This node takes all previously enriched workflow intelligence — including semantic retrieval results, contextual reasoning outputs, SLA metrics, governance flags, grounding confidence, and execution telemetry — and packages them into a structured final operational intelligence payload.

We also introduced centralized structured observability logging through ***logger.py***, where every incident execution is persisted as structured JSON telemetry containing execution paths, retrieval confidence, LLM usage, governance metadata, and alert outcomes. Architecturally, this step established enterprise-grade operational observability, traceability, auditability, and explainable workflow logging, enabling end-to-end monitoring and analysis of the multi-agent AI orchestration pipeline.



### **Build The Actual LangGraph Workflow**



Up until now:

we created:

*state schema*

*nodes*

*retrieval logic*

*governance logic*

*observability logic*



But all nodes are still: independent Python functions. This step officially turns everything into: a real LangGraph orchestration workflow.

This is where: node sequence, graph edges, workflow transitions, conditional routing, state propagation all become real.

LangGraph’s job is: orchestration.

Meaning:

which node runs next

how state flows

when branching happens

how workflows transition

That’s what we are implementing now.



**Step 9**

we transformed all the independently developed workflow nodes into a fully orchestrated LangGraph-based enterprise AI workflow by implementing ***workflow.py***. We created a StateGraph using the shared IncidentState schema, registered all workflow nodes (incident analysis, RAG retrieval, similarity reasoning, SLA analysis, governance, and alert generation), and defined graph edges to control workflow transitions between nodes. We also introduced intelligent conditional routing logic where low retrieval confidence dynamically skips expensive LLM reasoning and routes execution directly to governance validation, demonstrating governance-aware and cost-optimized orchestration. Finally, we compiled the graph into an executable LangGraph application, officially converting the project from procedural script execution into a stateful graph-driven multi-agent orchestration system with dynamic execution paths and centralized state propagation.





### FAST API: the external access layer.



Meaning:

it exposes your workflow as: REST APIs.



This allows:

ServiceNow

Power Automate

UiPath

dashboards

monitoring systems

enterprise applications

to interact with your AI workflow.



**Step 10**

we implemented the FastAPI Execution Layer, which transformed the LangGraph orchestration workflow into a deployable and externally consumable enterprise AI service. We created ***api.py*** using FastAPI to expose a REST API endpoint (POST /analyze-incident) that receives incident payloads from external systems such as ServiceNow, UiPath, or Power Automate. Inside this API layer, we initialize the runtime initial\_state object using incoming incident data and pass it into the compiled LangGraph workflow using app.invoke(initial\_state). Architecturally, this step established the separation between orchestration logic and external communication, where FastAPI acts purely as the external access/service layer while LangGraph handles the actual workflow execution, state propagation, routing, and node orchestration internally.







































**IncidentState in state.py and initial\_state in api.py serve two different purposes in the LangGraph architecture. IncidentState is the shared workflow state schema/contract defined using TypedDict, which tells LangGraph what fields exist in the workflow state and what data types they should contain, enabling structured state propagation, type safety, and predictable orchestration. On the other hand, initial\_state in api.py is the actual runtime state object created for each incoming API request, containing real incident data values received from external systems. In simple terms, IncidentState defines the blueprint/structure of the workflow state, while initial\_state is the live data instance passed into the LangGraph workflow during execution.**

**----------------------------------------------------------------------------------------------------------------------------------------------**

the Version 2 workflow **is designed to process one current incident at a time per API call**, which is actually the preferred enterprise pattern because it improves scalability, observability, fault isolation, and parallel processing. **So an external system like ServiceNow, UiPath, or Power Automate would typically loop through active incidents and call the FastAPI endpoint separately for each incident.** Meanwhile, the workflow gets access to past incidents through the precomputed FAISS vector store built earlier using faiss\_index.py, where historical incidents were embedded once and persisted into the FAISS index along with metadata. During runtime, the current incident embedding is used as a query vector to semantically search against this persisted historical incident memory.































Azure OpenAI (LLM and Emebddings)

&#x20;      ↓

Azure Function (offline indexing)

&#x20;      ↓

Blob Storage (vector memory)

&#x20;      ↓

Azure App Service (LangGraph workflow API)











https://unifiedportal-mem.epfindia.gov.in/memberinterface/

**101135683818**

**P4PNumber@786**



**UAN was 100924449569 and PF no. was MH/BAN/8922/000/2772**

