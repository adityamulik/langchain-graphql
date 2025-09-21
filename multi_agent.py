from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
import dotenv
import json
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import JSONLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from prompt import GRAPHQL_QUERY_GENERATOR_PROMPT, GRAPHQL_API_CALL_PROMPT, SUPERVISTOR_PROMPT, STRUCTURED_RESPONSE_OUTPUT
from langchain_core.messages import convert_to_messages

dotenv.load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = InMemoryVectorStore(embedding=embeddings)

def is_valid_json(json_string):
    """Check if a string is valid JSON and return the parsed object or an error message."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return "Response is not valid JSON."

def persist_queries_to_vector_store():
    """Load and persist GraphQL queries from a JSON file into the vector store."""
    loader = JSONLoader(
    file_path='./queries.json',
    jq_schema='.data.__schema.queryType.fields[]',
    text_content=False)

    data = loader.load()
    vector_store.add_documents(documents=data)
    # print(data[0])
    print(f"Loaded {len(data)} documents from the JSON file.")    
    # vector_store.add_documents(documents=data)

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

graphql_query_call = create_react_agent(
    model="ollama:llama3.1",
    tools=[call_graphql_api],
    prompt=GRAPHQL_API_CALL_PROMPT,
    name="call_graphql_api"
)

graphql_query_generator = create_react_agent(
    model="ollama:llama3.1",
    tools=[persist_queries_to_vector_store, find_similar_queries],
    prompt=GRAPHQL_QUERY_GENERATOR_PROMPT,
    name="generate_graphql_query"
)

graphql_structured_output = create_react_agent(
    model="ollama:llama3.1",
    tools=[is_valid_json],
    prompt=STRUCTURED_RESPONSE_OUTPUT,
    name="graphql_structured_output"
)

supervisor = create_supervisor(
    agents=[graphql_query_generator, graphql_query_call, graphql_structured_output],
    model=ChatOllama(model="llama3.1"),
    prompt=SUPERVISTOR_PROMPT
).compile()

def pretty_print_messages(update):
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")

    for node_name, node_update in update.items():
        print(f"Update from node {node_name}:")
        print("\n")

        for m in convert_to_messages(node_update["messages"]):
            m.pretty_print()
        print("\n")

for chunk in supervisor.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "find a vehicle from star wars with name that includes 'Speeder' and return its id, name, and pilots { id, name }"
            }
        ]
    }
):
    pretty_print_messages(chunk)