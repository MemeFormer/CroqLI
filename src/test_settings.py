# test_settings.py

import pytest
from unittest.mock import patch, MagicMock
from src.main import (
    settings_menu, model_settings_menu, api_keys_menu, system_prompts_menu,
    prompt_actions_menu, edit_prompt, change_title, move_prompt, pin_unpin_prompt,
    delete_prompt, use_prompt, add_new_prompt, switch_active_prompt
)
from src.config import Config
import json
from src.config import load_config
from src.services.groq_api import GroqService
@pytest.fixture
def mock_config():
    config = MagicMock(spec=Config)
    config.SYSTEM_PROMPTS = [
        {"title": "Prompt 1", "prompt": "This is prompt 1", "pinned": False},
        {"title": "Prompt 2", "prompt": "This is prompt 2", "pinned": False}
    ]
    config.active_prompt_index = 0
    config.groq_model = "mixtral-8x7b-32768"
    config.max_tokens = 8192
    config.temperature = 0.7
    config.top_p = 1.0
    return config

def test_settings_menu_options(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'setting': 'Model Settings'},
            {'setting': 'API Keys'},
            {'setting': 'System Prompts'},
            {'setting': 'back'}
        ]
        
        with patch('src.main.model_settings_menu') as mock_model_settings:
            with patch('src.main.api_keys_menu') as mock_api_keys:
                with patch('src.main.system_prompts_menu') as mock_system_prompts:
                    result = settings_menu(mock_config)
        
        assert mock_model_settings.called
        assert mock_api_keys.called
        assert mock_system_prompts.called
        assert result == 'back'

def test_model_settings_menu(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'setting': 'Model Name'},
            {'model': 'llama3-8b-8192'},
            {'setting': 'Max Tokens'},
            {'max_tokens': '4096'},
            {'setting': 'Temperature'},
            {'temperature': '0.7'},
            {'setting': 'Top P'},
            {'top_p': '0.9'},
            {'setting': 'Back'}
        ]
        
        with patch('src.main.set_key') as mock_set_key:
            model_settings_menu(mock_config)
        
        assert mock_config.groq_model == 'llama3-8b-8192'
        mock_config.update_model_settings.assert_any_call(max_tokens=4096)
        mock_config.update_model_settings.assert_any_call(temperature=0.7)
        mock_config.update_model_settings.assert_any_call(top_p=0.9)
        assert mock_set_key.call_count == 4

def test_api_keys_menu(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'groq_key': 'new_groq_key'},
            {'tavily_key': 'new_tavily_key'}
        ]
        
        with patch('src.main.set_key') as mock_set_key:
            api_keys_menu(mock_config)
        
        mock_set_key.assert_any_call('.env', 'GROQ_API_KEY', 'new_groq_key')
        mock_set_key.assert_any_call('.env', 'TAVILY_API_KEY', 'new_tavily_key')

def test_system_prompts_menu(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'prompt': 'Add New Prompt'},
            {'title': 'New Prompt'},
            {'prompt': 'This is a new prompt'},
            {'prompt': 'back'}
        ]
        
        result = system_prompts_menu(mock_config)
        
        assert len(mock_config.SYSTEM_PROMPTS) == 3
        assert mock_config.SYSTEM_PROMPTS[-1]['title'] == 'New Prompt'
        assert mock_config.SYSTEM_PROMPTS[-1]['prompt'] == 'This is a new prompt'
        assert result == 'back'

def test_prompt_actions_menu(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'action': 'Edit Prompt'},
            {'prompt': 'Updated prompt'},
            {'action': 'Change Title'},
            {'title': 'Updated Title'},
            {'action': 'Move Up'},
            {'action': 'Pin/Unpin'},
            {'action': 'Use'},
        ]
        
        with patch('src.main.edit_prompt') as mock_edit:
            with patch('src.main.change_title') as mock_change_title:
                with patch('src.main.move_prompt') as mock_move:
                    with patch('src.main.pin_unpin_prompt') as mock_pin:
                        with patch('src.main.use_prompt') as mock_use:
                            result = prompt_actions_menu(mock_config, 0)
        
        assert mock_edit.called
        assert mock_change_title.called
        assert mock_move.called
        assert mock_pin.called
        assert mock_use.called
        assert result == 'chat'

