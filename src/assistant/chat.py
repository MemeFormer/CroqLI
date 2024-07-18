# src/assistant/chat.py

from src.services.groq_api import GroqService
from src.ui.display import render_markdown
from src.config import load_config
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
import os

# Load environment variables
load_dotenv()

def load_or_create_env():
    """Load or create environment variables."""
    if not os.path.exists('.env'):
        with open('.env', 'w') as file:
            for key, value in config.DEFAULT_SETTINGS.items():
                file.write(f"{key}={value}\n")
    load_dotenv()

<<<<<<< HEAD
def get_groq_response(groq_service, input_text, history, DEFAULT_SETTINGS):
    """Get the GROQ response."""
    groq_model = os.getenv("GROQ_MODEL", DEFAULT_SETTINGS["GROQ_MODEL"])
    max_tokens = int(os.getenv("MAX_TOKENS", DEFAULT_SETTINGS["MAX_TOKENS"]))
    temperature = float(os.getenv("TEMPERATURE", DEFAULT_SETTINGS["TEMPERATURE"]))
    top_p = float(os.getenv("TOP_P", DEFAULT_SETTINGS["TOP_P"]))
    system_prompt = os.getenv("SYSTEM_PROMPT", DEFAULT_SETTINGS["SYSTEM_PROMPT"])
=======
def get_formatted_model_name(config):
    if "llama3-8b" in config.groq_model:
        model_emoji = "🦙8B"
    elif "llama3-70b" in config.groq_model:
        model_emoji = "🦙70B"
    elif "mixtral" in config.groq_model:
        model_emoji = "🌀"
    elif "gemma" in config.groq_model:
        model_emoji = "💎"
    else:
        model_emoji = "🤖"
    
    return f"{model_emoji} {config.groq_model}"

def get_groq_response(groq_service, input_text, history, config):
    config.load_system_prompts()  # Refresh prompts before each interaction
    messages = []
    if config.system_prompt:
        messages.append(ChatMessage(role="system", content=config.system_prompt))
    messages.extend([ChatMessage(role=msg["role"], content=msg["content"]) for msg in history])
    messages.append(ChatMessage(role="user", content=input_text))
>>>>>>> c099e0e (chaosINorder)

    body = {
        "model": groq_model,
        "messages": history + [{"role": "user", "content": input_text}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    if system_prompt:
        body["messages"].insert(0, {"role": "system", "content": system_prompt})

<<<<<<< HEAD
    response = groq_service.post("/chat/completions", json=body)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

=======
>>>>>>> c099e0e (chaosINorder)
def chat_mode(config, console):
    """Initiates the chat mode with configuration and console support."""
    load_or_create_env()
    # Utilize config for environment variables if needed
    groq_service = GroqService()

<<<<<<< HEAD
=======
    try:
        groq_service = GroqService()
    except Exception as e:
        console.print(f"Error initializing GroqService: {str(e)}", style="bold red")
        return

>>>>>>> c099e0e (chaosINorder)
    history = []

    display_banner(console, config)

    while True:
<<<<<<< HEAD
        questions = [
            inquirer.Text('message', message="Enter your message (or type 'exit' to quit): ")
        ]
        answers = inquirer.prompt(questions)
        input_text = answers['message']
        
        if input_text.lower() == 'exit':
            break

        response = get_groq_response(groq_service, input_text, history, config.DEFAULT_SETTINGS)
        console.print("Response:", style="bold green")
        render_markdown(response, console)
        history.append({"role": "user", "content": input_text})
        history.append({"role": "assistant", "content": response})

if __name__ != "__main__":
    # This block ensures that the chat loop doesn't start automatically when importing chat.py
    pass
else:
    config = load_config()  # Assuming load_config() is defined in src.config
=======
        user_input = console.input("[bold magenta]YOU:[/bold magenta] ")

        if user_input.lower() in ['/quit', '/back']:
            break
        elif user_input.lower() == '/save':
            if history:
                save_last_response(history[-1]["content"])
                console.print("Last response saved.", style="bold green")
            else:
                console.print("No response to save yet.", style="bold yellow")
            continue
        elif user_input.strip() == '':
            continue

        console.print()  # Add an empty line for better readability

        try:
            response = get_groq_response(groq_service, user_input, history, config)
            model_name = get_formatted_model_name(config)
            console.print(f"[bold cyan]{model_name}:[/bold cyan] [#00FF00]{response}[/#00FF00]")
            console.print()  # Add an empty line for better readability
            console.print("-" * 40, style="dim")  # Add a subtle separator line
            console.print()  # Add another empty line after the separator
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
        except Exception as e:
            console.print(f"An error occurred: {str(e)}", style="bold red")

    console.print("Exiting chat mode.", style="bold blue")

def display_banner(console, config):
    """Display a banner with model settings and tips."""
    model_name = get_formatted_model_name(config)
    model_settings = (
        f"[bold underline #00FFFF]SETTINGS:[/bold underline #00FFFF] "
        f"  {model_name}   "
        f"   🌡️  Temp.: [bold #00FFFF]{config.temperature}[/bold #00FFFF] "
        f"   🎯 Top-P: [bold #00FFFF]{config.top_p}[/bold #00FFFF] "
        f"   📏 Max Tokens: [bold #00FFFF]{config.max_tokens}[/bold #00FFFF]"
    )
    tips = (
        "    [bold underline #00FFFF]TIPS:[/bold underline #00FFFF]  "
        f"Save Last Response  [bold #00FFFF]/save[/bold #00FFFF]  "
        f"  |   Go To Menu  [bold #00FFFF]/back[/bold #00FFFF]  "
        f"  |   Shut Down  [bold #00FFFF]/quit[/bold #00FFFF]"
    )

    console.print("=" * 88, style="bold yellow")
    console.print(model_settings, style="bright_white")
    console.print(tips, style="bright_white")
    console.print("=" * 88, style="bold yellow")

def save_last_response(response):
    """Save the last response to a file."""
    with open("last_response.txt", "w") as f:
        f.write(response)

if __name__ == "__main__":
    config = load_config()
>>>>>>> c099e0e (chaosINorder)
    console = Console()
    chat_mode(config, console)