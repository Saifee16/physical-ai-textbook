from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

class UserProfile(BaseModel):
    user_id: str
    software_level: str
    hardware_level: str
    robotics_knowledge: bool
    learning_goals: Optional[str]