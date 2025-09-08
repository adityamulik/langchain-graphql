# langchain-graphql

This package contains the LangChain integration with GraphQL

## Installation

```bash
pip install -U langchain-graphql
```

And you should configure credentials by setting the following environment variables:

* TODO: fill this out

## Chat Models

`ChatGraphQL` class exposes chat models from GraphQL.

```python
from langchain_graphql import ChatGraphQL

llm = ChatGraphQL()
llm.invoke("Sing a ballad of LangChain.")
```

## Embeddings

`GraphQLEmbeddings` class exposes embeddings from GraphQL.

```python
from langchain_graphql import GraphQLEmbeddings

embeddings = GraphQLEmbeddings()
embeddings.embed_query("What is the meaning of life?")
```

## LLMs

`GraphQLLLM` class exposes LLMs from GraphQL.

```python
from langchain_graphql import GraphQLLLM

llm = GraphQLLLM()
llm.invoke("The meaning of life is")
```
