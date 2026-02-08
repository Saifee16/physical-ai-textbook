"""
Content Personalization Service
"""
from typing import Dict, Optional, List
import logging
from services.openai_service import openai_service

logger = logging.getLogger(__name__)

class PersonalizationService:
    """Service for content personalization"""
    
    LEVEL_DESCRIPTIONS = {
        "beginner": "new to the topic with limited background",
        "intermediate": "some experience with related concepts",
        "advanced": "strong background and ready for deep technical content"
    }
    
    async def personalize_content(
        self,
        content: str,
        user_profile: Dict
    ) -> dict:
        """Personalize content based on user profile"""
        try:
            # Extract user levels
            software_level = user_profile.get('software_level', 'intermediate')
            hardware_level = user_profile.get('hardware_level', 'beginner')
            robotics_knowledge = user_profile.get('robotics_knowledge', False)
            learning_goals = user_profile.get('learning_goals', '')
            
            # Build focus areas
            focus_areas = []
            
            if software_level == 'beginner':
                focus_areas.append("software fundamentals and setup")
            
            if hardware_level == 'beginner':
                focus_areas.append("hardware basics and requirements")
            
            if not robotics_knowledge:
                focus_areas.append("robotics foundations")
            
            if learning_goals:
                focus_areas.append(f"alignment with goal: {learning_goals}")
            
            # Determine overall level (take the lower of software/hardware)
            level_priority = {"beginner": 0, "intermediate": 1, "advanced": 2}
            overall_level = software_level if level_priority.get(software_level, 1) <= level_priority.get(hardware_level, 1) else hardware_level
            
            # Personalize with OpenAI
            logger.info(f"Personalizing content for {overall_level} level")
            personalized = openai_service.personalize_content(
                content,
                overall_level,
                focus_areas if focus_areas else None
            )
            
            return {
                "personalized_content": personalized,
                "user_level": overall_level,
                "focus_areas": focus_areas,
                "modifications": self._generate_modification_summary(overall_level, focus_areas)
            }
        
        except Exception as e:
            logger.error(f"Personalization error: {e}")
            raise
    
    def _generate_modification_summary(self, level: str, focus_areas: List[str]) -> List[str]:
        """Generate summary of modifications made"""
        modifications = []
        
        if level == "beginner":
            modifications.append("Added detailed explanations for complex concepts")
            modifications.append("Simplified technical terminology")
            modifications.append("Included more step-by-step examples")
        elif level == "intermediate":
            modifications.append("Balanced theory with practical applications")
            modifications.append("Added intermediate-level examples")
        else:
            modifications.append("Included advanced technical details")
            modifications.append("Added optimization techniques")
            modifications.append("Referenced research papers and advanced topics")
        
        if "hardware" in str(focus_areas):
            modifications.append("Added hardware setup details and troubleshooting")
        
        if "software" in str(focus_areas):
            modifications.append("Expanded software installation and configuration")
        
        if "robotics foundations" in str(focus_areas):
            modifications.append("Included robotics background and fundamentals")
        
        return modifications

# Global instance
personalization_service = PersonalizationService()