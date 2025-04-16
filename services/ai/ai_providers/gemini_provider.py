import os
from .base import AIProvider
from google import genai



class GeminiAIProvider(AIProvider):
    def __init__(self):
        super().__init__()
        self.ai_client = genai.Client(
            api_key = os.getenv('GEMINI_API_KEY')
        )  

    def generate_content(self, model: str, prompt: str) -> str:
        response = self.ai_client.models.generate_content(model=model,contents=prompt)
        return response.text 