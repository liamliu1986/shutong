"""题库 API 路由

提供题目的 CRUD 操作接口。
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_mongodb
from app.dependencies import get_current_user
from app.schemas.question_bank import (
    QuestionCreate,
    QuestionResponse,
    QuestionListResponse,
)
from app.services.question_bank_service import QuestionBankService

router = APIRouter()


def get_question_bank_service(
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
) -> QuestionBankService:
    """获取题库服务实例"""
    return QuestionBankService(db)


def _verify_child_access(current_user: dict, child_id: str):
    """验证 child_id 属于当前用户"""
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")


@router.post("/question-bank", response_model=QuestionResponse, status_code=200)
async def create_question(
    data: QuestionCreate,
    current_user: dict = Depends(get_current_user),
    service: QuestionBankService = Depends(get_question_bank_service),
):
    """
    创建题目

    - **child_id**: 孩子 ID
    - **subject**: 科目
    - **grade**: 年级
    - **question_type**: 题型（choice/fill_blank/solve）
    - **question_text**: 题目文本
    """
    _verify_child_access(current_user, data.child_id)
    return await service.create_question(data)


@router.get("/question-bank", response_model=QuestionListResponse)
async def get_questions(
    child_id: str = Query(..., description="孩子 ID"),
    subject: str = Query(None, description="科目筛选"),
    question_type: str = Query(None, description="题型筛选"),
    difficulty: int = Query(None, ge=1, le=5, description="难度筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: dict = Depends(get_current_user),
    service: QuestionBankService = Depends(get_question_bank_service),
):
    """
    获取题目列表

    支持按科目、题型和难度筛选，支持分页。
    """
    _verify_child_access(current_user, child_id)
    return await service.get_questions(
        child_id=child_id,
        subject=subject,
        question_type=question_type,
        difficulty=difficulty,
        page=page,
        page_size=page_size,
    )


@router.get("/question-bank/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    current_user: dict = Depends(get_current_user),
    service: QuestionBankService = Depends(get_question_bank_service),
):
    """
    获取题目详情

    - **question_id**: 题目 ID
    """
    question = await service.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="题目未找到")
    _verify_child_access(current_user, question.child_id)
    return question


@router.delete("/question-bank/{question_id}", status_code=204)
async def delete_question(
    question_id: str,
    current_user: dict = Depends(get_current_user),
    service: QuestionBankService = Depends(get_question_bank_service),
):
    """
    删除题目

    - **question_id**: 题目 ID
    """
    question = await service.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="题目未找到")
    _verify_child_access(current_user, question.child_id)
    deleted = await service.delete_question(question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="题目未找到")
