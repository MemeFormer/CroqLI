# croqli/src/ui/display.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from typing import List, Dict

from rich.theme import Theme
from .theme import *
from rich.markdown import Markdown


# Define console at the module level


def create_custom_theme(config):
    return Theme({
        "info": config.brand_primary,
        "warning": config.brand_secondary,
        "danger": "red",
        "success": "green",
    })


def render_markdown(text: str, console: Console, config):
    custom_theme = create_custom_theme(config)
    styled_console = Console(theme=custom_theme)
    md = Markdown(text)
    styled_console.print(md)

    # Debug: Print using explicit colors
    print(f"[{config.brand_primary}]This should be in the primary color (orange)[/{config.brand_primary}]")
    print(f"[{config.brand_secondary}]This should be in the secondary color (light gray)[/{config.brand_secondary}]")


console = Console()
def print_welcome_message():
    """Display a welcome message to the user."""
    welcome_text = Text("Welcome to the Groq CLI Assistant!", style=TITLE_STYLE)
    console.print(Panel(welcome_text, expand=False, border_style=PRIMARY_COLOR))

def print_command_output(output: str):
    """Display command output in a formatted panel."""
    console.print(Panel(output, title="Command Output", expand=False, border_style=SECONDARY_COLOR))

def print_error_message(error: str):
    """Display error messages in a formatted panel."""
    console.print(Panel(error, title="Error", expand=False, border_style=ERROR_STYLE))

def print_command_history(history: List[Dict]):
    """Display command history in a table format."""
    table = Table(title="Command History", title_style=TITLE_STYLE)
    table.add_column("User Prompt", style=TEXT_STYLE)
    table.add_column("Command", style=HIGHLIGHT_STYLE)
    table.add_column("Success", style=SUCCESS_STYLE)
    table.add_column("Output/Error", style=TEXT_STYLE)

    for entry in history:
        success = "✓" if entry['success'] else "✗"
        output = entry['output'] if entry['success'] else entry['error']
        table.add_row(entry['user_prompt'], entry['command'], success, output)

    console.print(table)

def print_code_snippet(code: str, language: str = "python"):
    """Display a code snippet with syntax highlighting."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, border_style=SECONDARY_COLOR))

def print_help_message():
    """Display a help message with available commands."""
    help_text = """
    Available Commands:
    - execute: Execute a shell command
    - history: Show command history
    - help: Display this help message
    - exit: Exit the CLI Assistant
    """
    console.print(Panel(help_text, title="Help", expand=False, border_style=HIGHLIGHT_STYLE))