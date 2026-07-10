from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MistakeCreate(BaseModel):
    child_id: str
    subject: str
    grade: int = Field(ge=1, le=12)
    chapter: str
    question_text: str = ""
    question_image_url: str = ""
    question_latex: str = ""
    answer: str = ""
    explanation: str = ""
    difficulty: int = Field(ge=1, le=5, default=3)
    source: str = ""
    tags: List[str] = []
    knowledge_points: List[str] = []


class MistakeUpdate(BaseModel):
    subject: Optional[str] = None
    grade: Optional[int] = Field(None, ge=1, le=12)
    chapter: Optional[str] = None
    question_text: Optional[str] = None
    question_image_url: Optional[str] = None
    question_latex: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None
    explanation_gif_url: Optional[str] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    knowledge_points: Optional[List[str]] = None


class MistakeResponse(BaseModel):
    id: str
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
    difficulty: int = 3
    source: str = ""
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime


class MistakeListResponse(BaseModel):
    items: List[MistakeResponse]
    total: int
    page: int
    page_size: int
