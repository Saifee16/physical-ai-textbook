from pydantic import BaseModel
from typing import Optional


class ChapterCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ChapterResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    content: Optional[str]