def test_edit_prompt(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.return_value = {'prompt': 'Updated prompt'}
        edit_prompt(mock_config, 0)
    
    assert mock_config.SYSTEM_PROMPTS[0]['prompt'] == 'Updated prompt'
    mock_config.update_system_prompts.assert_called_once()

def test_change_title(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.return_value = {'title': 'New Title'}
        change_title(mock_config, 0)
    
    assert mock_config.SYSTEM_PROMPTS[0]['title'] == 'New Title'
    mock_config.update_system_prompts.assert_called_once()

def test_move_prompt(mock_config):
    result = move_prompt(mock_config, 0, 1)
    assert result == 1
    assert mock_config.SYSTEM_PROMPTS[0]['title'] == 'Prompt 2'
    assert mock_config.SYSTEM_PROMPTS[1]['title'] == 'Prompt 1'
    mock_config.update_system_prompts.assert_called_once()

def test_pin_unpin_prompt(mock_config):
    pin_unpin_prompt(mock_config, 0)
    assert mock_config.SYSTEM_PROMPTS[0]['pinned'] == True
    mock_config.update_system_prompts.assert_called_once()

def test_delete_prompt(mock_config):
    result = delete_prompt(mock_config, 0)
    assert result == True
    assert len(mock_config.SYSTEM_PROMPTS) == 1
    assert mock_config.SYSTEM_PROMPTS[0]['title'] == 'Prompt 2'
    mock_config.update_system_prompts.assert_called_once()



def test_use_prompt(mock_config):
    with patch('src.main.set_key') as mock_set_key:
        result = use_prompt(mock_config, 1)
    
    assert mock_config.active_prompt_index == 1
    assert mock_config.system_prompt == "This is prompt 2"
    mock_set_key.assert_any_call('.env', 'SYSTEM_PROMPT', "This is prompt 2")
    mock_set_key.assert_any_call('.env', 'SYSTEM_PROMPT_TITLE', "Prompt 2")
    assert result == 'main_menu'
    mock_config.system_prompt = "This is prompt 2"
    
def test_add_new_prompt(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'title': 'New Prompt'},
            {'prompt': 'This is a new prompt'}
        ]
        add_new_prompt(mock_config)
    
    assert len(mock_config.SYSTEM_PROMPTS) == 3
    assert mock_config.SYSTEM_PROMPTS[-1]['title'] == 'New Prompt'
    assert mock_config.SYSTEM_PROMPTS[-1]['prompt'] == 'This is a new prompt'
    assert mock_config.SYSTEM_PROMPTS[-1]['pinned'] == False
    mock_config.update_system_prompts.assert_called_once()

def test_switch_active_prompt(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.return_value = {'active_prompt': '2. Prompt 2'}
        with patch('src.main.use_prompt') as mock_use_prompt:
            mock_use_prompt.return_value = 'chat'
            result = switch_active_prompt(mock_config)
    
    mock_use_prompt.assert_called_once_with(mock_config, 1)
    assert result == 'chat'

# Tests for GroqService
@pytest.fixture
def mock_groq_service():
    with patch('src.services.groq_api.Groq') as mock_groq:
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        yield GroqService()

def test_groq_service_init(mock_groq_service):
    assert mock_groq_service.client is not None
    assert mock_groq_service.model_params.model_name == mock_groq_service.config.groq_model
    assert mock_groq_service.model_params.max_tokens == mock_groq_service.config.max_tokens
    assert mock_groq_service.model_params.temperature == mock_groq_service.config.temperature
    assert mock_groq_service.model_params.top_p == mock_groq_service.config.top_p

def test_groq_service_generate_response(mock_groq_service):
    mock_messages = [ChatMessage(role="user", content="Hello")]
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello, how can I help you?"
    mock_groq_service.client.chat.completions.create.return_value = mock_response

    response = mock_groq_service.generate_response(mock_messages)

    assert response == "Hello, how can I help you?"
    mock_groq_service.client.chat.completions.create.assert_called_once()

def test_groq_service_generate_response_error(mock_groq_service):
    mock_messages = [ChatMessage(role="user", content="Hello")]
    mock_groq_service.client.chat.completions.create.side_effect = Exception("API Error")

    with pytest.raises(Exception):
        mock_groq_service.generate_response(mock_messages)

# Tests for Config
def test_config_init():
    with patch('src.config.load_dotenv'):
        with patch('src.config.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key, default=None: default
            config = Config()
    
    assert config.groq_model == "mixtral-8x7b-32768"
    assert config.max_tokens == 8192
    assert config.temperature == 0.7
    assert config.top_p == 1.0
    assert len(config.SYSTEM_PROMPTS) == 5

def test_config_save_and_load_system_prompts(tmp_path):
    config = Config()
    config.SYSTEM_PROMPTS = [{"title": "Test Prompt", "prompt": "This is a test"}]
    
    with patch('src.config.open') as mock_open:
        mock_open.return_value.__enter__.return_value = MagicMock()
        config.save_system_prompts()
        mock_open.assert_called_once_with('system_prompts.json', 'w')
        mock_open.return_value.__enter__.return_value.write.assert_called_once()

    with patch('src.config.open') as mock_open:
        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(config.SYSTEM_PROMPTS)
        config.load_system_prompts()
        mock_open.assert_called_once_with('system_prompts.json', 'r')
        assert config.SYSTEM_PROMPTS == [{"title": "Test Prompt", "prompt": "This is a test"}]

def test_config_set_active_prompt():
    config = Config()
    config.SYSTEM_PROMPTS = [
        {"title": "Prompt 1", "prompt": "This is prompt 1"},
        {"title": "Prompt 2", "prompt": "This is prompt 2"}
    ]
    
    with patch('src.config.Config.save_system_prompts') as mock_save:
        config.set_active_prompt(1)
        assert config.active_prompt_index == 1
        assert config.system_prompt == "This is prompt 2"
        mock_save.assert_called_once()

def test_config_update_model_settings():
    config = Config()
    with patch('src.config.set_key') as mock_set_key:
        config.update_model_settings(model="new-model", max_tokens=1000, temperature=0.5, top_p=0.9)
    
    assert config.groq_model == "new-model"
    assert config.max_tokens == 1000
    assert config.temperature == 0.5
    assert config.top_p == 0.9
    assert mock_set_key.call_count == 4

def test_config_update_api_keys():
    config = Config()
    with patch('src.config.set_key') as mock_set_key:
        config.update_api_keys(groq_key="new_groq_key", tavily_key="new_tavily_key")
    
    assert mock_set_key.call_count == 2
    mock_set_key.assert_any_call('.env', 'GROQ_API_KEY', "new_groq_key")
    mock_set_key.assert_any_call('.env', 'TAVILY_API_KEY', "new_tavily_key")


def test_config_to_dict():
    config = Config()
    config_dict = config.to_dict()
    
    assert isinstance(config_dict, dict)
    assert 'groq_api_key' in config_dict
    assert 'tavily_api_key' in config_dict
    assert 'groq_model' in config_dict
    assert 'max_tokens' in config_dict
    assert 'temperature' in config_dict
    assert 'top_p' in config_dict
    assert 'system_prompt' in config_dict
    assert 'system_prompt_title' in config_dict
    assert 'tavily_search_depth' in config_dict
    assert 'tavily_max_tokens' in config_dict
    assert 'command_history_length' in config_dict
    assert 'log_file' in config_dict
    assert 'cheat_sheet_path' in config_dict
    assert 'brand_primary' in config_dict
    assert 'brand_secondary' in config_dict
    assert 'brand_text' in config_dict
    assert 'brand_dark' in config_dict

def test_config_validate():
    config = Config()
    config.groq_api_key = "test_groq_key"
    config.tavily_api_key = "test_tavily_key"
    
    # This should not raise an exception
    config.validate()
    
    # Test with missing API keys
    config.groq_api_key = None
    with pytest.raises(ValueError, match="GROQ_API_KEY is not set in the environment variables."):
        config.validate()
    
    config.groq_api_key = "test_groq_key"
    config.tavily_api_key = None
    with pytest.raises(ValueError, match="TAVILY_API_KEY is not set in the environment variables."):
        config.validate()

def test_load_config():
    with patch('src.config.Path.exists') as mock_exists:
        with patch('src.config.inquirer.prompt') as mock_prompt:
            with patch('src.config.Path.touch') as mock_touch:
                with patch('src.config.set_key') as mock_set_key:
                    with patch('src.config.load_dotenv') as mock_load_dotenv:
                        mock_exists.return_value = False
                        mock_prompt.side_effect = [
                            {'groq_key': 'test_groq_key'},
                            {'tavily_key': 'test_tavily_key'}
                        ]
                        
                        config = load_config()
                        
                        assert mock_exists.called
                        assert mock_prompt.call_count == 2
                        assert mock_touch.called
                        assert mock_set_key.call_count == 2
                        assert mock_load_dotenv.called
                        assert isinstance(config, Config)

# Test for model_settings_menu with invalid inputs
def test_model_settings_menu_invalid_inputs(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'setting': 'Max Tokens'},
            {'max_tokens': 'invalid'},  # Invalid input
            {'max_tokens': '4096'},
            {'setting': 'Temperature'},
            {'temperature': '2.0'},  # Invalid input
            {'temperature': '0.7'},
            {'setting': 'Top P'},
            {'top_p': '-0.1'},  # Invalid input
            {'top_p': '0.9'},
            {'setting': 'Back'}
        ]
        
        with patch('src.main.set_key'):
            model_settings_menu(mock_config)
        
        assert mock_config.update_model_settings.call_count == 3
        mock_config.update_model_settings.assert_any_call(max_tokens=4096)
        mock_config.update_model_settings.assert_any_call(temperature=0.7)
        mock_config.update_model_settings.assert_any_call(top_p=0.9)

# Test for system_prompts_menu with various actions
def test_system_prompts_menu_actions(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'prompt': '    Prompt 1'},  # Select first prompt
            {'action': 'Edit Prompt'},
            {'prompt': 'Updated prompt 1'},
            {'action': 'back'},
            {'prompt': 'Add New Prompt'},
            {'title': 'New Prompt'},
            {'prompt': 'This is a new prompt'},
            {'prompt': 'Switch Active Prompt'},
            {'active_prompt': '2. Prompt 2'},
            {'prompt': 'back'}
        ]
        
        with patch('src.main.prompt_actions_menu') as mock_actions_menu:
            with patch('src.main.add_new_prompt') as mock_add_prompt:
                with patch('src.main.switch_active_prompt') as mock_switch_prompt:
                    mock_actions_menu.return_value = 'back'
                    mock_switch_prompt.return_value = 'back'
                    
                    result = system_prompts_menu(mock_config)
        
        assert mock_actions_menu.called
        assert mock_add_prompt.called
        assert mock_switch_prompt.called
        assert result == 'back'

# Test for prompt_actions_menu with delete action
def test_prompt_actions_menu_delete(mock_config):
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.side_effect = [
            {'action': 'Delete'},
            {'action': 'back'}
        ]
        
        with patch('src.main.delete_prompt') as mock_delete:
            mock_delete.return_value = True
            result = prompt_actions_menu(mock_config, 0)
        
        assert mock_delete.called
        assert result == 'back'

# Test for delete_prompt with last prompt
def test_delete_prompt_last_prompt(mock_config):
    mock_config.SYSTEM_PROMPTS = [{"title": "Last Prompt", "prompt": "This is the last prompt"}]
    
    result = delete_prompt(mock_config, 0)
    
    assert result == False
    assert len(mock_config.SYSTEM_PROMPTS) == 1