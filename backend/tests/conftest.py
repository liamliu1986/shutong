"""
测试配置和 fixtures
"""
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.config import get_settings
from app.database import connect_mongodb, close_mongodb, connect_neo4j, close_neo4j, get_mongodb, get_neo4j


@pytest.fixture(scope="session")
def event_loop():
    """创建 session 级别的事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """连接测试数据库"""
    settings = get_settings()
    # 使用测试数据库，替换路径中的数据库名
    from urllib.parse import urlparse, urlunparse
    uri = settings.MONGODB_URI
    parsed = urlparse(uri)
    # 替换 path 部分的数据库名
    new_path = "/shutong_test"
    settings.MONGODB_URI = urlunparse(parsed._replace(path=new_path))

    await connect_mongodb()
    await connect_neo4j()

    yield

    # 清理测试数据库
    mongodb = get_mongodb()
    collections = await mongodb.list_collection_names()
    for collection in collections:
        await mongodb[collection].drop()

    # 清理 Neo4j 数据
    neo4j_driver = get_neo4j()
    async with neo4j_driver.session() as session:
        await session.run("MATCH (n) DETACH DELETE n")

    await close_mongodb()
    await close_neo4j()


@pytest_asyncio.fixture(scope="session")
async def client(setup_database):
    """创建测试客户端"""
    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
async def test_user(client: AsyncClient):
    """创建测试用户并返回 TokenResponse"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123456"
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    return response.json()


@pytest_asyncio.fixture(scope="session")
async def auth_headers(test_user):
    """创建带认证头的请求头"""
    token = test_user["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="session")
async def test_child(client: AsyncClient, auth_headers):
    """创建测试孩子"""
    child_data = {
        "name": "测试孩子",
        "grade": 8,
        "subjects": ["数学"]
    }
    response = await client.post(
        "/api/v1/users/me/children",
        json=child_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    return response.json()
