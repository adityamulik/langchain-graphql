from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://swapi-graphql.netlify.app/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport)

# Provide a GraphQL query
qe = gql(""" query { allFilms { films { title } } } """)
query = gql(
    """query { allFilms {
    films {
      title
    }
  }
}
"""
)

# Execute the query on the transport
result = client.execute(qe)
print(result)