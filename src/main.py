# src/main.py

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import click
from src.assistant.chat import chat_mode
from src.assistant.search import search_mode
from src.assistant.cli_assistant import assistant_mode
from src.ui.display import Console
from src.config import load_config
from src.ui.prompts import prompt_select_mode
from dotenv import load_dotenv


def main():
    load_dotenv()
    config = load_config()  # Load configuration
    console = Console()  # Initialize Rich console

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config()
    ctx.obj['console'] = Console()

@cli.command()
@click.pass_context
def hub(ctx):
    """Main hub for the application."""
    while True:
        mode = prompt_select_mode()
        if mode == 'Assistant':
            assistant_mode(ctx.obj['config'], ctx.obj['console'])
        elif mode == 'Chat':
            chat_mode(ctx.obj['config'], ctx.obj['console'])
        elif mode == 'Search':
            search_mode(ctx.obj['config'], ctx.obj['console'])
        elif mode == 'Exit':
            ctx.obj['console'].print("Exiting application. Goodbye!", style="bold yellow")
            break

if __name__ == "__main__":
    cli(obj={})
