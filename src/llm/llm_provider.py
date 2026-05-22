import os

from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


DEPLOYMENT_NAME = os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)


def invoke_llm(prompt: str):

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0,

        max_tokens=300
    )

    return response.choices[0].message.content