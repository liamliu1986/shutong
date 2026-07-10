"""题库 Schema 定义

定义题目和试卷的请求/响应数据结构。
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ========== 题目 Schemas ==========

class QuestionOptionCreate(BaseModel):
    """题目选项创建"""
    label: str
    content: str
    is_correct: bool = False


class QuestionCreate(BaseModel):
    """题目创建请求"""
    child_id: str
    subject: str
    grade: int = Field(ge=1, le=12)
    question_type: str  # "choice" | "fill_blank" | "solve"
    question_text: str
    question_latex: str = ""
    question_image_url: str = ""
    options: List[QuestionOptionCreate] = []
    answer: str = ""
    explanation: str = ""
    chapter: str = ""
    knowledge_point_ids: List[str] = []
    difficulty: int = Field(ge=1, le=5, default=3)
    tags: List[str] = []
    source_type: str = "single"
    source_paper_id: Optional[str] = None
    source_paper_name: Optional[str] = None
    question_index: Optional[int] = None


class QuestionResponse(BaseModel):
    """题目响应"""
    id: str
    child_id: str
    subject: str
    grade: int
    question_type: str
    question_text: str
    question_latex: str = ""
    question_image_url: str = ""
    options: List[QuestionOptionCreate] = []
    answer: str = ""
    explanation: str = ""
    chapter: str = ""
    knowledge_point_ids: List[str] = []
    difficulty: int = 3
    tags: List[str] = []
    source_type: str = "single"
    source_paper_id: Optional[str] = None
    source_paper_name: Optional[str] = None
    question_index: Optional[int] = None
    used_count: int = 0
    correct_rate: float = 0.0
    created_at: datetime
    updated_at: datetime


class QuestionListResponse(BaseModel):
    """题目列表响应"""
    items: List[QuestionResponse]
    total: int
    page: int
    page_size: int


# ========== 试卷 Schemas ==========

class PaperCreate(BaseModel):
    """试卷创建请求"""
    child_id: str
    name: str
    subject: str
    grade: int = Field(ge=1, le=12)
    source: str = ""
    exam_date: Optional[datetime] = None
    total_score: Optional[int] = None


class PaperResponse(BaseModel):
    """试卷响应"""
    id: str
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
    status: str = "uploaded"
    created_at: datetime


class PaperListResponse(BaseModel):
    """试卷列表响应"""
    items: List[PaperResponse]
    total: int
