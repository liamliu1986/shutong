"""错题本 API 测试"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_mistake(client: AsyncClient, test_child, auth_headers):
    """测试创建错题"""
    mistake_data = {
        "child_id": test_child["id"],
        "subject": "数学",
        "grade": 8,
        "chapter": "二次函数",
        "question_text": "已知函数f(x)=x²+2x+1，求f(2)的值。",
        "answer": "f(2)=9",
        "explanation": "将x=2代入f(x)=x²+2x+1，得f(2)=4+4+1=9",
        "difficulty": 3,
        "source": "期中考试",
        "tags": ["二次函数", "代入求值"],
        "knowledge_points": ["kp1", "kp2"]
    }
    response = await client.post(
        "/api/v1/mistakes",
        json=mistake_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["child_id"] == test_child["id"]
    assert data["subject"] == "数学"
    assert data["grade"] == 8
    assert data["chapter"] == "二次函数"
    assert data["question_text"] == "已知函数f(x)=x²+2x+1，求f(2)的值。"
    assert data["difficulty"] == 3
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_mistakes(client: AsyncClient, test_child, auth_headers):
    """测试获取错题列表"""
    # 先创建几条错题
    for i in range(3):
        mistake_data = {
            "child_id": test_child["id"],
            "subject": "数学",
            "grade": 8,
            "chapter": f"第{i+1}章",
            "question_text": f"题目{i+1}",
            "difficulty": 2,
        }
        await client.post("/api/v1/mistakes", json=mistake_data, headers=auth_headers)

    # 查询列表
    response = await client.get(
        "/api/v1/mistakes",
        params={"child_id": test_child["id"]},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert data["total"] >= 3
    assert len(data["items"]) >= 3


@pytest.mark.asyncio
async def test_get_mistakes_with_filters(client: AsyncClient, test_child, auth_headers):
    """测试带筛选条件的错题列表"""
    # 创建不同科目的错题
    for subject in ["数学", "英语", "数学"]:
        mistake_data = {
            "child_id": test_child["id"],
            "subject": subject,
            "grade": 9,
            "chapter": "测试章节",
            "question_text": f"{subject}题目",
        }
        await client.post(
            "/api/v1/mistakes",
            json=mistake_data,
            headers=auth_headers
        )

    # 按科目筛选
    response = await client.get(
        "/api/v1/mistakes",
        params={"child_id": test_child["id"], "subject": "数学"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert all(item["subject"] == "数学" for item in data["items"])


@pytest.mark.asyncio
async def test_get_mistake(client: AsyncClient, test_child, auth_headers):
    """测试获取单个错题详情"""
    # 先创建错题
    mistake_data = {
        "child_id": test_child["id"],
        "subject": "物理",
        "grade": 10,
        "chapter": "力学",
        "question_text": "一个物体受到10N的力，质量为2kg，求加速度。",
        "answer": "a=5m/s²",
        "difficulty": 2,
    }
    create_response = await client.post(
        "/api/v1/mistakes",
        json=mistake_data,
        headers=auth_headers
    )
    mistake_id = create_response.json()["id"]

    # 获取详情
    response = await client.get(
        f"/api/v1/mistakes/{mistake_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mistake_id
    assert data["subject"] == "物理"
    assert data["question_text"] == "一个物体受到10N的力，质量为2kg，求加速度。"


@pytest.mark.asyncio
async def test_get_mistake_not_found(client: AsyncClient, auth_headers):
    """测试获取不存在的错题"""
    response = await client.get(
        "/api/v1/mistakes/000000000000000000000000",
        headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_mistake(client: AsyncClient, test_child, auth_headers):
    """测试更新错题"""
    # 先创建错题
    mistake_data = {
        "child_id": test_child["id"],
        "subject": "化学",
        "grade": 11,
        "chapter": "有机化学",
        "question_text": "原始题目",
        "difficulty": 3,
    }
    create_response = await client.post(
        "/api/v1/mistakes",
        json=mistake_data,
        headers=auth_headers
    )
    mistake_id = create_response.json()["id"]

    # 更新错题
    update_data = {
        "question_text": "更新后的题目",
        "difficulty": 4,
        "tags": ["有机化学", "烷烃"]
    }
    response = await client.put(
        f"/api/v1/mistakes/{mistake_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question_text"] == "更新后的题目"
    assert data["difficulty"] == 4
    assert data["tags"] == ["有机化学", "烷烃"]
    # 未更新的字段应保持不变
    assert data["subject"] == "化学"


@pytest.mark.asyncio
async def test_update_mistake_not_found(client: AsyncClient, auth_headers):
    """测试更新不存在的错题"""
    update_data = {"question_text": "更新内容"}
    response = await client.put(
        "/api/v1/mistakes/000000000000000000000000",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_mistake(client: AsyncClient, test_child, auth_headers):
    """测试删除错题"""
    # 先创建错题
    mistake_data = {
        "child_id": test_child["id"],
        "subject": "历史",
        "grade": 7,
        "chapter": "古代史",
        "question_text": "待删除的题目",
    }
    create_response = await client.post(
        "/api/v1/mistakes",
        json=mistake_data,
        headers=auth_headers
    )
    mistake_id = create_response.json()["id"]

    # 删除错题
    response = await client.delete(
        f"/api/v1/mistakes/{mistake_id}",
        headers=auth_headers
    )
    assert response.status_code == 204

    # 验证已删除
    response = await client.get(
        f"/api/v1/mistakes/{mistake_id}",
        headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_mistake_not_found(client: AsyncClient, auth_headers):
    """测试删除不存在的错题"""
    response = await client.delete(
        "/api/v1/mistakes/000000000000000000000000",
        headers=auth_headers
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_explanation(client: AsyncClient, test_child, auth_headers):
    """测试获取 AI 解析"""
    # 先创建错题
    mistake_data = {
        "child_id": test_child["id"],
        "subject": "数学",
        "grade": 8,
        "chapter": "二次函数",
        "question_text": "求f(x)=x²的最小值",
        "explanation": "二次函数开口向上，顶点为最小值点",
    }
    create_response = await client.post(
        "/api/v1/mistakes",
        json=mistake_data,
        headers=auth_headers
    )
    mistake_id = create_response.json()["id"]

    # 获取 AI 解析
    response = await client.get(
        f"/api/v1/mistakes/{mistake_id}/explanation",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "mistake_id" in data
    assert "explanation" in data
    assert "similar_questions" in data
    assert "knowledge_links" in data
    assert "review_suggestion" in data
    assert data["mistake_id"] == mistake_id


@pytest.mark.asyncio
async def test_get_explanation_not_found(client: AsyncClient, auth_headers):
    """测试获取不存在错题的 AI 解析"""
    response = await client.get(
        "/api/v1/mistakes/000000000000000000000000/explanation",
        headers=auth_headers
    )
    assert response.status_code == 404
