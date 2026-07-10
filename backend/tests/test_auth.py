import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """测试用户注册"""
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "Test123456"
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient):
    """测试重复注册"""
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "Test123456"
    }
    # 第一次注册
    await client.post("/api/v1/auth/register", json=user_data)

    # 第二次注册应失败
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    """测试用户登录"""
    # 先注册
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "Test123456"
    }
    await client.post("/api/v1/auth/register", json=user_data)

    # 登录
    login_data = {
        "email": "login@example.com",
        "password": "Test123456"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """测试错误密码登录"""
    # 先注册用户
    user_data = {
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "Test123456"
    }
    register_response = await client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200

    # 使用错误密码登录
    login_data = {
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile(client: AsyncClient, test_user):
    """测试获取用户信息"""
    token = test_user["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
