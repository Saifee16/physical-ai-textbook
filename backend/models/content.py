from pydantic import BaseModel
from typing import Optional

class Content(BaseModel):
    chapter_id: str
    title: str
    content: str
    personalized: Optional[bool] = False
    translated: Optional[bool] = False