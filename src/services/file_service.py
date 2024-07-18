# croqli/src/services/file_service.py

import json
import os 
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
from typing import Any, Dict, List, Optional
from datetime import datetime
from config import Config
import inquirer


def ensure_directory_exists(directory: Path) -> None:
    """Ensure that the specified directory exists."""
    directory.mkdir(parents=True, exist_ok=True)

def append_to_command_history(file_path: Path, command: str, result: str) -> None:
    """Append a command and its result to the command history file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with file_path.open('a') as file:
        file.write(f"{timestamp} | Command: {command} | Result: {result}\n")

def read_command_history(file_path: Path, num_entries: int = 100) -> List[str]:
    """Read the last N entries from the command history file."""
    with file_path.open('r') as file:
        lines = file.readlines()
    return lines[-num_entries:]

class CheatSheet:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = self.load()

    def load(self):
        if self.file_path.exists():
            return self.read_json_file()
        return {
            "os": "",
            "shell": "",
            "package_manager": "",
            "installed_apps": {},
            "common_paths": {},
            "custom_aliases": {},
            "common_commands": {},
            "error_handling": {},
            "context_specific": {},
            "shortcuts": {}
        }

    def save(self):
        self.write_json_file(self.data)

    def read_json_file(self) -> Dict[str, Any]:
        """Read and return the contents of the JSON file."""
        with self.file_path.open('r') as file:
            return json.load(file)

    def write_json_file(self, data: Dict[str, Any]) -> None:
        """Write data to the JSON file."""
        with self.file_path.open('w') as file:
            json.dump(data, file, indent=2)
    def view(self):
        print(json.dumps(self.data, indent=2))

    def edit_manually(self):
        print("Editing cheat sheet manually...")
        for category in self.data:
            print(f"\nEditing {category}:")
            while True:
                key = input("Enter key (or press Enter to finish this category): ")
                if not key:
                    break
                value = input("Enter value: ")
                self.data[category][key] = value
        self.save()

    def edit_ai_assisted(self, llm_function):
        print("Editing cheat sheet with AI assistance...")
        # Implement AI-assisted editing using the provided LLM function
        context = f"Current cheat sheet content: {json.dumps(self.data, indent=2)}"
        user_input = input("What would you like to add or modify in the cheat sheet? ")
        prompt = f"{context}\n\nUser request: {user_input}\n\nPlease suggest changes to the cheat sheet based on the user's request."
        
        suggestion = llm_function([{"role": "user", "content": prompt}])
        
        print("\nAI Suggestion:")
        print(suggestion)
        
        apply_changes = inquirer.confirm("Do you want to apply these changes?", default=True)
        if apply_changes:
            # Here you would parse the AI's suggestion and apply it to self.data
            # For simplicity, let's just add it as a new entry in "ai_suggestions"
            if "ai_suggestions" not in self.data:
                self.data["ai_suggestions"] = {}
            self.data["ai_suggestions"][datetime.now().isoformat()] = suggestion
            self.save()
            print("Changes applied.")
        else:
            print("Changes discarded.")

    def update_auto_run(self, config):
        print("Automatically updating cheat sheet...")
        # Implement auto-update logic
        # For example, updating the installed apps:
        import subprocess
        try:
            result = subprocess.run(['brew', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                brew_list = result.stdout.strip().split('\n')
                self.data['installed_apps']['brew'] = brew_list
                self.save()
                print("Updated brew list in cheat sheet.")
        except FileNotFoundError:
            print("Brew is not installed or not in PATH.")

    def add_category(self, category_name):
        if category_name not in self.data:
            self.data[category_name] = {}
            self.save()
            print(f"Category '{category_name}' added.")
        else:
            print(f"Category '{category_name}' already exists.")

    def get_context(self):
        return self.data


# Example usage
if __name__ == "__main__":
    config = Config()
    cheat_sheet_path = config.cheat_sheet_path
    command_history_path = config.command_history_path
    
    

    ensure_directory_exists(cheat_sheet_path.parent)
    cheat_sheet = CheatSheet (cheat_sheet_path)
    

    # Example of appending to command history
    append_to_command_history(command_history_path, "ls -l", "Successfully listed directory contents")

    # Example of reading command history
    recent_commands = read_command_history(command_history_path, 10)
    print("Recent commands:")
    for command in recent_commands:
        print(command.strip())

    # Example of viewing the cheat sheet
    cheat_sheet.view()

    # Example of suggesting an update to the cheat sheet
    #suggest_cheat_sheet_update(cheat_sheet_path, "favorite_editor", "vim")

    # Example of performing a periodic update
    #perform_periodic_update(cheat_sheet_path)
