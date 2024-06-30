# src/services/file_service.py

import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime

def read_json_file(file_path: Path) -> Dict[str, Any]:
    """Read and return the contents of a JSON file."""
    with file_path.open('r') as file:
        return json.load(file)

def write_json_file(file_path: Path, data: Dict[str, Any]) -> None:
    """Write data to a JSON file."""
    with file_path.open('w') as file:
        json.dump(data, file, indent=2)

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

def update_cheat_sheet(cheat_sheet_path: Path, key: str, value: Any) -> None:
    """Update a specific entry in the cheat sheet."""
    cheat_sheet = read_json_file(cheat_sheet_path)
    if isinstance(cheat_sheet[key], dict):
        cheat_sheet[key].update(value)
    else:
        cheat_sheet[key] = value
    write_json_file(cheat_sheet_path, cheat_sheet)

def get_cheat_sheet_value(cheat_sheet_path: Path, key: str) -> Any:
    """Get a specific value from the cheat sheet."""
    cheat_sheet = read_json_file(cheat_sheet_path)
    return cheat_sheet.get(key)

def initialize_cheat_sheet(cheat_sheet_path: Path) -> None:
    """Initialize the cheat sheet with default values if it doesn't exist."""
    if not cheat_sheet_path.exists():
        default_cheat_sheet = {
            "os": "",
            "shell": "",
            "package_manager": "",
            "installed_apps": {},
            "common_paths": {},
            "custom_aliases": {}
        }
        write_json_file(cheat_sheet_path, default_cheat_sheet)

def suggest_cheat_sheet_update(cheat_sheet_path: Path, key: str, value: Any) -> bool:
    """Suggest an update to the cheat sheet and return whether the user accepted."""
    print(f"I noticed a potential update for your cheat sheet:")
    print(f"Key: {key}")
    print(f"Value: {value}")
    response = input("Would you like to add this to your cheat sheet? (Y/n): ")
    if response.lower() != 'n':
        update_cheat_sheet(cheat_sheet_path, key, value)
        return True
    return False

def perform_periodic_update(cheat_sheet_path: Path) -> None:
    """Perform periodic updates to the cheat sheet."""
    # This is a placeholder function. You would implement specific update logic here.
    # For example, updating the brew list:
    import subprocess
    try:
        result = subprocess.run(['brew', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            brew_list = result.stdout.strip().split('\n')
            update_cheat_sheet(cheat_sheet_path, 'brew_list', brew_list)
            print("Updated brew list in cheat sheet.")
    except FileNotFoundError:
        print("Brew is not installed or not in PATH.")

# Example usage
if __name__ == "__main__":
    cheat_sheet_path = Path.home() / '.assistant' / 'cheat_sheet.json'
    command_history_path = Path.home() / '.assistant' / 'command_history.txt'

    ensure_directory_exists(cheat_sheet_path.parent)
    initialize_cheat_sheet(cheat_sheet_path)

    # Example of appending to command history
    append_to_command_history(command_history_path, "ls -l", "Successfully listed directory contents")

    # Example of reading command history
    recent_commands = read_command_history(command_history_path, 10)
    print("Recent commands:")
    for command in recent_commands:
        print(command.strip())

    # Example of suggesting an update to the cheat sheet
    suggest_cheat_sheet_update(cheat_sheet_path, "favorite_editor", "vim")

    # Example of performing a periodic update
    perform_periodic_update(cheat_sheet_path)
