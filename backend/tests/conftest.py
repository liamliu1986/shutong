"""
测试配置和 fixtures
"""
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.config import get_settings
from app.database import connect_mongodb, close_mongodb, connect_neo4j, close_neo4j, get_mongodb


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """连接测试数据库"""
    settings = get_settings()
    # 使用测试数据库
    test_db_name = "shutong_test"
    settings.MONGODB_URI = f"mongodb://localhost:27017/{test_db_name}"

    await connect_mongodb()
    await connect_neo4j()

    yield

    # 清理测试数据库
    mongodb = get_mongodb()
    collections = await mongodb.list_collection_names()
    for collection in collections:
        await mongodb[collection].drop()

    await close_mongodb()
    await close_neo4j()


@pytest_asyncio.fixture
async def client(setup_database):
    """创建测试客户端"""
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user(setup_database):
    """创建测试用户"""
    from passlib.context import CryptContext
    from datetime import datetime

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    mongodb = get_mongodb()

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": pwd_context.hash("testpassword123"),
        "children": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # 插入测试用户
    result = await mongodb.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id

    yield user_data

    # 清理测试用户
    await mongodb.users.delete_one({"_id": result.inserted_id})
