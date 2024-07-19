from src.models.models import SearchResult
from src.config import load_config
from tavily import TavilyClient

class TavilyService:
    def __init__(self):
        self.config = load_config()
        self.client = TavilyClient(api_key=self.config.tavily_api_key)

    def perform_search(self, query: str) -> SearchResult:
        context = self.client.get_search_context(
            query=query,
            search_depth=self.config.tavily_search_depth,
            max_tokens=self.config.tavily_max_tokens
        )
        return SearchResult(query=query, context=context, summary="")  # Summary can be filled later if needed

# You can add more Tavily-related functions here as needed^