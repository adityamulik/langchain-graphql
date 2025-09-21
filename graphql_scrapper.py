from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

import dotenv

dotenv.load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

tools = load_tools(
    ["graphql"],
    graphql_endpoint="https://swapi-graphql.netlify.app/graphql",
)

agent = create_react_agent(llm, tools)

qe = """ query { allFilms { films { title } } } """

graphql_fields = """query { allFilms {
    films {
      title
      director
      releaseDate
      speciesConnection {
        species {
          name
          classification
          homeworld {
            name
          }
        }
      }
    }
  }
}
"""

suffix = "Search for the titles of all the star wars films stored in the graphql database that has this schem, ensure the entire planet object and all attributes are returned. Return the graphql query only. Here is the graphql schema: "

input_message = {
    "role": "user",
    "content": suffix + qe,
}

for step in agent.stream(
    {"messages": [input_message]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()