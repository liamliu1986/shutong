"""
数学知识图谱初始化脚本

使用方法：
    cd backend
    python -m scripts.init_math_graph

注意：此脚本会清空 Neo4j 中的所有现有数据并重建数学知识图谱
"""
import asyncio
import logging
import sys

# 添加项目根目录到路径
sys.path.insert(0, ".")

from app.database import connect_neo4j, close_neo4j
from app.services.knowledge_graph_service import KnowledgeGraphService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """初始化数学知识图谱"""
    logger.info("开始初始化数学知识图谱...")

    try:
        # 连接 Neo4j
        await connect_neo4j()
        logger.info("Neo4j 连接成功")

        # 初始化知识图谱
        await KnowledgeGraphService.init_math_graph()
        logger.info("数学知识图谱初始化完成")

        # 验证初始化结果
        subjects = await KnowledgeGraphService.get_subjects()
        logger.info(f"已创建 {len(subjects)} 个学科")

        if subjects:
            graph = await KnowledgeGraphService.get_subject_graph(subjects[0]["id"])
            logger.info(f"学科 '{subjects[0]['name']}' 包含 {len(graph['chapters'])} 个章节")
            total_kps = sum(len(ch["knowledge_points"]) for ch in graph["chapters"])
            logger.info(f"共 {total_kps} 个知识点，{len(graph['relations'])} 条关系")

    except Exception as e:
        logger.error(f"初始化失败: {e}")
        raise
    finally:
        # 关闭连接
        await close_neo4j()
        logger.info("Neo4j 连接已关闭")

    logger.info("初始化脚本执行完毕")


if __name__ == "__main__":
    asyncio.run(main())
