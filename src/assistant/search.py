# src/assistant/search.py

from src.services.tavily_api import TavilyService
from src.ui.display import render_markdown
from src.config import load_config
from src.ui.prompts import prompt_user_input
from groq import Groq

class SearchModule:
    def __init__(self, config):
        self.config = config
        self.tavily_service = TavilyService()
        self.groq_client = Groq(api_key=self.config.get('groq_api_key'))

    def fetch_and_process_tavily(self, query):
        """Fetch and process data from Tavily."""
        return self.tavily_service.perform_search(query).context

    def summarize_search_results(self, context):
        """Summarize the search results using the LLM."""
        prompt = f"Summarize the following information: {context}"
        summary = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.config.get('groq_model'),
            max_tokens=self.config.get('max_tokens'),
            temperature=self.config.get('temperature'),
            top_p=self.config.get('top_p')
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
    print("Debug: Entering search mode")
    search_module = SearchModule(config)
    
    console.print("Welcome to Search Mode. Type '/menu' to return to the main menu or 'exit' to quit.", style="bold blue")
    
    while True:
        query = prompt_user_input("Search")
        
        if query.lower() == 'exit':
            console.print("Exiting Search Mode. Goodbye!", style="bold yellow")
            break
        elif query.lower() == '/menu':
            console.print("Returning to main menu...", style="bold yellow")
            return  # This will return control to hub_mode
        
        result = search_module.search(query)
        console.print("Search Results:", style="bold")
        render_markdown(result, console, config)

# Example usage (can be removed if not needed)
#if __name__ == "__main__":
    #config = load_config()
    #from rich.console import Console
    #console = Console()
    #search_mode(config, console)

__all__ = ['SearchModule', 'search_mode']