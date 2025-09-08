from typing import Type

from langchain_graphql.retrievers import GraphQLRetriever
from langchain_tests.integration_tests import (
    RetrieversIntegrationTests,
)


class TestGraphQLRetriever(RetrieversIntegrationTests):
    @property
    def retriever_constructor(self) -> Type[GraphQLRetriever]:
        """Get an empty vectorstore for unit tests."""
        return GraphQLRetriever

    @property
    def retriever_constructor_params(self) -> dict:
        return {"k": 2}

    @property
    def retriever_query_example(self) -> str:
        """
        Returns a str representing the "query" of an example retriever call.
        """
        return "example query"
