"""试卷服务模块

提供试卷的 CRUD 操作和识别功能。
"""
import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.question_bank import PaperModel
from app.schemas.question_bank import (
    PaperCreate,
    PaperResponse,
    PaperListResponse,
)

logger = logging.getLogger(__name__)


class PaperService:
    """试卷服务类"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.papers

    async def create_paper(self, data: PaperCreate, images: list[dict] = None) -> PaperResponse:
        """
        创建试卷

        Args:
            data: 试卷创建数据
            images: 图片列表

        Returns:
            创建的试卷响应
        """
        now = datetime.now()
        paper_dict = data.model_dump()
        paper_dict["created_at"] = now
        paper_dict["images"] = images or []
        paper_dict["question_ids"] = []
        paper_dict["question_count"] = 0
        paper_dict["status"] = "uploaded"

        result = await self.collection.insert_one(paper_dict)
        paper_dict["id"] = str(result.inserted_id)
        if "_id" in paper_dict:
            del paper_dict["_id"]

        logger.info(f"创建试卷成功: {paper_dict['id']}")
        return PaperResponse(**paper_dict)

    async def get_papers(self, child_id: str) -> PaperListResponse:
        """
        获取试卷列表

        Args:
            child_id: 孩子 ID

        Returns:
            试卷列表响应
        """
        query = {"child_id": child_id}
        total = await self.collection.count_documents(query)

        cursor = (
            self.collection.find(query)
            .sort("created_at", -1)
        )

        items = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            items.append(PaperResponse(**doc))

        logger.info(f"查询试卷列表: child_id={child_id}, total={total}")
        return PaperListResponse(items=items, total=total)

    async def get_paper(self, paper_id: str) -> Optional[PaperResponse]:
        """
        获取单个试卷详情

        Args:
            paper_id: 试卷 ID

        Returns:
            试卷响应，未找到返回 None
        """
        try:
            doc = await self.collection.find_one({"_id": ObjectId(paper_id)})
        except Exception:
            logger.warning(f"无效的试卷 ID: {paper_id}")
            return None

        if doc is None:
            logger.info(f"试卷未找到: {paper_id}")
            return None

        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return PaperResponse(**doc)

    async def recognize_paper(self, paper_id: str) -> dict:
        """
        触发试卷识别

        Args:
            paper_id: 试卷 ID

        Returns:
            识别结果
        """
        paper = await self.get_paper(paper_id)
        if paper is None:
            return None

        # 更新状态为处理中
        await self.collection.update_one(
            {"_id": ObjectId(paper_id)},
            {"$set": {"status": "processing"}}
        )

        # MVP 阶段返回模拟识别结果
        # TODO: 后续接入 OCR API 进行真正的试卷识别
        logger.info(f"试卷识别开始: {paper_id}")

        # 模拟识别完成，更新状态
        await self.collection.update_one(
            {"_id": ObjectId(paper_id)},
            {"$set": {"status": "completed"}}
        )

        return {
            "paper_id": paper_id,
            "status": "completed",
            "message": "试卷识别完成（MVP 模拟）",
            "recognized_questions": [],
        }

    async def delete_paper(self, paper_id: str) -> bool:
        """
        删除试卷

        Args:
            paper_id: 试卷 ID

        Returns:
            是否删除成功
        """
        try:
            result = await self.collection.delete_one(
                {"_id": ObjectId(paper_id)}
            )
        except Exception:
            logger.warning(f"无效的试卷 ID: {paper_id}")
            return False

        if result.deleted_count == 0:
            logger.info(f"试卷未找到: {paper_id}")
            return False

        logger.info(f"删除试卷成功: {paper_id}")
        return True
