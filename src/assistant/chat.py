# croqli/src/assistant/chat.py

from src.services.groq_api import GroqService
from src.ui.display import render_markdown
from src.config import load_config
from src.models.models import ChatMessage
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import os
import inquirer
import click

# Load environment variables
load_dotenv()


def load_or_create_env():
    """Load or create environment variables."""
    if not os.path.exists('.env'):
        with open('.env', 'w') as file:
            for key, value in config.DEFAULT_SETTINGS.items():
                file.write(f"{key}={value}\n")
    load_dotenv()


def get_groq_response(groq_service, input_text, history, DEFAULT_SETTINGS):
    """Get the GROQ response."""
    system_prompt = os.getenv("SYSTEM_PROMPT", DEFAULT_SETTINGS["SYSTEM_PROMPT"])
    
    messages = []
    if system_prompt:
        messages.append(ChatMessage(role="system", content=system_prompt))
    messages.extend([ChatMessage(role=msg["role"], content=msg["content"]) for msg in history])
    messages.append(ChatMessage(role="user", content=input_text))

    response = groq_service.generate_response(messages)
    return response

from rich.markdown import Markdown

def chat_mode(config, console):
    """Initiates the chat mode with configuration and console support."""
    load_or_create_env()

    try:
        groq_service = GroqService()
    except Exception as e:
        console.print(f"Error initializing GroqService: {str(e)}", style="bold red")
        return
    
    history = []
    while True:
        user_input = input("Enter your message (or type 'exit' to quit): ")
        
        if user_input.lower() in ['exit', '/quit', '/back']:
            break

        if user_input.strip() == '':
            continue

        try:
            response = get_groq_response(groq_service, user_input, history, config.DEFAULT_SETTINGS)
            console.print("Response:", style="bold green")
            console.print(Markdown(response))
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})    
        except Exception as e:
            console.print(f"An error occurred: {str(e)}", style="bold red")

    console.print("Exiting chat mode.", style="bold blue")
        
        

if __name__ != "__main__":
    # This block ensures that the chat loop doesn't start automatically when importing chat.py
    pass
else:
    config = load_config()  # Assuming load_config() is defined in src.config
    console = Console()
    chat_mode(config, console)
# Adjustments for render_markdown to use Rich console
def render_markdown(text: str, console: Console):
    """Renders markdown text using Rich."""
    md = Markdown(text)
    console.print(md)
