import os
import google.generativeai as genai
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """Actually uses Gemini, but kept name for compatibility"""
    
    def __init__(self):
        # Use your Gemini Key from .env
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        # Gemini handles embeddings differently
        self.embed_model = "models/text-embedding-004"

    def generate_embedding(self, text: str) -> List[float]:
        try:
            result = genai.embed_content(model=self.embed_model, content=text)
            return result['embedding']
        except Exception as e:
            logger.error(f"Gemini Embedding Error: {e}")
            raise

    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        try:
            # Convert OpenAI message format to Gemini format
            prompt = messages[-1]['content']
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini Chat Error: {e}")
            raise

    def translate_text(self, text: str, target_language: str = "Urdu") -> str:
        prompt = f"Translate this to {target_language}, keep technical terms in English: {text}"
        response = self.model.generate_content(prompt)
        return response.text

# Global instance
openai_service = OpenAIService()