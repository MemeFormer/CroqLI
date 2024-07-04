# croqli/src/assistant/__init__py 
print("Debug: Entering src/assistant/__init__.py")


from .chat import chat_mode
from .cli_assistant import cli_assistant_mode

__all__ = ['chat_mode', 'cli_assistant_mode']

print("Debug: Finished src/assistant/__init__.py")