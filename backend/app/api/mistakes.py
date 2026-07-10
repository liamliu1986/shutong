"""错题本 API 路由

提供错题的 CRUD 操作和 AI 解析接口。
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_mongodb
from app.dependencies import get_current_user
from app.schemas.mistake import (
    MistakeCreate,
    MistakeUpdate,
    MistakeResponse,
    MistakeListResponse,
)
from app.services.mistake_service import MistakeService
from app.services.ocr_service import OCRService

router = APIRouter()


def get_mistake_service(db: AsyncIOMotorDatabase = Depends(get_mongodb)) -> MistakeService:
    """获取错题服务实例"""
    return MistakeService(db)


def _verify_child_access(current_user: dict, child_id: str):
    """验证 child_id 属于当前用户"""
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")


@router.post("/mistakes", response_model=MistakeResponse, status_code=200)
async def create_mistake(
    data: MistakeCreate,
    current_user: dict = Depends(get_current_user),
    service: MistakeService = Depends(get_mistake_service),
):
    """
    创建错题

    - **child_id**: 孩子 ID
    - **subject**: 科目
    - **grade**: 年级
    - **chapter**: 章节
    - **question_text**: 题目文本
    """
    _verify_child_access(current_user, data.child_id)
    return await service.create_mistake(data)


@router.get("/mistakes", response_model=MistakeListResponse)
async def get_mistakes(
    child_id: str = Query(..., description="孩子 ID"),
    subject: str = Query(None, description="科目筛选"),
    chapter: str = Query(None, description="章节筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: dict = Depends(get_current_user),
    service: MistakeService = Depends(get_mistake_service),
):
    """
    获取错题列表

    支持按科目和章节筛选，支持分页。
    """
    _verify_child_access(current_user, child_id)
    return await service.get_mistakes(
        child_id=child_id,
        subject=subject,
        chapter=chapter,
        page=page,
        page_size=page_size,
    )


@router.get("/mistakes/{mistake_id}", response_model=MistakeResponse)
async def get_mistake(
    mistake_id: str,
    current_user: dict = Depends(get_current_user),
    service: MistakeService = Depends(get_mistake_service),
):
    """
    获取错题详情

    - **mistake_id**: 错题 ID
    """
    mistake = await service.get_mistake(mistake_id)
    if mistake is None:
        raise HTTPException(status_code=404, detail="错题未找到")
    _verify_child_access(current_user, mistake.child_id)
    return mistake


@router.put("/mistakes/{mistake_id}", response_model=MistakeResponse)
async def update_mistake(
    mistake_id: str,
    data: MistakeUpdate,
    current_user: dict = Depends(get_current_user),
    service: MistakeService = Depends(get_mistake_service),
):
    """
    更新错题

    - **mistake_id**: 错题 ID
    - 仅更新提供的字段
    """
    mistake = await service.get_mistake(mistake_id)
    if mistake is None:
        raise HTTPException(status_code=404, detail="错题未找到")
    _verify_child_access(current_user, mistake.child_id)
    updated = await service.update_mistake(mistake_id, data)
    if updated is None:
        raise HTTPException(status_code=404, detail="错题未找到")
    return updated


@router.delete("/mistakes/{mistake_id}", status_code=204)
async def delete_mistake(
    mistake_id: str,
    current_user: dict = Depends(get_current_user),
    service: MistakeService = Depends(get_mistake_service),
):
    """
    删除错题

    - **mistake_id**: 错题 ID
    """
    mistake = await service.get_mistake(mistake_id)
    if mistake is None:
        raise HTTPException(status_code=404, detail="错题未找到")
    _verify_child_access(current_user, mistake.child_id)
    deleted = await service.delete_mistake(mistake_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="错题未找到")


@router.get("/mistakes/{mistake_id}/explanation")
async def get_explanation(
    mistake_id: str,
    current_user: dict = Depends(get_current_user),
    service: MistakeService = Depends(get_mistake_service),
):
    """
    获取错题的 AI 解析

    - **mistake_id**: 错题 ID
    - 返回 AI 解析、相似题目和知识点链接
    """
    mistake = await service.get_mistake(mistake_id)
    if mistake is None:
        raise HTTPException(status_code=404, detail="错题未找到")
    _verify_child_access(current_user, mistake.child_id)
    explanation = await service.get_explanation(mistake_id)
    if explanation is None:
        raise HTTPException(status_code=404, detail="错题未找到")
    return explanation
