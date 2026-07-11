"""
完整工作流集成测试
测试从用户注册到题库管理的完整业务流程
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_workflow(client: AsyncClient):
    """完整工作流测试"""

    # 1. 注册用户
    register_response = await client.post("/api/v1/auth/register", json={
        "username": "integration_user",
        "email": "integration@example.com",
        "password": "Test123456"
    })
    assert register_response.status_code == 200
    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. 添加孩子
    child_response = await client.post("/api/v1/users/me/children", json={
        "name": "小明",
        "grade": 9,
        "subjects": ["数学", "物理"]
    }, headers=headers)
    assert child_response.status_code == 200
    child_id = child_response.json()["id"]

    # 3. 创建错题
    mistake_response = await client.post("/api/v1/mistakes", json={
        "child_id": child_id,
        "subject": "数学",
        "grade": "九年级",
        "chapter": "二次函数",
        "question_text": "求函数 f(x)=x² 的最小值",
        "answer": "0",
        "explanation": "因为 x²≥0，所以最小值为0",
        "difficulty": 2
    }, headers=headers)
    assert mistake_response.status_code == 200

    # 4. 添加题目到题库
    question_response = await client.post("/api/v1/question-bank", json={
        "child_id": child_id,
        "subject": "数学",
        "grade": 9,
        "question_type": "solve",
        "question_text": "解方程 x²-5x+6=0",
        "answer": "x=2 或 x=3",
        "chapter": "方程与不等式",
        "difficulty": 3
    }, headers=headers)
    assert question_response.status_code == 200

    # 5. 获取错题列表
    mistakes_response = await client.get(
        f"/api/v1/mistakes?child_id={child_id}",
        headers=headers
    )
    assert mistakes_response.status_code == 200
    assert mistakes_response.json()["total"] > 0

    # 6. 获取题库列表
    questions_response = await client.get(
        f"/api/v1/question-bank?child_id={child_id}",
        headers=headers
    )
    assert questions_response.status_code == 200

    # 7. 获取学科列表
    subjects_response = await client.get(
        "/api/v1/subjects",
        headers=headers
    )
    assert subjects_response.status_code == 200

    print("✅ 完整工作流测试通过")
