from importlib import metadata

from langchain_graphql.chat_models import ChatGraphQL
from langchain_graphql.document_loaders import GraphQLLoader
from langchain_graphql.embeddings import GraphQLEmbeddings
from langchain_graphql.retrievers import GraphQLRetriever
from langchain_graphql.toolkits import GraphQLToolkit
from langchain_graphql.tools import GraphQLTool
from langchain_graphql.vectorstores import GraphQLVectorStore

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "ChatGraphQL",
    "GraphQLVectorStore",
    "GraphQLEmbeddings",
    "GraphQLLoader",
    "GraphQLRetriever",
    "GraphQLToolkit",
    "GraphQLTool",
    "__version__",
]
