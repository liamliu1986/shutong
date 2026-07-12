"""错题本服务模块

提供错题的 CRUD 操作和查询功能。
"""
import asyncio
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
from app.services.knowledge_graph_service import KnowledgeGraphService

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

        # 触发掌握度更新（不阻塞返回）
        asyncio.create_task(
            KnowledgeGraphService.update_child_mastery(
                data.child_id, data.subject
            )
        )

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
        # 获取原数据以触发掌握度更新
        original = await self.get_mistake(mistake_id)
        if original is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return original

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

        # 错题更新后触发掌握度重新计算
        asyncio.create_task(
            KnowledgeGraphService.update_child_mastery(
                original.child_id, original.subject
            )
        )

        return await self.get_mistake(mistake_id)

    async def delete_mistake(self, mistake_id: str) -> bool:
        """
        删除错题

        Args:
            mistake_id: 错题 ID

        Returns:
            是否删除成功
        """
        # 获取原数据以触发掌握度更新
        original = await self.get_mistake(mistake_id)
        if original is None:
            logger.info(f"错题未找到: {mistake_id}")
            return False

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

        # 删除后触发掌握度重新计算
        asyncio.create_task(
            KnowledgeGraphService.update_child_mastery(
                original.child_id, original.subject
            )
        )

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

        # 如果错题关联了知识点，从知识图谱获取详细信息
        knowledge_links = []
        related_kp_names = []

        if mistake.knowledge_points:
            try:
                for kp_id in mistake.knowledge_points:
                    kp_info = await KnowledgeGraphService.get_knowledge_point_detail(kp_id)
                    if kp_info:
                        knowledge_links.append({
                            "id": kp_id,
                            "name": kp_info["name"],
                            "description": kp_info.get("description", ""),
                        })
                        related_kp_names.append(kp_info["name"])
            except Exception:
                logger.warning(f"获取知识点信息失败: {mistake.knowledge_points}")

        # 没有知识图谱数据时使用通用解析
        if not knowledge_links:
            knowledge_links = [
                {
                    "id": "kl1",
                    "name": "已关联知识点",
                    "description": "错题将自动关联到知识点以追踪掌握度",
                }
            ]

        # 生成更具体的解析内容
        explanation = mistake.explanation or (
            f"这道题涉及{'、'.join(related_kp_names) if related_kp_names else '基础知识点'}。"
            f"建议先复习相关概念，再尝试做同类题目。"
        )

        similar_questions = []
        if related_kp_names:
            similar_questions.append({
                "id": "sq1",
                "question": f"请找一道考察{'、'.join(related_kp_names)}的练习题，"
                           f"检验是否真正掌握了该知识点。",
                "hint": f"重点关注{'、'.join(related_kp_names)}的应用场景。"
            })
        else:
            similar_questions.append({
                "id": "sq1",
                "question": "已知函数g(x)=x²-4x+3，求g(1)的值。",
                "hint": "将x=1代入函数表达式即可。"
            })

        return {
            "mistake_id": mistake_id,
            "explanation": explanation,
            "similar_questions": similar_questions,
            "knowledge_links": knowledge_links,
            "review_suggestion": (
                f"建议3天后复习此题"
                f"{'，重点关注' + '、'.join(related_kp_names) if related_kp_names else ''}。"
            ),
        }
