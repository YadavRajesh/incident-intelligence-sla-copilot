***Incident Analysis Node***

This is the FIRST node after ingestion.

Purpose Of This Node

Its job is:

preprocess the incident

normalize the payload

prepare clean text for downstream RAG retrieval

validate mandatory fields



Think of it as:

“context preparation layer.”

\-----------------------------------

***RAG Retrieval Agent*** <i>--> only retrieves: “potentially similar incidents.” It does NOT decide if they are truly related.</i>

Its job is:

Take normalized incident context

Generate embeddings

Search FAISS vector index

Retrieve top-k semantically similar incidents

Store retrieved context in shared state



Think of it as:

“the contextual memory retrieval layer.”

\--------------------------------------------

***Similarity Reasoning Agent*** <i>(our True AI Agent --> Because this component: reasons, interprets semantics, evaluates ambiguity,makes contextual decisions.</i>

*This is different from deterministic nodes. This is your strongest “agentic AI” component.*



Its responsibilities are:

Take retrieved historical incidents Compare them with current incident, Use LLM semantic reasoning.

Classify incidents as:

CONFIRMED\_MATCH

POSSIBLE\_MATCH

NO\_MATCH

Update shared state with reasoning results

\------------------------------------------------------

***SLA Analysis Node*** (This node is: completely deterministic

Meaning:

no LLM

no AI reasoning

no embeddings



Just:



business rules

SLA calculations

operational logic



And this is GOOD architecture.)



Its responsibilities are:

Calculate SLA progress

Compute elapsed/remaining hours

Determine SLA risk level

Decide alert severity

Enrich workflow state with operational intelligence

\-----------------------------------------------------------

***Governance \& Evaluation Node*** (In enterprise AI systems, you NEVER blindly trust: retrieval, LLM reasoning, AI outputs. You validate them. That’s what this node does.)



Purpose Of This Node

Responsibilities:



Evaluate retrieval quality

Check reasoning confidence

Detect low-confidence matches

Add governance flags

Improve explainability

Support observability and auditing



This node demonstrates: AI outputs should be evaluated, not blindly trusted.

\---------------------------------------------------

***Alert Generation Node***

Purpose Of This Node

Responsibilities:

Generate final alert payload

Format incident summary

Include historical context

Include governance metadata

Trigger notifications

Send observability logs

Finalize workflow output

