"""
Translation Service
"""
import hashlib
from typing import Optional
import logging
from database.postgres import get_cached_translation, cache_translation
from services.openai_service import openai_service

logger = logging.getLogger(__name__)

class TranslationService:
    """Service for content translation"""
    
    @staticmethod
    def generate_content_hash(content: str) -> str:
        """Generate hash of content for caching"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    async def translate_content(
        self,
        content: str,
        chapter_id: str,
        target_language: str = "ur"
    ) -> dict:
        """Translate content with caching"""
        try:
            # Generate content hash
            content_hash = self.generate_content_hash(content)
            
            # Check cache
            cached = await get_cached_translation(chapter_id, content_hash, target_language)
            if cached:
                logger.info(f"Translation cache hit for {chapter_id}")
                return {
                    "translated_content": cached,
                    "cached": True,
                    "target_language": target_language
                }
            
            # Translate with OpenAI
            logger.info(f"Translating {chapter_id} to {target_language}")
            language_name = "Urdu" if target_language == "ur" else target_language
            translated = openai_service.translate_text(content, language_name)
            
            # Cache translation
            await cache_translation(chapter_id, content_hash, target_language, translated)
            
            return {
                "translated_content": translated,
                "cached": False,
                "target_language": target_language
            }
        
        except Exception as e:
            logger.error(f"Translation error: {e}")
            raise

# Global instance
translation_service = TranslationService()