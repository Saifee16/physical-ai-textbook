from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: Optional[datetime] = None

class ChatSession(BaseModel):
    id: str
    user_id: Optional[str]
    messages: List[ChatMessage] = []
    created_at: datetime