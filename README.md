# Auto function invocation using Semantic Kernel

This repository contains a sample code to demonstrate the capability of Semantic Kernel to automatically invoke functions based on the context.

Here is a writeup on the scenario: [Blog post](https://www.prasanna.dev/posts/auto-function-calling-semantic-kernel)

## Pre requisites

1. Azure OpenAI Endpoints with GPT4o model
2. Azure OpenAI Endpoints with Embedding models (ada) - This will be used for indexing data in Azure AI Search and also to perform vector search. We need to embed the query to invoke the search endpoints.
3. Bing Service in Azure - [Setup](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource)
4. Azure AI Search Service with an [indexed data source to perform Vector Search.](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-create-index?tabs=config-2024-07-01%2Crest-2024-07-01%2Cpush%2Cportal-check-index)

## Execute

1. Copy the `.env.sample` file into `.env` and update the values.
2. Setup the `venv` and install the dependencies.

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Invoke the `orchestrator.py` file to run the code.

```shell
python orchestrator.py
```
