import os
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class RefrigeratorInfoPlugin:
    """A plugin that provides intelligence specific to refrigerators.
    Usage:
        search_client = SearchClient(endpoint, index_name, AzureKeyCredential(api_key))
        kernel.add_plugin(RefrigeratorInfoPlugin(search_client), plugin_name="AppliancesInfo")

    Examples:
        {{AppliancesInfo.search "What is the electrical requirement for a refrigerator?"}}
        =>  Returns the first `num_results` number of results for the given search query
            and ignores the first `offset` number of results.
    """
    
    def __init__(self, search_client: SearchClient, 
                 embedded_column: str = "text_vector", 
                 content_column: str = "chunk"):
        self._search_client = search_client
        self._embedded_column = embedded_column
        self._content_column = content_column
        
    @kernel_function(name="search", description="performs search on the electrical appliances manuals and returns appropriate results")
    async def vector_search(self, query: str) -> str:
        def get_embeddings(text: str):
            import openai

            open_ai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            open_ai_key = os.getenv("AZURE_OPENAI_API_KEY")

            client = openai.AzureOpenAI(
                azure_endpoint=open_ai_endpoint,
                api_key=open_ai_key,
                api_version="2023-09-01-preview",
            )
            embedding = client.embeddings.create(input=[text], model=os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT_NAME"))
            return embedding.data[0].embedding

        
        vector_query = VectorizedQuery(vector=get_embeddings(query), 
                                       k_nearest_neighbors=3, 
                                       fields=self._content_column)
        results = self._search_client.search(
            vector_queries=[vector_query],
            select=self._content_column
        )
        
        return results
