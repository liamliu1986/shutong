"""
知识图谱 Pydantic 模型
定义知识图谱 API 的请求和响应数据结构
"""
from pydantic import BaseModel
from typing import Optional, List


class KnowledgePointResponse(BaseModel):
    """知识点响应"""
    id: str
    name: str
    importance: int = 0
    description: Optional[str] = None


class ChapterResponse(BaseModel):
    """章节响应"""
    id: str
    name: str
    order: int
    knowledge_points: List[KnowledgePointResponse] = []


class RelationResponse(BaseModel):
    """关系响应"""
    from_id: str
    to_id: str
    type: str  # "RELATED_TO" or "PREREQUISITE_OF"


class SubjectResponse(BaseModel):
    """学科响应"""
    id: str
    name: str
    grade_level: Optional[str] = None


class SubjectGraphResponse(BaseModel):
    """学科知识图谱响应"""
    subject_id: str
    chapters: List[ChapterResponse]
    relations: List[RelationResponse]


class MasteryEntry(BaseModel):
    """掌握度条目"""
    kp_id: str
    mastery_score: float
    total_attempts: int
    last_updated: Optional[str] = None
