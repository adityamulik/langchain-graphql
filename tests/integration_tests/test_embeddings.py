"""Test GraphQL embeddings."""

from typing import Type

from langchain_graphql.embeddings import GraphQLEmbeddings
from langchain_tests.integration_tests import EmbeddingsIntegrationTests


class TestParrotLinkEmbeddingsIntegration(EmbeddingsIntegrationTests):
    @property
    def embeddings_class(self) -> Type[GraphQLEmbeddings]:
        return GraphQLEmbeddings

    @property
    def embedding_model_params(self) -> dict:
        return {"model": "nest-embed-001"}
