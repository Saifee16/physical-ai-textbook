"""
Content Personalization Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import logging

from routes.auth import get_current_user
from database.postgres import get_user_profile
from services.personalization_service import personalization_service

logger = logging.getLogger(__name__)
router = APIRouter()

class PersonalizeRequest(BaseModel):
    content: str
    chapter_id: str

class PersonalizeResponse(BaseModel):
    personalized_content: str
    user_level: str
    focus_areas: List[str]
    modifications: List[str]

@router.post("/", response_model=PersonalizeResponse)
async def personalize_content(
    request: PersonalizeRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Personalize content based on user profile
    
    Requires authentication. Adapts content difficulty and focus
    based on user's software/hardware level and robotics knowledge.
    """
    try:
        # Get user profile
        profile = await get_user_profile(user_id)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail="User profile not found"
            )
        
        # Personalize content
        result = await personalization_service.personalize_content(
            request.content,
            profile
        )
        
        logger.info(f"Content personalized for user {user_id}, chapter {request.chapter_id}")
        
        return PersonalizeResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Personalization error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Personalization failed: {str(e)}"
        )

@router.post("/preview")
async def preview_personalization(
    request: PersonalizeRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Preview what personalization would look like without applying it
    """
    try:
        profile = await get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get just the modifications summary
        modifications = personalization_service._generate_modification_summary(
            profile.get('software_level', 'intermediate'),
            []
        )
        
        return {
            "user_level": profile.get('software_level', 'intermediate'),
            "will_modify": modifications,
            "chapter_id": request.chapter_id
        }
    
    except Exception as e:
        logger.error(f"Preview error: {e}")
        raise HTTPException(status_code=500, detail="Preview failed")