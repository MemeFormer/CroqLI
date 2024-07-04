# src/assistant/chat.py

from src.services.groq_api import GroqService
from src.ui.display import render_markdown
from src.config import load_config
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
    groq_model = os.getenv("GROQ_MODEL", DEFAULT_SETTINGS["GROQ_MODEL"])
    max_tokens = int(os.getenv("MAX_TOKENS", DEFAULT_SETTINGS["MAX_TOKENS"]))
    temperature = float(os.getenv("TEMPERATURE", DEFAULT_SETTINGS["TEMPERATURE"]))
    top_p = float(os.getenv("TOP_P", DEFAULT_SETTINGS["TOP_P"]))
    system_prompt = os.getenv("SYSTEM_PROMPT", DEFAULT_SETTINGS["SYSTEM_PROMPT"])

    body = {
        "model": groq_model,
        "messages": history + [{"role": "user", "content": input_text}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    if system_prompt:
        body["messages"].insert(0, {"role": "system", "content": system_prompt})

    response = groq_service.post("/chat/completions", json=body)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def chat_mode(config, console):
    """Initiates the chat mode with configuration and console support."""
    load_or_create_env()
    # Utilize config for environment variables if needed
    groq_service = GroqService()

    history = []
    while True:
        questions = [
            inquirer.Text('message', message="Enter your message (or type 'exit' to quit): ")
        ]
        answers = inquirer.prompt(questions)
        input_text = answers['message']
        
        if input_text.lower() == 'exit':
            break

        response = get_groq_response(groq_service, input_text, history, config.DEFAULT_SETTINGS)
        console.print("Response:", style="bold green")
        render_markdown(response, console)
        history.append({"role": "user", "content": input_text})
        history.append({"role": "assistant", "content": response})

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
