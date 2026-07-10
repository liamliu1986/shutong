from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MistakeModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    subject: str
    grade: int
    chapter: str
    knowledge_points: List[str] = []

    question_image_url: str = ""
    question_text: str = ""
    question_latex: str = ""

    answer: str = ""
    explanation: str = ""
    explanation_gif_url: str = ""

    difficulty: int = Field(ge=1, le=5, default=3)
    source: str = ""
    tags: List[str] = []

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
