import getpass
import dotenv
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import JSONLoader
from langchain.agents import create_agent
from google.cloud import aiplatform as vertex_ai

dotenv.load_dotenv()

# project_id = "gen-lang-client-0004110952"
# vertex_ai.init(project=project_id, location="us-central1")

from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_experimental.llms import ChatLlamaAPI


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = InMemoryVectorStore(embedding=embeddings)

def store_json_queries(queries):
    return queries["data"]["__schema"]["queryType"]["fields"]

def persist_queries_to_vector_store():
    loader = JSONLoader(
    file_path='./queries.json',
    jq_schema='.data.__schema.queryType.fields[]',
    text_content=False)

    data = loader.load()
    vector_store.add_documents(documents=data)
    # print(data[0])
    print(f"Loaded {len(data)} documents from the JSON file.")    
    # vector_store.add_documents(documents=data)

persist_queries_to_vector_store()

def find_similar_queries(query):
    """Find the most similar queries from the vector store."""
    return vector_store.similarity_search(query, k=1)

def call_graphql_api(query):
    """Call the GraphQL API with the provided query."""
    from gql import Client, gql
    from gql.transport.aiohttp import AIOHTTPTransport

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://swapi-graphql.netlify.app/graphql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport)

    # Provide a GraphQL query
    qe = gql(query)

    # Execute the query on the transport
    result = client.execute(qe)
    return result

tools = [find_similar_queries, call_graphql_api]

prompt = """You are a GraphQL expert. Given the user's question, find the most relevant GraphQL query from the vector store and provide it as the answer. If no relevant query is found, respond with 'No relevant query found.'."""

agent = create_agent("ollama:llama3.1", tools, prompt=prompt)

query = "First, create a query to fetch all films with their titles, show me the query. Wait for my confirmation before executing the query."

# agent.invoke(
#     {"messages": [{"role": "user", "content": query}]}
# )

for step in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()