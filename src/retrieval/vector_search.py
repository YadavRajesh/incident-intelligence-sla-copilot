#This file loads the persisted FAISS index and performs semantic similarity search by comparing the current incident embedding against 
#historical incident embeddings. It returns the top-k closest contextual matches.
import faiss #FAISS for vector similarity search
import pickle #pickle for loading metadata
import numpy as np #NumPy for handling vector data


INDEX_PATH = "data/vector_store/historical.index" #saved FAISS index file path
METADATA_PATH = "data/vector_store/metadata.pkl" #saved metadata file path corresponding to the FAISS index. This contains the original incident information for each vector in the index.


index = faiss.read_index(INDEX_PATH) #Loads the persisted FAISS vector index into memory. This gives runtime access to historical incident embeddings.

with open(METADATA_PATH, "rb") as f: #Opens the metadata file in read-binary mode.
    metadata = pickle.load(f) #Loads all historical incident metadata into memory. This allows the system to later map retrieved vectors back to actual incidents.

#Defines the semantic retrieval function. It takes a query embedding (Embedding of current incident) and returns the top-k most similar historical incidents based on vector similarity.
def vector_search(query_embedding, top_k=5):

    query_vector = np.array(
        [query_embedding],
        dtype="float32"
    )#Converts the current incident embedding into NumPy float32 format required by FAISS.Extra brackets convert it into a 2D array because FAISS expects:[number_of_vectors, vector_dimension]

    distances, indices = index.search(
        query_vector,
        top_k
    ) #This is the core FAISS similarity search. FAISS compares:current incident embedding against all stored historical embeddings

    results = []

    for idx, dist in zip(indices[0], distances[0]): #Loops through:retrieved vector positions corresponding similarity distances

        results.append({
            "distance": float(dist),
            "incident": metadata[idx]
        })#Creates structured retrieval results. Each result contains:similarity distance and the original incident information from metadata corresponding to the retrieved vector index.

    return results #Returns top-k semantically similar incidents back to the workflow.These results later become:state["retrieved_candidates"] inside the LangGraph shared state.


#what this code does:
# Current Incident
#       ↓
# Generate embedding
#       ↓
# Load FAISS index
#       ↓
# Compare against historical vectors
#       ↓
# Retrieve closest semantic matches
#       ↓
# Return contextual candidates