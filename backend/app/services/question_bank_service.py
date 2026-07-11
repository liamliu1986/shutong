"""题库服务模块

提供题目的 CRUD 操作和批量导入功能。
"""
import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.question_bank import QuestionModel
from app.schemas.question_bank import (
    QuestionCreate,
    QuestionResponse,
    QuestionListResponse,
)

logger = logging.getLogger(__name__)


class QuestionBankService:
    """题库服务类"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.questions

    async def create_question(self, data: QuestionCreate) -> QuestionResponse:
        """
        创建题目

        Args:
            data: 题目创建数据

        Returns:
            创建的题目响应
        """
        now = datetime.now()
        question_dict = data.model_dump()
        question_dict["created_at"] = now
        question_dict["updated_at"] = now
        question_dict["used_count"] = 0
        question_dict["correct_rate"] = 0.0

        result = await self.collection.insert_one(question_dict)
        question_dict["id"] = str(result.inserted_id)
        if "_id" in question_dict:
            del question_dict["_id"]

        logger.info(f"创建题目成功: {question_dict['id']}")
        return QuestionResponse(**question_dict)

    async def get_questions(
        self,
        child_id: str,
        subject: Optional[str] = None,
        question_type: Optional[str] = None,
        difficulty: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> QuestionListResponse:
        """
        获取题目列表

        Args:
            child_id: 孩子 ID
            subject: 科目筛选（可选）
            question_type: 题型筛选（可选）
            difficulty: 难度筛选（可选）
            page: 页码
            page_size: 每页数量

        Returns:
            题目列表响应
        """
        query = {"child_id": child_id}
        if subject:
            query["subject"] = subject
        if question_type:
            query["question_type"] = question_type
        if difficulty:
            query["difficulty"] = difficulty

        total = await self.collection.count_documents(query)
        skip = (page - 1) * page_size

        cursor = (
            self.collection.find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(page_size)
        )

        items = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            items.append(QuestionResponse(**doc))

        logger.info(
            f"查询题目列表: child_id={child_id}, total={total}, page={page}"
        )
        return QuestionListResponse(
            items=items, total=total, page=page, page_size=page_size
        )

    async def get_question(self, question_id: str) -> Optional[QuestionResponse]:
        """
        获取单个题目详情

        Args:
            question_id: 题目 ID

        Returns:
            题目响应，未找到返回 None
        """
        try:
            doc = await self.collection.find_one({"_id": ObjectId(question_id)})
        except Exception:
            logger.warning(f"无效的题目 ID: {question_id}")
            return None

        if doc is None:
            logger.info(f"题目未找到: {question_id}")
            return None

        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return QuestionResponse(**doc)

    async def delete_question(self, question_id: str) -> bool:
        """
        删除题目

        Args:
            question_id: 题目 ID

        Returns:
            是否删除成功
        """
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(question_id)}
            )
        except Exception:
            logger.warning(f"无效的题目 ID: {question_id}")
            return False

        if result.deleted_count == 0:
            logger.info(f"题目未找到: {question_id}")
            return False

        logger.info(f"删除题目成功: {question_id}")
        return True

    async def batch_import(self, paper_id: str, questions: list[QuestionCreate]) -> dict:
        """
        批量导入题目

        Args:
            paper_id: 试卷 ID
            questions: 题目列表

        Returns:
            导入结果统计
        """
        now = datetime.now()
        success_count = 0
        failed_count = 0
        question_ids = []

        for question_data in questions:
            try:
                question_dict = question_data.model_dump()
                question_dict["created_at"] = now
                question_dict["updated_at"] = now
                question_dict["used_count"] = 0
                question_dict["correct_rate"] = 0.0
                question_dict["source_type"] = "paper"
                question_dict["source_paper_id"] = paper_id

                result = await self.collection.insert_one(question_dict)
                question_ids.append(str(result.inserted_id))
                success_count += 1
            except Exception as e:
                logger.error(f"导入题目失败: {e}")
                failed_count += 1

        logger.info(
            f"批量导入完成: paper_id={paper_id}, "
            f"成功={success_count}, 失败={failed_count}"
        )

        return {
            "success_count": success_count,
            "failed_count": failed_count,
            "question_ids": question_ids,
        }
