from dotenv import load_dotenv
load_dotenv()

from azure.storage.blob import BlobServiceClient
import os


CONNECTION_STRING = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING"
)

CONTAINER_NAME = "incident-data"


blob_service_client = BlobServiceClient.from_connection_string(
    CONNECTION_STRING
)

#This function when called from other parts of AI system will Download file locally.
def download_blob(
    blob_name: str, #blob_name is the name of the file (in our case HistoricalIncidents.csv) in container (incident-date) within Azure Blob Storage that we want to download. 
    download_path: str
):

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=blob_name
    )

    with open(download_path, "wb") as file:

        data = blob_client.download_blob()

        file.write(
            data.readall()
        )


#This function when called from other parts of AI system will upload a local file to Azure Blob Storage.
def upload_blob(
    file_path: str,
    blob_name: str
):

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=blob_name
    )

    with open(file_path, "rb") as data:

        blob_client.upload_blob(
            data,
            overwrite=True
        )