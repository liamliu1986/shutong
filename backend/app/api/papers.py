"""试卷 API 路由

提供试卷的 CRUD 操作和识别接口。
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.database import get_mongodb
from app.dependencies import get_current_user
from app.schemas.question_bank import (
    PaperCreate,
    PaperResponse,
    PaperListResponse,
)
from app.services.paper_service import PaperService

router = APIRouter()


def get_paper_service(
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
) -> PaperService:
    """获取试卷服务实例"""
    return PaperService(db)


def _verify_child_access(current_user: dict, child_id: str):
    """验证 child_id 属于当前用户"""
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")


@router.post("/papers", response_model=PaperResponse, status_code=201)
async def create_paper(
    data: PaperCreate,
    current_user: dict = Depends(get_current_user),
    service: PaperService = Depends(get_paper_service),
):
    """
    上传试卷

    - **child_id**: 孩子 ID
    - **name**: 试卷名称
    - **subject**: 科目
    - **grade**: 年级
    - **source**: 来源（可选）
    - **exam_date**: 考试日期（可选）
    - **total_score**: 总分（可选）
    """
    _verify_child_access(current_user, data.child_id)
    return await service.create_paper(data)


@router.get("/papers", response_model=PaperListResponse)
async def get_papers(
    child_id: str = Query(..., description="孩子 ID"),
    current_user: dict = Depends(get_current_user),
    service: PaperService = Depends(get_paper_service),
):
    """
    获取试卷列表

    - **child_id**: 孩子 ID
    """
    _verify_child_access(current_user, child_id)
    return await service.get_papers(child_id=child_id)


@router.get("/papers/{paper_id}", response_model=PaperResponse)
async def get_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user),
    service: PaperService = Depends(get_paper_service),
):
    """
    获取试卷详情

    - **paper_id**: 试卷 ID
    """
    paper = await service.get_paper(paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="试卷未找到")
    _verify_child_access(current_user, paper.child_id)
    return paper


@router.post("/papers/{paper_id}/recognize")
async def recognize_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user),
    service: PaperService = Depends(get_paper_service),
):
    """
    触发试卷识别

    - **paper_id**: 试卷 ID
    - 返回识别结果
    """
    paper = await service.get_paper(paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="试卷未找到")
    _verify_child_access(current_user, paper.child_id)
    result = await service.recognize_paper(paper_id)
    if result is None:
        raise HTTPException(status_code=404, detail="试卷未找到")
    return result


@router.delete("/papers/{paper_id}", status_code=204)
async def delete_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user),
    service: PaperService = Depends(get_paper_service),
):
    """
    删除试卷

    - **paper_id**: 试卷 ID
    """
    paper = await service.get_paper(paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="试卷未找到")
    _verify_child_access(current_user, paper.child_id)
    deleted = await service.delete_paper(paper_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="试卷未找到")
