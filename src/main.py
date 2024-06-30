# src/main.py

import inquirer
import sys
from pathlib import Path
from src.assistant.cli_assistant import assistant_mode
from dotenv import load_dotenv, set_key 
from inquirer import prompt, List
from src.config import load_config
from src.assistant.chat import chat_mode
from src.assistant.search import search_mode
from src.assistant import cli_assistant 
from src.assistant.system_info import SystemInfo
from src.ui.display import Console

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def main():
    load_dotenv()
    config = load_config()  # Load configuration
    console = Console()  # Initialize Rich console

    while True:
        mode = inquirer.prompt([
            inquirer.List('mode',
                 message="Select a mode",
                 choices=['Chat', 'Search', 'Assistant', 'Settings', 'Exit'])
        ])['mode']

        if mode == 'Exit':
            break
        elif mode == 'Chat':
            chat_mode(config, console)
        elif mode == 'Search':
            search_mode(config, console)
        elif mode == 'Assistant':
            assistant_mode(config, console)
        elif mode == 'Settings':
            settings_menu(config)
            

def model_settings_menu(config):
    model_max_tokens = {
        "llama3-8b-8192": 8192,
        "llama3-70b-8192": 8192,
        "mixtral-8x7b-32768": 32768,
        "gemma-7b-it": 8192
    }

    while True:
        setting = inquirer.prompt([
            inquirer.List('setting',
                          message="Choose a model setting to modify",
                          choices=['Model Name', 'Max Tokens', 'Temperature', 'Top P', 'Back'])
        ])['setting']

        if setting == 'Back':
            break

        elif setting == 'Model Name':
            new_model = inquirer.prompt([
                inquirer.List('model', 
                              message="Choose the model to use", 
                              choices=[
                                  "llama3-8b-8192",
                                  "llama3-70b-8192",
                                  "mixtral-8x7b-32768",
                                  "gemma-7b-it"
                              ])
            ])['model']
            config.groq_model = new_model
            set_key('.env', 'GROQ_MODEL', new_model)

        elif setting == 'Max Tokens':
            current_model = config.groq_model
            max_range = model_max_tokens[current_model]
            new_max_tokens = inquirer.prompt([
                inquirer.Text('max_tokens', 
                              message=f"Enter max tokens (for {current_model}, range 0-{max_range}):", 
                              default=str(config.max_tokens),
                              validate=lambda x: x.isdigit() and 0 <= int(x) <= max_range)
            ])['max_tokens']
            config.max_tokens = int(new_max_tokens)
            set_key('.env', 'MAX_TOKENS', new_max_tokens)

        elif setting == 'Temperature':
            new_temperature = inquirer.prompt([
                inquirer.Text('temperature', 
                              message="Enter temperature (0.0 - 1.0):", 
                              default=str(config.temperature),
                              validate=lambda x: is_float(x) and 0.0 <= float(x) <= 1.0)
            ])['temperature']
            config.temperature = float(new_temperature)
            set_key('.env', 'TEMPERATURE', new_temperature)

        elif setting == 'Top P':
            new_top_p = inquirer.prompt([
                inquirer.Text('top_p', 
                              message="Enter top P (0.0 - 1.0):", 
                              default=str(config.top_p),
                              validate=lambda x: is_float(x) and 0.0 <= float(x) <= 1.0)
            ])['top_p']
            config.top_p = float(new_top_p)
            set_key('.env', 'TOP_P', new_top_p)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def settings_menu(config):
    while True:
        setting = inquirer.prompt([
            inquirer.List('setting',
                 message="Choose a setting to modify",
                 choices=['Model Settings', 'API Keys', 'System Prompts', 'Back'])
        ])['setting']

        if setting == 'Back':
            break
        elif setting == 'Model Settings':
            model_settings_menu(config) 
        

