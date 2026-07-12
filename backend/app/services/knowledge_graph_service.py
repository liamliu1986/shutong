"""
知识图谱服务模块
负责 Neo4j 知识图谱的初始化、查询和管理
"""
import logging
from typing import List

from app.database import get_neo4j

logger = logging.getLogger(__name__)


class KnowledgeGraphService:
    """知识图谱服务"""

    @staticmethod
    async def init_math_graph():
        """初始化数学知识图谱（全量清空重建）"""
        driver = get_neo4j()
        async with driver.session() as session:
            # 清空现有数据
            await session.run("MATCH (n) DETACH DELETE n")
            logger.info("已清空 Neo4j 现有数据")

            # 创建学科节点
            await session.run("""
                CREATE (s:Subject {
                    id: 'math',
                    name: '数学',
                    grade_level: '7-12'
                })
            """)
            logger.info("已创建学科节点：数学")

            # 创建章节节点
            chapters = [
                {"id": "ch1", "name": "二次函数", "order": 1},
                {"id": "ch2", "name": "一次函数", "order": 2},
                {"id": "ch3", "name": "方程与不等式", "order": 3},
                {"id": "ch4", "name": "几何图形", "order": 4},
            ]

            for ch in chapters:
                await session.run("""
                    MATCH (s:Subject {id: 'math'})
                    CREATE (c:Chapter {
                        id: $id,
                        name: $name,
                        order: $order
                    })
                    CREATE (s)-[:HAS_CHAPTER {order: $order}]->(c)
                """, **ch)
            logger.info(f"已创建 {len(chapters)} 个章节节点")

            # 创建知识点节点
            knowledge_points = [
                # 二次函数
                {"id": "kp1", "name": "二次函数的定义", "description": "形如y=ax²+bx+c(a≠0)的函数", "chapter": "ch1", "importance": 5},
                {"id": "kp2", "name": "二次函数的图像", "description": "抛物线的绘制与特征", "chapter": "ch1", "importance": 5},
                {"id": "kp3", "name": "二次函数的性质", "description": "开口方向、对称轴、顶点、单调性", "chapter": "ch1", "importance": 4},
                {"id": "kp4", "name": "二次函数的应用", "description": "最值问题、实际应用", "chapter": "ch1", "importance": 3},
                # 一次函数
                {"id": "kp5", "name": "一次函数的定义", "description": "形如y=kx+b(k≠0)的函数", "chapter": "ch2", "importance": 4},
                {"id": "kp6", "name": "一次函数的图像", "description": "直线的绘制与特征", "chapter": "ch2", "importance": 4},
                {"id": "kp7", "name": "一次函数的性质", "description": "斜率、截距、单调性", "chapter": "ch2", "importance": 4},
                # 方程与不等式
                {"id": "kp8", "name": "一元二次方程", "description": "ax²+bx+c=0的解法", "chapter": "ch3", "importance": 5},
                {"id": "kp9", "name": "不等式", "description": "一元一次不等式及其组", "chapter": "ch3", "importance": 4},
                # 几何图形
                {"id": "kp10", "name": "三角形", "description": "三角形的性质、全等、相似", "chapter": "ch4", "importance": 4},
                {"id": "kp11", "name": "四边形", "description": "平行四边形、矩形、菱形、正方形", "chapter": "ch4", "importance": 4},
                {"id": "kp12", "name": "圆", "description": "圆的性质、弧长、面积", "chapter": "ch4", "importance": 4},
            ]

            for kp in knowledge_points:
                await session.run("""
                    MATCH (c:Chapter {id: $chapter})
                    CREATE (kp:KnowledgePoint {
                        id: $id,
                        name: $name,
                        description: $description,
                        importance: $importance
                    })
                    CREATE (c)-[:HAS_KNOWLEDGE_POINT]->(kp)
                """, **kp)
            logger.info(f"已创建 {len(knowledge_points)} 个知识点节点")

            # 创建知识点关联关系（RELATED_TO）
            related_relations = [
                ("kp1", "kp2"),  # 二次函数定义 → 图像
                ("kp2", "kp3"),  # 图像 → 性质
                ("kp3", "kp4"),  # 性质 → 应用
                ("kp5", "kp6"),  # 一次函数定义 → 图像
                ("kp6", "kp7"),  # 图像 → 性质
            ]

            for from_id, to_id in related_relations:
                await session.run("""
                    MATCH (a:KnowledgePoint {id: $from_id})
                    MATCH (b:KnowledgePoint {id: $to_id})
                    CREATE (a)-[:RELATED_TO]->(b)
                """, from_id=from_id, to_id=to_id)

            # 创建前置关系（PREREQUISITE_OF）
            prerequisite_relations = [
                ("kp5", "kp1"),  # 一次函数 → 二次函数
                ("kp8", "kp1"),  # 一元二次方程 → 二次函数
                ("kp8", "kp3"),  # 一元二次方程 → 二次函数性质
            ]

            for from_id, to_id in prerequisite_relations:
                await session.run("""
                    MATCH (a:KnowledgePoint {id: $from_id})
                    MATCH (b:KnowledgePoint {id: $to_id})
                    CREATE (a)-[:PREREQUISITE_OF]->(b)
                """, from_id=from_id, to_id=to_id)

            logger.info("已创建知识点关联关系")
            logger.info("数学知识图谱初始化完成")

    @staticmethod
    async def get_subjects() -> List[dict]:
        """获取所有学科"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (s:Subject)
                RETURN s.id as id, s.name as name, s.grade_level as grade_level
            """)
            subjects = []
            async for record in result:
                subjects.append({
                    "id": record["id"],
                    "name": record["name"],
                    "grade_level": record["grade_level"]
                })
            return subjects

    @staticmethod
    async def get_subject_graph(subject_id: str) -> dict:
        """获取学科知识图谱"""
        driver = get_neo4j()
        async with driver.session() as session:
            # 获取章节
            chapters_result = await session.run("""
                MATCH (s:Subject {id: $subject_id})-[:HAS_CHAPTER]->(c:Chapter)
                RETURN c.id as id, c.name as name, c.order as order
                ORDER BY c.order
            """, subject_id=subject_id)

            chapters = []
            async for record in chapters_result:
                # 获取每个章节的知识点
                kps_result = await session.run("""
                    MATCH (c:Chapter {id: $chapter_id})-[:HAS_KNOWLEDGE_POINT]->(kp:KnowledgePoint)
                    RETURN kp.id as id, kp.name as name, kp.importance as importance, kp.description as description
                """, chapter_id=record["id"])

                kps = []
                async for kp_record in kps_result:
                    kps.append({
                        "id": kp_record["id"],
                        "name": kp_record["name"],
                        "importance": kp_record["importance"],
                        "description": kp_record.get("description")
                    })

                chapters.append({
                    "id": record["id"],
                    "name": record["name"],
                    "order": record["order"],
                    "knowledge_points": kps
                })

            # 获取指定学科下的知识点关联关系
            relations_result = await session.run("""
                MATCH (s:Subject {id: $subject_id})-[:HAS_CHAPTER]->(:Chapter)-[:HAS_KNOWLEDGE_POINT]->(a:KnowledgePoint)-[r]->(b:KnowledgePoint)
                WHERE type(r) IN ['RELATED_TO', 'PREREQUISITE_OF']
                RETURN a.id as from_id, b.id as to_id, type(r) as type
            """, subject_id=subject_id)

            relations = []
            async for record in relations_result:
                relations.append({
                    "from": record["from_id"],
                    "to": record["to_id"],
                    "type": record["type"]
                })

            return {
                "subject_id": subject_id,
                "chapters": chapters,
                "relations": relations
            }

    @staticmethod
    async def get_child_mastery(child_id: str, subject_id: str) -> List[dict]:
        """获取孩子对某学科知识点的掌握度

        MVP 阶段返回空数组，后续实现 Grades 关系
        """
        # TODO: 实现掌握度查询（需要 Child 节点和 Grades 关系）
        # 暂返回空数组
        return []
