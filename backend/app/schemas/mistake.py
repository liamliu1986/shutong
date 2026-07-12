from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class MistakeCreate(BaseModel):
    child_id: str
    subject: str
    grade: Optional[str] = None
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
    grade: Optional[str] = None
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
    grade: Optional[str] = None
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

    @field_validator("grade", mode="before")
    @classmethod
    def _coerce_grade_to_string(cls, value):
        """兼容历史整数 grade 数据"""
        if isinstance(value, int):
            return str(value)
        return value


class MistakeListResponse(BaseModel):
    items: List[MistakeResponse]
    total: int
    page: int
    page_size: int
