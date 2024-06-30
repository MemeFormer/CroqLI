# croqli/src/config.py

import os
from pathlib import Path
from dotenv import load_dotenv, set_key

# Define brand colors
BRAND_PRIMARY = "#F55036"  # Orange
BRAND_SECONDARY = "#CCCCCC"  # Light gray
BRAND_TEXT = "#FFFFFF"  # White for text on primary background
BRAND_DARK = "#666666"  # Darker gray

# Predefined system prompts as profiles
SYSTEM_PROMPTS = [
    {"title": "Friendly Assistant", "prompt": "You are a helpful and friendly assistant."},
    {"title": "Technical Support", "prompt": "You are a technical support specialist, ready to solve complex issues."},
    {"title": "Creative Writer", "prompt": "You are a creative writer, full of imagination and vivid descriptions."},
    {"title": "Data Analyst", "prompt": "You are a data analyst, providing insights and detailed analysis."},
    {"title": "Casual Conversation", "prompt": "You are here for a casual chat, keeping the tone light and friendly."}
]

class Config:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # API Keys
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')

        # GROQ Model settings
        self.groq_model = os.getenv('GROQ_MODEL', 'llama3-8b-8192')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '8192'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.top_p = float(os.getenv('TOP_P', '1.0'))
        self.system_prompt = os.getenv('SYSTEM_PROMPT', SYSTEM_PROMPTS[0]["prompt"])
        self.system_prompt_title = os.getenv('SYSTEM_PROMPT_TITLE', SYSTEM_PROMPTS[0]["title"])

        # Tavily search settings
        self.tavily_search_depth = os.getenv('TAVILY_SEARCH_DEPTH', 'advanced')
        self.tavily_max_tokens = int(os.getenv('TAVILY_MAX_TOKENS', '1500'))

        # Assistant settings
        self.command_history_length = int(os.getenv('COMMAND_HISTORY_LENGTH', '10'))

        # File paths
        self.log_file = Path(os.getenv('LOG_FILE', 'assistant.log'))
        self.cheat_sheet_path = Path(os.getenv('CHEAT_SHEET_PATH', Path.home() / '.croqli_cheatsheet.json'))

        # Brand colors
        self.brand_primary = BRAND_PRIMARY
        self.brand_secondary = BRAND_SECONDARY
        self.brand_text = BRAND_TEXT
        self.brand_dark = BRAND_DARK

    def validate(self):
        """Validate the configuration settings."""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment variables.")
        if not self.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not set in the environment variables.")
        
        # Add more validation as needed

    def to_dict(self):
        """Convert configuration to a dictionary."""
        return {
            'groq_api_key': self.groq_api_key,
            'tavily_api_key': self.tavily_api_key,
            'groq_model': self.groq_model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'system_prompt': self.system_prompt,
            'system_prompt_title': self.system_prompt_title,
            'tavily_search_depth': self.tavily_search_depth,
            'tavily_max_tokens': self.tavily_max_tokens,
            'command_history_length': self.command_history_length,
            'log_file': str(self.log_file),
            'cheat_sheet_path': str(self.cheat_sheet_path),
            'brand_primary': self.brand_primary,
            'brand_secondary': self.brand_secondary,
            'brand_text': self.brand_text,
            'brand_dark': self.brand_dark
        }

def load_config():
    env_path = Path('.env')
    if not env_path.exists():
        groq_key = inquirer.prompt([
            inquirer.Text('groq_key', message="Please enter your GROQ API key:")
        ])['groq_key']
        tavily_key = inquirer.prompt([
            inquirer.Text('tavily_key', message="Please enter your Tavily API key:")
        ])['tavily_key']

        env_path.touch()  # Create the .env file
        set_key(str(env_path), 'GROQ_API_KEY', groq_key)
        set_key(str(env_path), 'TAVILY_API_KEY', tavily_key)

    load_dotenv()
    """Load and validate the configuration."""
    config = Config()
    config.validate()
    return config

# Default settings for the chat model
DEFAULT_SETTINGS = {
    "model": "llama3-8b-8192",
    "max_tokens": 8192,
    "temperature": 0.7,
    "top_p": 1.0,
    "system_prompt": SYSTEM_PROMPTS[0]["prompt"],
    "system_prompt_title": SYSTEM_PROMPTS[0]["title"]
}

# Example usage
if __name__ == "__main__":
    config = load_config()
    print(config.to_dict())
    print("Default Settings:", DEFAULT_SETTINGS)
    print("System Prompts:", SYSTEM_PROMPTS)
