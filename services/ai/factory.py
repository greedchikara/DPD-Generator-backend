from .ai_providers.base import AIProvider
from .ai_providers.gemini_provider import GeminiAIProvider

def get_ai_provider(provider_name: str = "gemini") -> AIProvider:
    if(provider_name == "gemini"):
        return GeminiAIProvider()    
    else:
        raise ValueError(f"Unsupported AI provider: {provider_name}")
    
def ai_provider_dependency(provider_name: str = 'gemini') -> AIProvider:
    return get_ai_provider(provider_name)
