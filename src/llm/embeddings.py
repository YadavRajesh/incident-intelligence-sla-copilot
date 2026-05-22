#This file acts as the centralized embedding generation layer of the system. It connects to the embedding model (Azure OpenAI) and 
#converts incident text into semantic vector embeddings used for retrieval.
import os

from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")


def create_embedding(text: str):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding