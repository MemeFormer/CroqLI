# croqli/src/ui/prompts.py

import inquirer
from typing import List, Dict, Any
from .theme import PRIMARY_COLOR, SECONDARY_COLOR

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