def system_prompts_menu(config):
    while True:
        # 1. Display numbered list of prompts using inquirer.List
        # 2. Get user choice (Edit, Add, Delete, Move, Back)
        # 3. Implement logic for each choice:
           # - Edit: Allow modifying the selected prompt
           # - Add: Get new prompt from user, append to config.SYSTEM_PROMPTS
           # - Delete: Remove selected prompt
           # - Move: Implement logic to reorder prompts
           # - Back: Return to settings menu


        while True:
            # 1. Display numbered list of prompts using inquirer.List
            prompt_choices = [
                inquirer.List('prompt_choice',
                          message="Choose a system prompt to modify:",
                          choices=[
                              f"{i+1}. {p.get('title', 'Untitled Prompt')}" 
                              for i, p in enumerate(config.SYSTEM_PROMPTS)
                          ] + ['Add New Prompt', 'Back'])
            ]
            answer = inquirer.prompt(prompt_choices)['prompt_choice']

            if answer == 'Back':
                break

            elif answer == 'Add New Prompt':
                # Get new prompt title and content
                new_title = inquirer.prompt([
                    inquirer.Text('title', message="Enter a title for the new prompt:")
                ])['title']
                new_prompt = inquirer.prompt([
                    inquirer.Text('prompt', message="Enter the new system prompt:")
                ])['prompt']

                # Append to SYSTEM_PROMPTS and update .env
                config.SYSTEM_PROMPTS.append({'title': new_title, 'prompt': new_prompt})
                set_key('.env', 'SYSTEM_PROMPT', new_prompt)
                set_key('.env', 'SYSTEM_PROMPT_TITLE', new_title)

            else:
                # Extract prompt index from the chosen option
                try:
                    prompt_index = int(answer.split('.')[0]) - 1
                except (ValueError, IndexError):
                    print("Invalid prompt selection.")
                    continue

                # 2. Get user choice (Edit, Delete, Move, Back)
                action = inquirer.prompt([
                    inquirer.List('action',
                                message="Choose an action:",
                                choices=['Edit', 'Delete', 'Move Up', 'Move Down', 'Back'])
                ])['action']

                if action == 'Back':
                    continue

                elif action == 'Edit':
                    # Edit prompt title and/or content
                    updated_title = inquirer.prompt([
                        inquirer.Text('title', 
                                    message="Edit the prompt title:", 
                                    default=config.SYSTEM_PROMPTS[prompt_index]['title'])
                    ])['title']
                    updated_prompt = inquirer.prompt([
                        inquirer.Text('prompt', 
                                    message="Edit the system prompt:", 
                                    default=config.SYSTEM_PROMPTS[prompt_index]['prompt'])
                    ])['prompt']

                    # Update SYSTEM_PROMPTS and .env
                    config.SYSTEM_PROMPTS[prompt_index]['title'] = updated_title
                    config.SYSTEM_PROMPTS[prompt_index]['prompt'] = updated_prompt
                    set_key('.env', 'SYSTEM_PROMPT', updated_prompt)
                    set_key('.env', 'SYSTEM_PROMPT_TITLE', updated_title)

                elif action == 'Delete':
                    # Delete the prompt
                    del config.SYSTEM_PROMPTS[prompt_index]
                    # Update .env with the first prompt (or a default)
                    if config.SYSTEM_PROMPTS:
                        set_key('.env', 'SYSTEM_PROMPT', config.SYSTEM_PROMPTS[0]['prompt'])
                        set_key('.env', 'SYSTEM_PROMPT_TITLE', config.SYSTEM_PROMPTS[0]['title'])
                    else:
                        set_key('.env', 'SYSTEM_PROMPT', "You are a helpful assistant.")
                        set_key('.env', 'SYSTEM_PROMPT_TITLE', "Default Prompt")

                elif action.startswith('Move'):
                    # Move the prompt up or down
                    new_index = prompt_index + (1 if action == 'Move Down' else -1)
                    if 0 <= new_index < len(config.SYSTEM_PROMPTS):
                        config.SYSTEM_PROMPTS.insert(new_index, config.SYSTEM_PROMPTS.pop(prompt_index))
                        # No need to update .env here, as the order doesn't affect it



if __name__ == "__main__":
    main()

