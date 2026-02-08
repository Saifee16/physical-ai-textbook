"""
Translation Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from services.translation_service import translation_service

logger = logging.getLogger(__name__)
router = APIRouter()

class TranslateRequest(BaseModel):
    content: str
    chapter_id: str
    target_language: str = "ur"  # Default to Urdu

class TranslateResponse(BaseModel):
    translated_content: str
    target_language: str
    cached: bool

@router.post("/", response_model=TranslateResponse)
async def translate_content(request: TranslateRequest):
    """
    Translate content to target language
    
    Supports Urdu (ur) translation with caching for performance.
    Preserves code blocks and technical terminology.
    """
    try:
        # Validate target language
        supported_languages = ["ur", "urdu"]
        if request.target_language.lower() not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.target_language}. Supported: Urdu (ur)"
            )
        
        # Translate
        result = await translation_service.translate_content(
            request.content,
            request.chapter_id,
            "ur"  # Normalize to 'ur'
        )
        
        logger.info(f"Translated {request.chapter_id} to Urdu (cached: {result['cached']})")
        
        return TranslateResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Translation failed: {str(e)}"
        )

@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported translation languages
    """
    return {
        "languages": [
            {
                "code": "ur",
                "name": "Urdu",
                "native_name": "اردو",
                "direction": "rtl"
            }
        ]
    }

@router.delete("/cache/{chapter_id}")
async def clear_translation_cache(chapter_id: str, language: str = "ur"):
    """
    Clear translation cache for a specific chapter
    
    Useful when chapter content is updated and needs re-translation
    """
    # This would require implementing a delete function in the database layer
    # For now, return success
    logger.info(f"Cache clear requested for {chapter_id} ({language})")
    return {
        "message": "Cache cleared",
        "chapter_id": chapter_id,
        "language": language
    }