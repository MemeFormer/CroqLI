#/src/assistant/system_info.py

import sys
import json
import platform
import subprocess
from pathlib import Path
from src.services.file_service import CheatSheet




class SystemInfo:
    def __init__(self):
        self.cheat_sheet = CheatSheet(Path.home / '.croqli_cheatsheet.json')  # Correct instantiation

    def load_cheat_sheet(self):
        return self.cheat_sheet.data
       

    def save_cheat_sheet(self, cheat_sheet_data):
        self.cheat_sheet.data = cheat_sheet_data
        self.cheat_sheet.save()

    def check_brew_installed(self):
        return subprocess.call(['which', 'brew'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

    def update_cheat_sheet(self, key, value):
        self.cheat_sheet.data[key] = value
        self.save_cheat_sheet(self.cheat_sheet.data)

    def get_cheat_sheet_value(self, key):
        return self.cheat_sheet.data.get(key)

    def add_favorite_directory(self, directory):
        favorites = self.get_cheat_sheet_value("favorite_directories")
        if directory not in favorites:
            favorites.append(directory)
            self.cheat_sheet.data["favorite_directories"] = favorites
            self.cheat_sheet.save()

    def remove_favorite_directory(self, directory):
        favorites = self.get_cheat_sheet_value("favorite_directories")
        if directory in favorites:
            favorites.remove(directory)
            self.update_cheat_sheet["favorite_directories"] = favorites
            self.cheat_sheet.save()

   
    def collect_system_info(self):
        # This method can be expanded to collect more system information
        self.cheat_sheet.data["os"], platform.system()
        self.cheat_sheet.data["python_path"], sys.executable
        self.cheat_sheet.data["brew_installed"], self.check_brew_installed()
        self.cheat_sheet.data["system_info_collected"], True
        self.cheat_sheet.save()

    def get_brew_list(self):
        if self.get_cheat_sheet_value("brew_installed"):
            try:
                result = subprocess.run(['brew', 'list'], capture_output=True, text=True)
                return result.stdout.strip().split('\n')
            except subprocess.CalledProcessError:
                return []
        return []

    def update_brew_list(self):
        brew_list = self.get_brew_list()
        self.cheat_sheet.data["brew_list"] = brew_list
        self.cheat_sheet.save()

    def suggest_updates(self):
        suggestions = []
        if not self.get_cheat_sheet_value("system_info_collected"):
            suggestions.append("Collect initial system information")
        if self.get_cheat_sheet_value("brew_installed") and "brew_list" not in self.cheat_sheet.data:
            suggestions.append("Update Homebrew package list")
        # Add more suggestions as needed
        return suggestions

# Example usage
if __name__ == "__main__":
    sys_info = SystemInfo()
    print("Initial cheat sheet:", sys_info.cheat_sheet)

    # Collect system info
    sys_info.collect_system_info()

    # Add a favorite directory
    sys_info.add_favorite_directory(str(Path.home() / "Documents"))
    
    # Update brew list
    sys_info.update_brew_list()

    print("Updated cheat sheet:", sys_info.cheat_sheet)
    print("Suggestions:", sys_info.suggest_updates())
