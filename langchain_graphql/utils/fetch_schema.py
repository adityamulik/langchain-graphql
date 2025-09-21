import requests
import openai

from langchain_core.embeddings import Embeddings

def fetch_graphql_and_embed(
    endpoint: str,
    query: str,
    variables: dict = None,
    extract_fn=lambda data: data,
    openai_api_key: str = None,
    model: str = "text-embedding-ada-002"
):
    # Step 1: Query the GraphQL endpoint
    response = requests.post(
        endpoint,
        json={"query": query, "variables": variables or {}},
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    data = response.json()["data"]

    # Step 2: Extract relevant text (customize extract_fn as needed)
    text = extract_fn(data)

    # Step 3: Get embeddings from OpenAI
    openai.api_key = openai_api_key
    embedding = Embeddings.create(input=text, model=model)["data"][0]["embedding"]
    return embedding