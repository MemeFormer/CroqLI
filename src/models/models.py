# croqli/src/models/models.py

from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# src/models/models.py

class SearchResult(BaseModel):
    query: str
    context: str
    summary: str

class LLMModelParams(BaseModel):
    model_name: str
    max_tokens: int
    temperature: float
    top_p: float

class SystemPrompt(BaseModel):
    title: str
    prompt: str

class SearchResult(BaseModel):
    query: str
    context: str
    summary: str

class ChatMessage(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    messages: List[ChatMessage]

class AssistantResponse(BaseModel):
    text: str
    source: str  # e.g., "chat", "search", "system"
    confidence: Optional[float]

class SystemPrompt(BaseModel):
    title: str
    prompt: str

class UserProfile(BaseModel):
    preferred_model: str
    favorite_prompts: List[str]
    search_frequency: float  # e.g., how often the user tends to need search results
    max_tokens: int
    temperature: float
    top_p: float

class AssistantConfig(BaseModel):
    llm_params: LLMModelParams
    system_prompts: List[SystemPrompt]
    user_profile: Optional[UserProfile]