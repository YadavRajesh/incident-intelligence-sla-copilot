# from src.retrieval.faiss_index import (build_faiss_index)


# if __name__ == "__main__":

#     build_faiss_index("data/HistoricalIncidents.csv")
#above code is when HistoricalIncidents.csv is already present locally and we just want to build the FAISS index from it. If we dont want to connect to Azure Blob Storage and just want to run the code locally, we can use the above code to build the FAISS index from the local CSV file. This is useful for testing and development purposes. In production, we would want to connect to Azure Blob Storage to download the latest CSV file and upload the built FAISS index back to Azure Blob Storage.
#-------------------------------------------------------------
#Note: build_index,py is not imported anywhere in the codebase. It is a standalone script that can be run manually to build the FAISS index from the historical incidents CSV file. The code in this file is responsible for downloading the latest CSV from Azure Blob Storage, building the FAISS index, and then uploading the index back to Azure Blob Storage. This is useful for testing and development purposes. In production, this functionality would be handled by an Azure Function with a Timer Trigger as shown in function_app.py.
#below code is when we want to run the code locally and we want to download the latest CSV from Azure Blob Storage, build the FAISS index and then upload the index back to Azure Blob Storage. This is useful when we want to run the code locally for testing or development purposes.

from src.storage.blob_storage import (
    download_blob,
    upload_blob
)

from src.retrieval.faiss_index import (
    build_faiss_index
)

print("Downloading latest CSV from Blob Storage...")

download_blob(
    "HistoricalIncidents.csv",
    "data/HistoricalIncidents.csv"
)

print("Building FAISS vector index...")

build_faiss_index(
    "data/HistoricalIncidents.csv"
)

print("Uploading FAISS index to Blob Storage...")

upload_blob(
    "data/vector_store/historical.index",
    "historical.index"
)

upload_blob(
    "data/vector_store/metadata.pkl",
    "metadata.pkl"
)

print("Pipeline completed successfully.")