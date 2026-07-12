"""
知识图谱 API 路由
提供学科、知识点、掌握度等接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.services.knowledge_graph_service import KnowledgeGraphService
from app.schemas.knowledge_graph import (
    SubjectResponse,
    SubjectGraphResponse,
    MasteryEntry,
)

router = APIRouter()


@router.get("/subjects", response_model=List[SubjectResponse])
async def get_subjects(current_user: dict = Depends(get_current_user)):
    """获取所有学科列表

    需要 JWT 认证
    """
    return await KnowledgeGraphService.get_subjects()


@router.get("/subjects/{subject_id}/graph", response_model=SubjectGraphResponse)
async def get_subject_graph(
    subject_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取学科知识图谱

    返回章节、知识点及关联关系
    需要 JWT 认证
    """
    return await KnowledgeGraphService.get_subject_graph(subject_id)


@router.post("/subjects/init-math")
async def init_math_graph(current_user: dict = Depends(get_current_user)):
    """初始化数学知识图谱

    清空并重建数学学科的知识图谱数据
    需要 JWT 认证
    """
    await KnowledgeGraphService.init_math_graph()
    return {"message": "数学知识图谱初始化完成"}


@router.get("/children/{child_id}/mastery", response_model=List[MasteryEntry])
async def get_child_mastery(
    child_id: str,
    subject_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取孩子知识点掌握度

    需要验证孩子属于当前用户
    需要 JWT 认证
    """
    # 验证孩子属于当前用户
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")

    return await KnowledgeGraphService.get_child_mastery(child_id, subject_id)
