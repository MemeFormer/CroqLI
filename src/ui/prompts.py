# croqli/src/ui/prompts.py

import inquirer
from typing import List, Dict, Any
from .theme import PRIMARY_COLOR, SECONDARY_COLOR
from pathlib import Path
from src.services.file_service import update_cheat_sheet

# Use the default theme and modify it
default_theme = inquirer.themes.Default()
default_theme.Question.mark_color = PRIMARY_COLOR
default_theme.Question.bracket_color = SECONDARY_COLOR
default_theme.List.selection_color = PRIMARY_COLOR

def get_user_input(prompt: str) -> str:
    """Get user input with a simple prompt."""
    return input(f"{prompt}: ")

def get_choice(message: str, choices: List[str]) -> str:
    """Present a list of choices to the user and return their selection."""
    questions = [
        inquirer.List('choice',
                      message=message,
                      choices=choices,
                     )
    ]
    answers = inquirer.prompt(questions, theme=default_theme)
    return answers['choice']

def get_confirmation(message: str) -> bool:
    """Ask the user for confirmation."""
    questions = [
        inquirer.Confirm('confirm',
                         message=message,
                         default=True)
    ]
    answers = inquirer.prompt(questions, theme=default_theme)
    return answers['confirm']

def get_multiple_choices(message: str, choices: List[str]) -> List[str]:
    """Allow the user to select multiple options from a list."""
    questions = [
        inquirer.Checkbox('choices',
                          message=message,
                          choices=choices)
    ]
    answers = inquirer.prompt(questions, theme=default_theme)
    return answers['choices']

def get_form_input(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get multiple inputs from the user in a form-like structure."""
    return inquirer.prompt(questions, theme=default_theme)




def prompt_select_mode() -> str:
    """Present a list of mode choices to the user and return their selection."""
    return get_choice(
        message="Select mode:",
        choices=['Assistant', 'Chat', 'Search', 'Exit']
    )

def prompt_user_input(mode: str) -> str:
    """Get user input for a specific mode."""
    return get_user_input(f"{mode}> ")

def handle_add_command(user_input: str, cheat_sheet_path: Path):
    """Handle the /add command to add information to the cheat sheet."""
    if user_input.startswith("/add"):
        question_to_add = user_input.replace("/add ", "").strip()
        if question_to_add:
            update_cheat_sheet(cheat_sheet_path, "useful_questions", [question_to_add])
            print("Added to your cheat sheet!")
        else:
            print("Please specify the question to add.")
    else:
        print("Unknown command. Try /add followed by the question.")
