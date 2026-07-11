"""题库数据模型

定义题目和试卷的数据结构。
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuestionOption(BaseModel):
    """题目选项"""
    label: str
    content: str
    is_correct: bool = False


class QuestionModel(BaseModel):
    """题目模型"""
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    subject: str
    grade: int

    question_type: str  # "choice" | "fill_blank" | "solve"
    question_text: str
    question_latex: str = ""
    question_image_url: str = ""

    options: List[QuestionOption] = []
    answer: str = ""
    explanation: str = ""

    chapter: str = ""
    knowledge_point_ids: List[str] = []
    difficulty: int = Field(ge=1, le=5, default=3)
    tags: List[str] = []

    source_type: str = "single"  # "single" | "paper"
    source_paper_id: Optional[str] = None
    source_paper_name: Optional[str] = None
    question_index: Optional[int] = None

    used_count: int = 0
    correct_rate: float = 0.0

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True


class PaperModel(BaseModel):
    """试卷模型"""
    id: Optional[str] = Field(None, alias="_id")
    child_id: str
    name: str
    subject: str
    grade: int

    images: List[dict] = []
    question_ids: List[str] = []
    question_count: int = 0

    source: str = ""
    exam_date: Optional[datetime] = None
    total_score: Optional[int] = None

    status: str = "uploaded"  # "uploaded" | "processing" | "completed" | "failed"
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
