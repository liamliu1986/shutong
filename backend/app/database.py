"""
数据库连接管理模块
管理 MongoDB 和 Neo4j 的连接生命周期
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession

from app.config import get_settings

logger = logging.getLogger(__name__)

# MongoDB 全局变量
mongodb_client: AsyncIOMotorClient = None
mongodb: AsyncIOMotorDatabase = None

# Neo4j 全局变量
neo4j_driver: AsyncDriver = None


async def connect_mongodb():
    """连接 MongoDB 并创建索引"""
    global mongodb_client, mongodb

    settings = get_settings()
    logger.info(f"正在连接 MongoDB: {settings.MONGODB_URI}")

    mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)
    mongodb = mongodb_client.shutong

    # 创建索引
    await mongodb.users.create_index("email", unique=True)
    await mongodb.users.create_index("username", unique=True)
    await mongodb.documents.create_index("user_id")
    await mongodb.quizzes.create_index("user_id")
    await mongodb.quizzes.create_index("document_id")

    logger.info("MongoDB 连接成功，索引已创建")


async def close_mongodb():
    """关闭 MongoDB 连接"""
    global mongodb_client, mongodb

    if mongodb_client:
        mongodb_client.close()
        mongodb_client = None
        mongodb = None
        logger.info("MongoDB 连接已关闭")


async def connect_neo4j():
    """连接 Neo4j"""
    global neo4j_driver

    settings = get_settings()
    logger.info(f"正在连接 Neo4j: {settings.NEO4J_URI}")

    neo4j_driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )

    # 验证连接
    await neo4j_driver.verify_connectivity()
    logger.info("Neo4j 连接成功")


async def close_neo4j():
    """关闭 Neo4j 连接"""
    global neo4j_driver

    if neo4j_driver:
        await neo4j_driver.close()
        neo4j_driver = None
        logger.info("Neo4j 连接已关闭")


def get_mongodb() -> AsyncIOMotorDatabase:
    """获取 MongoDB 数据库实例"""
    if mongodb is None:
        raise RuntimeError("MongoDB 未连接，请先调用 connect_mongodb()")
    return mongodb


def get_neo4j() -> AsyncDriver:
    """获取 Neo4j 驱动实例"""
    if neo4j_driver is None:
        raise RuntimeError("Neo4j 未连接，请先调用 connect_neo4j()")
    return neo4j_driver
