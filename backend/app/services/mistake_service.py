"""错题本服务模块

提供错题的 CRUD 操作和查询功能。
"""
import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.mistake import MistakeModel
from app.schemas.mistake import (
    MistakeCreate,
    MistakeUpdate,
    MistakeResponse,
    MistakeListResponse,
)

logger = logging.getLogger(__name__)


class MistakeService:
    """错题本服务类"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.mistakes

    async def create_mistake(self, data: MistakeCreate) -> MistakeResponse:
        """
        创建错题记录

        Args:
            data: 错题创建数据

        Returns:
            创建的错题响应
        """
        now = datetime.now()
        mistake_dict = data.model_dump()
        mistake_dict["created_at"] = now
        mistake_dict["updated_at"] = now

        result = await self.collection.insert_one(mistake_dict)
        mistake_dict["id"] = str(result.inserted_id)
        if "_id" in mistake_dict:
            del mistake_dict["_id"]

        logger.info(f"创建错题成功: {mistake_dict['id']}")
        return MistakeResponse(**mistake_dict)

    async def get_mistakes(
        self,
        child_id: str,
        subject: Optional[str] = None,
        chapter: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> MistakeListResponse:
        """
        获取错题列表

        Args:
            child_id: 孩子 ID
            subject: 科目筛选（可选）
            chapter: 章节筛选（可选）
            page: 页码
            page_size: 每页数量

        Returns:
            错题列表响应
        """
        query = {"child_id": child_id}
        if subject:
            query["subject"] = subject
        if chapter:
            query["chapter"] = chapter

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
            items.append(MistakeResponse(**doc))

        logger.info(
            f"查询错题列表: child_id={child_id}, total={total}, page={page}"
        )
        return MistakeListResponse(
            items=items, total=total, page=page, page_size=page_size
        )

    async def get_mistake(self, mistake_id: str) -> Optional[MistakeResponse]:
        """
        获取单个错题详情

        Args:
            mistake_id: 错题 ID

        Returns:
            错题响应，未找到返回 None
        """
        try:
            doc = await self.collection.find_one({"_id": ObjectId(mistake_id)})
        except Exception:
            logger.warning(f"无效的错题 ID: {mistake_id}")
            return None

        if doc is None:
            logger.info(f"错题未找到: {mistake_id}")
            return None

        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return MistakeResponse(**doc)

    async def update_mistake(
        self, mistake_id: str, data: MistakeUpdate
    ) -> Optional[MistakeResponse]:
        """
        更新错题

        Args:
            mistake_id: 错题 ID
            data: 更新数据（仅更新非 None 字段）

        Returns:
            更新后的错题响应，未找到返回 None
        """
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_mistake(mistake_id)

        update_data["updated_at"] = datetime.now()

        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(mistake_id)}, {"$set": update_data}
            )
        except Exception:
            logger.warning(f"无效的错题 ID: {mistake_id}")
            return None

        if result.modified_count == 0:
            logger.info(f"错题未修改或未找到: {mistake_id}")
            return await self.get_mistake(mistake_id)

        logger.info(f"更新错题成功: {mistake_id}")
        return await self.get_mistake(mistake_id)

    async def delete_mistake(self, mistake_id: str) -> bool:
        """
        删除错题

        Args:
            mistake_id: 错题 ID

        Returns:
            是否删除成功
        """
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(mistake_id)}
            )
        except Exception:
            logger.warning(f"无效的错题 ID: {mistake_id}")
            return False

        if result.deleted_count == 0:
            logger.info(f"错题未找到: {mistake_id}")
            return False

        logger.info(f"删除错题成功: {mistake_id}")
        return True

    async def get_explanation(self, mistake_id: str) -> Optional[dict]:
        """
        获取错题的 AI 解析

        Args:
            mistake_id: 错题 ID

        Returns:
            AI 解析结果，未找到返回 None
        """
        mistake = await self.get_mistake(mistake_id)
        if mistake is None:
            return None

        # MVP 阶段返回模拟 AI 解析
        # TODO: 后续接入大模型 API 生成真正的解析
        return {
            "mistake_id": mistake_id,
            "explanation": mistake.explanation or "这道题考查的是基础知识点，建议先理解概念再做练习。",
            "similar_questions": [
                {
                    "id": "sq1",
                    "question": "已知函数g(x)=x²-4x+3，求g(1)的值。",
                    "hint": "将x=1代入函数表达式即可。"
                }
            ],
            "knowledge_links": [
                {
                    "id": "kl1",
                    "name": "二次函数的基本性质",
                    "url": "/knowledge/二次函数的基本性质"
                }
            ],
            "review_suggestion": "建议3天后复习此题，重点关注二次函数的代入求值。"
        }
