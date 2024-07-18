import os
import shlex
import subprocess
import traceback
import json
import platform
import logging
import inquirer
from pathlib import Path
from dotenv import load_dotenv
from groq import Client, Groq
from src.main import cheat_sheet_menu
# Import your custom modules
from src.services.file_service import CheatSheet, write_json_file
from src.services.groq_api import Groq#Service
from src.services.tavily_api import TavilyService
from src.ui.display import (
    print_welcome_message, print_command_output, print_error_message,
    print_command_history, print_help_message, print_code_snippet
)
from src.ui.prompts import (
    get_user_input, get_choice, get_confirmation,
    get_multiple_choices, get_form_input
)
from src.assistant.chat import chat_mode
from src.assistant.search import search_mode
from src.assistant.system_info import SystemInfo
from src.config import load_config
print("Debug: Entering src/assistant/cli_assistant.py")
# Setup logging
logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize SystemInfo
system_info = SystemInfo()

# Initialize the cheat sheet if it doesn't exist
write_json_file(Path.home() / ".croqli_cheatsheet.json")

# Initialize an empty list to keep the history of commands and their contexts
command_history = []
COMMAND_HISTORY_LENGTH = 10



# Detect shell and operating system
def detect_shell_and_os():
    """Detect the current shell and operating system."""
    # Detect the shell
    shell = os.getenv('SHELL', '/bin/bash')
    shell_name = os.path.basename(shell)

    # Detect the OS
    operating_system = platform.system().lower()

    return shell_name, operating_system

def handle_cheat_sheet_action(config, choice):
    if choice == 'View':
        config.cheat_sheet.view()
    elif choice == 'Edit (manually)':
        config.cheat_sheet.edit_manually()
    elif choice == 'Edit (AI-assisted)':
        config.cheat_sheet.edit_ai_assisted(config.groq_service.generate_response)
    elif choice == 'Update (auto-run)':
        config.cheat_sheet.update_auto_run(config)
    elif choice == 'Add categories':
        category_name = inquirer.prompt([
            inquirer.Text('category', message="Enter new category name:")
        ])['category']
        config.cheat_sheet.add_category(category_name)

def execute_command(command):
    """Execute a shell command and return the output and exit code."""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        return stdout.decode().strip(), stderr.decode().strip(), exit_code
    except Exception as e:
        return "", str(e), 1

def check_program_installed(program: str) -> bool:
    """Check if a particular program is installed and available."""
    return subprocess.call(['which', program], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def provide_helpful_tips(command: str, stderr: str) -> str:
    """Provide tips or suggestions when a command fails."""
    if "ls:" in stderr and "No such file or directory" in stderr:
        return f"Tip: The directory in the command '{command}' does not exist. Please check the path."
    if "command not found" in stderr:
        program = command.split()[0]
        return f"Tip: The command '{program}' is not available. Please install it or check your spelling."
    return stderr

def update_command_history(user_prompt, command, success, output=None, error=None):
    command_history.append({
            'user_prompt': user_prompt,
        'command': command,
        'success': success,
        'output': output,
        'error': error
    })
    # Keep only the last N commands in memory to avoid unbounded growth
    if len(command_history) > COMMAND_HISTORY_LENGTH:
        command_history.pop(0)

    log_command(user_prompt, command, success, output, error)

def log_command(user_prompt, command, success, output=None, error=None):
    """Log command execution results."""
    result = "Success" if success else "Error"
    logging.info(f"User Prompt: {user_prompt}, Command: {command}, Result: {result}, Output: {output}, Error: {error}")

def generate_system_prompt(shell_name, operating_system):
    """Generate the system prompt, incorporating command history and environment information."""
    platform_info = {
            "macos": {
                "open_command": "open",
            "browser": "Safari"
        },
        "linux": {
                "open_command": "xdg-open",
            "browser": "firefox"
        },
        "windows": {
                "open_command": "start",
            "browser": "Microsoft Edge"
        }
    }

    platform_data = platform_info.get(operating_system, {})
    history_info = '\n'.join([
            f"Previous Command: {h['command']}, Success: {h['success']}, Error: {h['error'] or 'None'}"
        for h in command_history[-3:]
    ])  # Last 3 commands

    system_prompt = f"""You are an AI assistant that can understand natural language prompts and generate the appropriate shell commands to execute based on the user's request. Your task is to analyze the user's input and determine the best command to execute, then provide the command in a valid JSON format with a "command" key.

Environment Information:
- Shell: {shell_name}
- Operating System: {operating_system}
- Open Command:Continuing from where the script left off:


- Open Command: {platform_data.get("open_command", "unknown")}
- Default Browser: {platform_data.get("browser", "unknown")}

{history_info}

Please be concise and only provide the necessary command, without any additional explanation or context. Your goal is to provide the most appropriate command for the user's request.
"""
    return system_prompt

def handle_error_and_retry(user_prompt, error_message, shell_name, operating_system):
    """Handle errors by requesting a new command based on the error message."""
    retry_prompt = f"The last command failed with the following error: {error_message}. Please modify the command to fix the error."
    system_prompt = generate_system_prompt(shell_name, operating_system)
    chat_completion = Client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
            {"role": "user", "content": retry_prompt}
        ],
        model="mixtral-8x7b-32768",
        temperature=0.1,
        max_tokens=32768,
        response_format={"type": "json_object"}
    )

    response_json = chat_completion.choices[0].message.content
    try:
        command_dict = json.loads(response_json)
        command = command_dict['command']
        print(f"Retrying command [{command}] ...")
        stdout, stderr, exit_code = execute_command(command)

        if exit_code == 0:
            update_command_history(user_prompt, command, True, stdout)
            print("Command executed successfully.")
            print("Command output:")
            print(stdout)
        else:
            helpful_tips = provide_helpful_tips(command, stderr)
            update_command_history(user_prompt, command, False, error=helpful_tips)
            print("Error executing command:")
            print(helpful_tips)
    except json.JSONDecodeError as e:
        print(f"Error parsing response as JSON: {e}")
        print(f"Response JSON: {response_json}")
        print("Tip: Please ensure your input is clear, or try simplifying your request.")
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        print("Tip: An unexpected error occurred. Please try again.")

