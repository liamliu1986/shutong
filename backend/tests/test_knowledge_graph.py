"""
知识图谱模块测试
使用真实 Neo4j 实例进行集成测试
"""
import pytest
from httpx import AsyncClient

from app.services.knowledge_graph_service import KnowledgeGraphService


class TestKnowledgeGraphService:
    """知识图谱服务测试"""

    @pytest.mark.asyncio
    async def test_init_math_graph(self, setup_database):
        """测试初始化数学知识图谱"""
        # 调用初始化
        await KnowledgeGraphService.init_math_graph()

        # 验证学科节点已创建
        subjects = await KnowledgeGraphService.get_subjects()
        assert len(subjects) == 1
        assert subjects[0]["id"] == "math"
        assert subjects[0]["name"] == "数学"

    @pytest.mark.asyncio
    async def test_get_subjects(self, setup_database):
        """测试获取学科列表"""
        # 先初始化数据
        await KnowledgeGraphService.init_math_graph()

        subjects = await KnowledgeGraphService.get_subjects()
        assert isinstance(subjects, list)
        assert len(subjects) >= 1

        # 验证数据结构
        subject = subjects[0]
        assert "id" in subject
        assert "name" in subject
        assert "grade_level" in subject

    @pytest.mark.asyncio
    async def test_get_subject_graph(self, setup_database):
        """测试获取学科知识图谱"""
        # 先初始化数据
        await KnowledgeGraphService.init_math_graph()

        graph = await KnowledgeGraphService.get_subject_graph("math")

        # 验证图结构
        assert "subject_id" in graph
        assert graph["subject_id"] == "math"
        assert "chapters" in graph
        assert "relations" in graph

        # 验证章节数据
        chapters = graph["chapters"]
        assert isinstance(chapters, list)
        assert len(chapters) == 4  # 二次函数、一次函数、方程与不等式、几何图形

        # 验证每个章节有知识点
        for chapter in chapters:
            assert "id" in chapter
            assert "name" in chapter
            assert "order" in chapter
            assert "knowledge_points" in chapter
            assert isinstance(chapter["knowledge_points"], list)
            assert len(chapter["knowledge_points"]) > 0

        # 验证关系数据
        relations = graph["relations"]
        assert isinstance(relations, list)
        assert len(relations) > 0

        for relation in relations:
            assert "from" in relation
            assert "to" in relation

    @pytest.mark.asyncio
    async def test_get_subject_graph_not_found(self, setup_database):
        """测试获取不存在学科的图谱"""
        graph = await KnowledgeGraphService.get_subject_graph("nonexistent")
        assert graph["chapters"] == []
        assert graph["relations"] == []

    @pytest.mark.asyncio
    async def test_get_child_mastery_empty(self, setup_database):
        """测试获取孩子掌握度（无数据）"""
        # 先初始化数据
        await KnowledgeGraphService.init_math_graph()

        mastery = await KnowledgeGraphService.get_child_mastery("test_child", "math")
        assert isinstance(mastery, list)
        assert len(mastery) == 0  # MVP 阶段返回空数组


class TestKnowledgeGraphAPI:
    """知识图谱 API 测试"""

    @pytest.mark.asyncio
    async def test_get_subjects_unauthorized(self, client: AsyncClient):
        """测试未认证获取学科列表"""
        response = await client.get("/api/v1/subjects")
        assert response.status_code == 403  # 未提供 token

    @pytest.mark.asyncio
    async def test_get_subjects_authorized(self, client: AsyncClient, test_user):
        """测试认证后获取学科列表"""
        token = test_user["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 先初始化知识图谱
        await KnowledgeGraphService.init_math_graph()

        response = await client.get("/api/v1/subjects", headers=headers)
        assert response.status_code == 200
        subjects = response.json()
        assert isinstance(subjects, list)
        assert len(subjects) >= 1

    @pytest.mark.asyncio
    async def test_get_subject_graph_authorized(self, client: AsyncClient, test_user):
        """测试认证后获取学科图谱"""
        token = test_user["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 先初始化知识图谱
        await KnowledgeGraphService.init_math_graph()

        response = await client.get("/api/v1/subjects/math/graph", headers=headers)
        assert response.status_code == 200
        graph = response.json()
        assert "chapters" in graph
        assert "relations" in graph
        assert len(graph["chapters"]) == 4

    @pytest.mark.asyncio
    async def test_get_child_mastery_authorized(self, client: AsyncClient, test_user):
        """测试认证后获取孩子掌握度"""
        token = test_user["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 先初始化知识图谱
        await KnowledgeGraphService.init_math_graph()

        # 先添加一个孩子
        child_data = {"name": "小明", "grade": 9, "subjects": ["数学"]}
        child_response = await client.post(
            "/api/v1/users/me/children",
            json=child_data,
            headers=headers
        )

        if child_response.status_code == 200:
            child_id = child_response.json()["id"]
            response = await client.get(
                f"/api/v1/children/{child_id}/mastery?subject_id=math",
                headers=headers
            )
            assert response.status_code == 200
            mastery = response.json()
            assert isinstance(mastery, list)
