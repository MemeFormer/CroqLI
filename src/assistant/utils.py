# croqli/src/assistant/utils.py

import httpx
import os
from rich.console import Console
from rich.markdown import Markdown
from src.ui.display import render_markdown

def init_rest_client():
    """Initialize and return a GroqService instance."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return httpx.Client(
        base_url="https://api.groq.com/openai/v1",
        headers={"Authorization": f"Bearer {groq_api_key}"}
    )


def render_markdown(text: str):
    """Render markdown text using Rich."""
    console = Console()
    md = Markdown(text)
    console.print(md)

def handle_error(error, console):
    error_message = str(error)
    console.print(f"[bold red]Error:[/bold red] {error_message}")
    
    if "command not found" in error_message.lower():
        console.print("Suggestion: This command might not be installed. Would you like to search for installation instructions?")
    elif "permission denied" in error_message.lower():
        console.print("Suggestion: You might not have the necessary permissions. Try using 'sudo' before the command.")
    # Add more error patterns and suggestions as needed