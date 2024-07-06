# croqli/src/models.py

from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# src/models/models.py

class ChatMessage(BaseModel):
    role: str
    content: str

class SearchResult(BaseModel):
    query: str
    context: str
    summary: str

# Add any other model classes you need here

class LLMModelParams(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str
    max_tokens: int
    temperature: float
    top_p: float

class LLMModelParams(BaseModel):
    model: str = Field(..., alias="model_name")
    max_tokens: int
    temperature: float
    top_p: float

    class Config:
        allow_population_by_field_name = True

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

class UserProfile(BaseModel):
    preferred_model: str
    favorite_prompts: List[str]
    search_frequency: float  # e.g., how often the user tends to need search results

class AssistantConfig(BaseModel):
    llm_params: LLMModelParams
    system_prompts: List[SystemPrompt]
    user_profile: Optional[UserProfile]

