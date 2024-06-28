# src/assistant/search.py

from src.services.tavily_api import TavilyService
from src.ui.display import render_markdown
from src.config import load_config
from groq import Groq

class SearchModule:
    def __init__(self):
        self.config = load_config()
        self.tavily_service = TavilyService()
        self.groq_client = Groq(api_key=self.config.groq_api_key)

    def search_mode(config, console):
        search_module = SearchModule()
    
        while True:
            query = console.input("Enter your search query (or 'exit' to quit): ")
            if query.lower() == 'exit':
                break
        
        result = search_module.search(query)
        console.print("Search Results:", style="bold")
        render_markdown(result, console)


    def fetch_and_process_tavily(self, query):
        """Fetch and process data from Tavily."""
        return self.tavily_service.perform_search(query).context

    def summarize_search_results(self, context):
        """Summarize the search results using the LLM."""
        prompt = f"Summarize the following information: {context}"
        summary = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.config.groq_model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p
        ).choices[0].message.content
        return summary

    def search(self, query):
        """Perform a search and return summarized results."""
        try:
            context = self.fetch_and_process_tavily(query)
            summary = self.summarize_search_results(context)
            return summary
        except Exception as e:
            return f"An error occurred during the search: {str(e)}"

def search_mode(config, console):
    search_module = SearchModule()
    
    while True:
        query = input("Enter your search query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        result = search_module.search(query)
        console.print("Search Results:", style="bold")
        render_markdown(result)

# Example usage (can be removed if not needed)
if __name__ == "__main__":
    search_module = SearchModule()
    query = input("Enter your search query: ")
    result = search_module.search(query)
    render_markdown(result)

__all__ = ['SearchModule', 'search_mode']