def suggest_similar_commands(user_prompt):
    """Suggest similar commands based on previous commands."""
    suggestions = [h['command'] for h in command_history if user_prompt.lower() in h['user_prompt'].lower()]
    if suggestions:
        print("Did you mean one of these commands?")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

#def handle_add_command(user_input: str, cheat_sheet_path: Path):
    #"""Handle the /add command to add information to the cheat sheet."""
    #if user_input.startswith("/add"):
        #question_to_add = user_input.replace("/add ", "").strip()
        #if question_to_add:
            #if 'useful_questions' not in self.cheat_sheet.data:
                #self.cheat_sheet.data['useful_questions'] = []
            #self.cheat_sheet.data['useful_questions'].append(question_to_add)
            #self.cheat_sheet.save()
            #print("Added to your cheat sheet!")
        #else:
            #print("Please specify the question to add.")
    #else:
        #print("Unknown command. Try /add followed by the question.")


# Activate the virtual environment
venv_path = '/Users/Shared/Relocated Items/Docs_dump/visual studio code projects/CLI_assistant/my_env'
activate_script = os.path.join(venv_path, 'bin', 'activate')
activate_script = shlex.quote(activate_script)
subprocess.run(f'source {activate_script}', shell=True, check=True)

# Load environment variables
#env_path = Path('/Users/Shared/Relocated Items/Docs_dump/visual studio code projects/CLI_assistant/.env')
#load_dotenv(dotenv_path=env_path)

# src/assistant/cli_assistant.py

def cli_assistant_mode(config, console):
    """
    Implement the command-line interface logic here.
    This is the main entry point for the "CLI Assistant" mode.
    """
    try:
        load_dotenv() 
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        client = Groq(api_key=api_key)

        shell_name, operating_system = detect_shell_and_os()
        cheat_sheet = CheatSheet(config.cheat_sheet_path)


        while True:
            user_input = input("Query:> ")

            if user_input.lower().strip() in ['exit', 'quit', '/menu']:
                break
            elif user_input == "/cheat_sheet":
                cheat_sheet_menu(config)
            #elif user_input.startswith("/add"):
                #handle_add_command(user_input, cheat_sheet)
            else:
                # Process other commands or queries as usual
                suggest_similar_commands(user_input)

                system_prompt = generate_system_prompt(shell_name, operating_system)
                cheat_sheet_context = cheat_sheet.get_context()
                
                # Include cheat sheet context in the system prompt
                system_prompt += f"\n\nCheat Sheet Context: {json.dumps(cheat_sheet_context)}"

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    model="mixtral-8x7b-32768",
                    temperature=0.1,
                    max_tokens=32768,
                    response_format={"type": "json_object"}
                )

            response_json = chat_completion.choices[0].message.content

            try:
                command_dict = json.loads(response_json)
                command = command_dict['command']
                print(f"Running command [{command}] ...")
                stdout, stderr, exit_code = execute_command(command)

                if exit_code == 0:
                    cheat_sheet.data["installed_apps"]["python"] = platform.python_version(), cheat_sheet.save()
                    update_command_history(user_input, command, True, stdout)
                    print("Command executed successfully.")
                    print("Command output:")
                    print(stdout)
                else:
                    helpful_tips = provide_helpful_tips(command, stderr)
                    update_command_history(user_input, command, False, error=helpful_tips)
                    print("Error executing command:")
                    print(helpful_tips)
                    handle_error_and_retry(user_input, helpful_tips, shell_name, operating_system)
            except json.JSONDecodeError as e:
                print(f"Error parsing response as JSON: {e}")
                print(f"Response JSON: {response_json}")
                print("Tip: Please ensure your input is clear, or try simplifying your request.")
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
                print("Tip: An unexpected error occurred. Please try again.")

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

# Export the cli_assistant_mode function
__all__ = ['cli_assistant_mode']

