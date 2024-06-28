# src/main.py

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.assistant.cli_assistant import assistant_mode
from dotenv import load_dotenv
from inquirer import prompt, List
from src.config import load_config
from src.assistant.chat import chat_mode
from src.assistant.search import search_mode
from src.assistant import cli_assistant 
from src.assistant.system_info import SystemInfo
from src.ui.display import Console


def main():
    load_dotenv()
    config = load_config()  # Load configuration
    console = Console()  # Initialize Rich console

    while True:
        mode = prompt([
            List('mode',
                 message="Select a mode",
                 choices=['Chat', 'Search', 'Assistant', 'Exit'])
        ])['mode']

        if mode == 'Exit':
            break
        elif mode == 'Chat':
            chat_mode(config, console)
        elif mode == 'Search':
            search_mode(config, console)
        elif mode == 'Assistant':
            assistant_mode(config, console)

if __name__ == "__main__":
    main()


