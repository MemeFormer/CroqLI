# croqli/src/config.py
import inquirer
import os
import json
from pathlib import Path
from dotenv import load_dotenv, set_key

BRAND_PRIMARY = "#F55036"  # Orange
BRAND_SECONDARY = "#CCCCCC"  # Light gray
BRAND_TEXT = "#FFFFFF"  # White for text on primary background
BRAND_DARK = "#666666"  # Darker gray


class Config:

    
    def save_system_prompts(self):
        with open('system_prompts.json', 'w') as f:
            json.dump(self.SYSTEM_PROMPTS, f)

    def load_system_prompts(self):
        try:
            with open('system_prompts.json', 'r') as f:
                self.SYSTEM_PROMPTS = json.load(f)
        except FileNotFoundError:
            pass  # Use default prompts if file doesn't exist

    def set_active_prompt(self, index: int):
        self.active_prompt_index = index
        self.system_prompt = self.SYSTEM_PROMPTS[index]['prompt']
        self.save_system_prompts()

    def __init__(self):
        load_dotenv()

        
       
        self.SYSTEM_PROMPTS = [
            {"title": "Friendly Assistant", "prompt": "You are a helpful and friendly assistant."},
            {"title": "Technical Support", "prompt": "You are a technical support specialist, ready to solve complex issues."},
            {"title": "Creative Writer", "prompt": "You are a creative writer, full of imagination and vivid descriptions."},
            {"title": "Data Analyst", "prompt": "You are a data analyst, providing insights and detailed analysis."},
            {"title": "Casual Conversation", "prompt": "You are here for a casual chat, keeping the tone light and friendly."}
        ]

        self.DEFAULT_SETTINGS = {
            "GROQ_MODEL": "mixtral-8x7b-32768",
            "MAX_TOKENS": "8192",
            "TEMPERATURE": "0.7",
            "TOP_P": "1.0",
            "SYSTEM_PROMPT": ""
        }

<<<<<<< HEAD
        # API Keys
=======
        self.model_max_tokens = {
            "llama3-8b-8192": 8192,
            "llama3-70b-8192": 8192,
            "mixtral-8x7b-32768": 32768,
            "gemma-7b-it": 8192
        }

>>>>>>> c099e0e (chaosINorder)
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')

        self.groq_model = os.getenv('GROQ_MODEL', self.DEFAULT_SETTINGS["GROQ_MODEL"])
        self.max_tokens = int(os.getenv('MAX_TOKENS', self.DEFAULT_SETTINGS["MAX_TOKENS"]))
        self.temperature = float(os.getenv('TEMPERATURE', self.DEFAULT_SETTINGS["TEMPERATURE"]))
        self.top_p = float(os.getenv('TOP_P', self.DEFAULT_SETTINGS["TOP_P"]))
        self.system_prompt = str(os.getenv("SYSTEM_PROMPT", self.DEFAULT_SETTINGS["SYSTEM_PROMPT"]))
        
        self.tavily_search_depth = os.getenv('TAVILY_SEARCH_DEPTH', 'advanced')
        self.tavily_max_tokens = int(os.getenv('TAVILY_MAX_TOKENS', '1500'))

        # Assistant settings
        self.command_history_length = int(os.getenv('COMMAND_HISTORY_LENGTH', '10'))

        self.log_file = Path(os.getenv('LOG_FILE', 'assistant.log'))
        self.cheat_sheet_path = Path(os.getenv('CHEAT_SHEET_PATH', Path.home() / '.croqli_cheatsheet.json'))
        self.command_history_path = Path(os.getenv('COMMAND_HISTORY_PATH', Path.home() / '.croqli_command_history.txt'))


        self.brand_primary = BRAND_PRIMARY
        self.brand_secondary = BRAND_SECONDARY
        self.brand_text = BRAND_TEXT
        self.brand_dark = BRAND_DARK

        self.active_prompt_index = int(os.getenv('ACTIVE_PROMPT_INDEX', '0'))
        self.load_system_prompts()

        

    def update_system_prompts(self, prompts):
        self.SYSTEM_PROMPTS = prompts
        self.system_prompt = prompts[self.active_prompt_index]['prompt']
        self.save_to_env('SYSTEM_PROMPT', self.system_prompt)
        self.save_to_env('SYSTEM_PROMPT_TITLE', prompts[self.active_prompt_index]['title'])
    
    def get(self, key, default=None):
        return getattr(self, key, default)

    def validate(self):
        """Validate the configuration settings."""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not set in the environment variables.")
        if not self.tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not set in the environment variables.")
        
<<<<<<< HEAD
        # Add more validation as needed
=======
    def save_to_env(self, key, value):
        set_key('.env', key, str(value))
        setattr(self, key.lower(), value)

    def update_model_settings(self, model=None, max_tokens=None, temperature=None, top_p=None):
        if model:
            self.save_to_env('GROQ_MODEL', model)
            self.groq_model = model
        if max_tokens is not None:
            self.save_to_env('MAX_TOKENS', str(max_tokens))
            self.max_tokens = max_tokens
        if temperature is not None:
            self.save_to_env('TEMPERATURE', str(temperature))
            self.temperature = temperature
        if top_p is not None:
            self.save_to_env('TOP_P', str(top_p))
            self.top_p = top_p
    def update_api_keys(self, groq_key=None, tavily_key=None):
        if groq_key:
            self.save_to_env('GROQ_API_KEY', groq_key)
        if tavily_key:
            self.save_to_env('TAVILY_API_KEY', tavily_key)

    def update_system_prompts(self, prompts):
        self.SYSTEM_PROMPTS = prompts
        self.save_to_env('SYSTEM_PROMPT', prompts[0]['prompt'])
        self.save_to_env('SYSTEM_PROMPT_TITLE', prompts[0]['title'])
>>>>>>> c099e0e (chaosINorder)

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

        env_path.touch()  
        set_key(str(env_path), 'GROQ_API_KEY', groq_key)
        set_key(str(env_path), 'TAVILY_API_KEY', tavily_key)

    load_dotenv()
    """Load and validate the configuration."""
    config = Config()
<<<<<<< HEAD
    config.validate()
    return config



## Example usage
#if __name__ == "__main__":
    #config = load_config()
    #print(config.to_dict())
    #print("Default Settings:", config.DEFAULT_SETTINGS)
    #print("System Prompts:", config.SYSTEM_PROMPTS)
=======
    return config
>>>>>>> c099e0e (chaosINorder)
