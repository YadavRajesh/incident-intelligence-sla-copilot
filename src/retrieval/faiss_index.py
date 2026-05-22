#This file performs the one-time historical indexing process by generating embeddings for past incidents and storing them inside a 
#persistent FAISS vector index. It essentially creates the searchable semantic memory of the system.
#Please note that this indexing process is separate from the real-time workflow execution. It will never be called during normal API requests. 
#It should typically be executed as a standalone indexing job before the API service starts or whenever historical incident data needs refreshing. The simplest enterprise-friendly approach is to create a small runner script like:
# from src.retrieval.faiss_index import build_faiss_index

# build_faiss_index(
#     "data/historical_incidents.csv"
# )
#and run it manually using: python build_index.py

# Later in production, this can evolve into:
# Azure Function timer trigger


# that periodically rebuilds the vector store with newly closed incidents.

import faiss #Imports the FAISS library which is responsible for high-performance vector similarity search.
import numpy as np #Imports NumPy for handling vectors/embeddings as numerical arrays.
import pandas as pd #Imports Pandas to load and process historical incident CSV files.
import pickle #Used to save and load Python objects like metadata.

from src.llm.embeddings import create_embedding

 
VECTOR_STORE_PATH = "data/vector_store" #Defines the folder location where the FAISS index and metadata files will be persisted.

#main function responsible for building the FAISS vector index from historical incidents.
def build_faiss_index(csv_path: str): #Input parameter containing the path to the historical incidents CSV file.

    df = pd.read_csv(csv_path, sep=";")#Loads the historical incidents data from the specified CSV file into a Pandas DataFrame. The separator is set to comma (,) which is standard for CSV files. This forces Pandas to correctly split each row into separate structured fields like incident_number, short_description, description, etc., instead of treating the whole line as one giant string.
    # with open(csv_path,"r",encoding="cp1252",errors="replace") as f: #Loads the historical incidents data from the specified CSV file into a Pandas DataFrame. Encoding is set to cp1252 to handle special characters.errors="replace" Automatically replaces problematic characters instead of crashing.
    #     df = pd.read_csv(f,engine="python")

    embeddings = [] #Will store vector embeddings of historical incidents.
    metadata = [] #Will store original incident information corresponding to each embedding.

    for _, row in df.iterrows():

        text = (
            f"{row.get('short_description', '')} "
            f"{row.get('description', '')}"
        )[:500]

        embedding = create_embedding(text)

        embeddings.append(embedding)

        print(row.to_dict())
        metadata.append(row.to_dict())#Stores the original historic incident row as metadata. Because FAISS only stores vectors.When FAISS later retrieves a similar vector, we need metadata to know:
        #which incident it belongs to incident number,description,other fields


    embeddings_np = np.array(
        embeddings,
        dtype="float32"
    )#Converts the Python list of embeddings into a NumPy array.FAISS expects embeddings in NumPy float32 format.

    dimension = embeddings_np.shape[1] #Determines embedding vector size. If embedding model returns 1536-dimensional vectors: dimension would be 1536.This is required when creating the FAISS index.

    index = faiss.IndexFlatL2(dimension) #Creates a FAISS index L2 Distance (Euclidean Distance) This tells FAISS how vector similarity should be calculated. Smaller distance = more semantically similar.

    index.add(embeddings_np) #Adds all historical incident embeddings into the FAISS index. This creates the searchable vector memory of the system.

    faiss.write_index(
        index,
        f"{VECTOR_STORE_PATH}/historical.index"
    ) #Persists/saves the FAISS index to disk.This prevents rebuilding embeddings every runtime.Very important enterprise optimization.

    with open(
        f"{VECTOR_STORE_PATH}/metadata.pkl",
        "wb"
    ) as f: ##Opens a binary file to store metadata.
        pickle.dump(metadata, f) #Saves all incident metadata into a pickle file. This allows the system to later map retrieved vectors back to actual incidents.

    print("FAISS index built successfully")


# Sequence of the above code execution:
# Historical CSV
#       ↓
# Generate embeddings
#       ↓
# Create FAISS index
#       ↓
# Store vectors
#       ↓
# Persist searchable semantic memory