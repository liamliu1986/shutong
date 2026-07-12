"""
知识图谱 Pydantic 模型
定义知识图谱 API 的请求和响应数据结构
"""
from pydantic import BaseModel, Field
from typing import Optional, List


# ─── 请求模型（CRUD） ─────────────────────────────────────────────

class SubjectCreate(BaseModel):
    """创建学科请求"""
    id: str = Field(..., description="学科唯一标识，如 'math'")
    name: str = Field(..., description="学科中文名，如 '数学'")
    grade_level: Optional[str] = Field(None, description="适用年级范围，如 '7-12'")


class SubjectUpdate(BaseModel):
    """更新学科请求"""
    name: Optional[str] = None
    grade_level: Optional[str] = None


class ChapterCreate(BaseModel):
    """创建章节请求"""
    id: str = Field(..., description="章节唯一标识")
    name: str = Field(..., description="章节名称")
    order: int = Field(..., description="排序序号")


class ChapterUpdate(BaseModel):
    """更新章节请求"""
    name: Optional[str] = None
    order: Optional[int] = None


class KnowledgePointCreate(BaseModel):
    """创建知识点请求"""
    id: str = Field(..., description="知识点唯一标识")
    name: str = Field(..., description="知识点名称")
    description: Optional[str] = None
    importance: int = Field(3, ge=1, le=5, description="重要度 1-5")


class KnowledgePointUpdate(BaseModel):
    """更新知识点请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    importance: Optional[int] = Field(None, ge=1, le=5)


class KnowledgePointPosition(BaseModel):
    """知识点位置"""
    id: str
    x: float
    y: float


class RelationCreate(BaseModel):
    """创建关系请求"""
    from_id: str = Field(..., description="源知识点 ID")
    to_id: str = Field(..., description="目标知识点 ID")
    type: str = Field(..., description="关系类型: RELATED_TO 或 PREREQUISITE_OF")


# ─── 响应模型 ────────────────────────────────────────────────────

class KnowledgePointResponse(BaseModel):
    """知识点响应"""
    id: str
    name: str
    importance: int = 0
    description: Optional[str] = None
    pos_x: float = 0
    pos_y: float = 0


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
