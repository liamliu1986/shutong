"""OCR 服务模块

MVP 阶段返回模拟数据，后续将接入真实 OCR API。
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class OCRService:
    """OCR 服务，负责从错题图片中识别文字和公式"""

    @staticmethod
    async def recognize_image(image_url: str) -> Dict[str, Any]:
        """
        识别图片中的题目内容

        Args:
            image_url: 图片 URL 地址

        Returns:
            包含识别结果的字典：
            - text: 识别出的文字
            - latex: 识别出的 LaTeX 公式
            - confidence: 置信度
            - detected_subject: 检测到的科目
            - detected_chapter: 检测到的章节
            - suggested_knowledge_points: 推荐的知识点列表
        """
        logger.info(f"OCR 识别图片: {image_url}")

        # MVP 阶段返回模拟数据
        # TODO: 后续接入真实 OCR API（如百度 OCR、阿里云 OCR）
        return {
            "text": "已知函数f(x)=x²+2x+1，求f(2)的值。",
            "latex": "f(x)=x^2+2x+1",
            "confidence": 0.95,
            "detected_subject": "数学",
            "detected_chapter": "二次函数",
            "suggested_knowledge_points": [
                {"id": "kp1", "name": "二次函数的定义", "confidence": 0.9}
            ]
        }

    @staticmethod
    async def recognize_batch(image_urls: List[str]) -> List[Dict[str, Any]]:
        """
        批量识别多张图片

        Args:
            image_urls: 图片 URL 列表

        Returns:
            识别结果列表
        """
        results = []
        for url in image_urls:
            result = await OCRService.recognize_image(url)
            results.append(result)
        return results
