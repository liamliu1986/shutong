"""
知识图谱服务模块
负责 Neo4j 知识图谱的初始化、查询和管理
"""
import logging
import math
from datetime import datetime
from typing import Dict, List, Optional

from app.database import get_neo4j, get_mongodb

logger = logging.getLogger(__name__)


class KnowledgeGraphService:
    """知识图谱服务"""

    @staticmethod
    async def _get_subject_id_by_name(subject_name: str) -> Optional[str]:
        """根据学科名称查找 Neo4j 中的 subject_id"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run(
                "MATCH (s:Subject {name: $name}) RETURN s.id as id",
                name=subject_name,
            )
            record = await result.single()
            return record["id"] if record else None

    @staticmethod
    async def get_knowledge_point_detail(kp_id: str) -> Optional[dict]:
        """获取知识点详情"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (kp:KnowledgePoint {id: $kp_id})
                OPTIONAL MATCH (kp)<-[:HAS_KNOWLEDGE_POINT]-(c:Chapter)
                RETURN kp.id as id, kp.name as name,
                       kp.description as description,
                       kp.importance as importance,
                       c.name as chapter_name, c.id as chapter_id
            """, kp_id=kp_id)
            record = await result.single()
            if not record:
                return None
            return {
                "id": record["id"],
                "name": record["name"],
                "description": record.get("description"),
                "importance": record.get("importance"),
                "chapter_name": record.get("chapter_name"),
                "chapter_id": record.get("chapter_id"),
            }

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

        从 MongoDB mastery 集合中查询
        """
        db = get_mongodb()
        cursor = db.mastery.find({
            "child_id": child_id,
            "subject_id": subject_id,
        })
        results = []
        async for doc in cursor:
            results.append({
                "kp_id": doc["kp_id"],
                "mastery_score": doc["mastery_score"],
                "total_attempts": doc["total_attempts"],
                "last_updated": doc.get("last_updated"),
            })
        return results

    @staticmethod
    async def update_child_mastery(child_id: str, subject_name: str):
        """根据错题数据更新孩子对指定学科的掌握度

        从 MongoDB 查询错题，按知识点聚合后计算掌握度
        """
        subject_id = await KnowledgeGraphService._get_subject_id_by_name(subject_name)
        if not subject_id:
            logger.warning(f"未找到学科: {subject_name}")
            return

        db = get_mongodb()

        # 获取该孩子的所有错题
        cursor = db.mistakes.find({
            "child_id": child_id,
            "subject": subject_name,
        })

        # 按知识点聚合错题数
        kp_attempts: Dict[str, int] = {}
        async for mistake in cursor:
            for kp_id in mistake.get("knowledge_points", []):
                kp_attempts[kp_id] = kp_attempts.get(kp_id, 0) + 1

        now = datetime.now()

        # 计算掌握度并写入 MongoDB mastery 集合
        for kp_id, count in kp_attempts.items():
            mastery = round(100 * (1 - math.tanh(0.15 * count)), 1)
            await db.mastery.update_one(
                {"child_id": child_id, "subject_id": subject_id, "kp_id": kp_id},
                {"$set": {
                    "mastery_score": mastery,
                    "total_attempts": count,
                    "correct_attempts": 0,
                    "last_updated": now,
                }},
                upsert=True,
            )

        logger.info(
            f"掌握度更新完成: child_id={child_id}, "
            f"subject_id={subject_id}, kps={len(kp_attempts)}"
        )

    # ═══════════════════════════════════════════════════════════════
    # Phase 3: CRUD 方法
    # ═══════════════════════════════════════════════════════════════

    # ─── 学科 CRUD ───────────────────────────────────────────────

    @staticmethod
    async def create_subject(
        id: str, name: str, grade_level: Optional[str] = None
    ) -> dict:
        """创建学科"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                CREATE (s:Subject {id: $id, name: $name})
                SET s.grade_level = $grade_level
                RETURN s.id as id, s.name as name, s.grade_level as grade_level
            """, id=id, name=name, grade_level=grade_level or "")
            record = await result.single()
            if not record:
                raise ValueError(f"创建学科失败: {id}")
            logger.info(f"创建学科成功: {id}")
            return {
                "id": record["id"],
                "name": record["name"],
                "grade_level": record["grade_level"],
            }

    @staticmethod
    async def update_subject(id: str, name: Optional[str] = None,
                              grade_level: Optional[str] = None) -> bool:
        """更新学科"""
        driver = get_neo4j()
        async with driver.session() as session:
            sets = []
            params: dict = {"id": id}
            if name is not None:
                sets.append("s.name = $name")
                params["name"] = name
            if grade_level is not None:
                sets.append("s.grade_level = $grade_level")
                params["grade_level"] = grade_level
            if not sets:
                return True
            result = await session.run(
                f"MATCH (s:Subject {{id: $id}}) SET {', '.join(sets)} RETURN s",
                **params
            )
            record = await result.single()
            if not record:
                logger.warning(f"更新学科失败, 未找到: {id}")
                return False
            logger.info(f"更新学科成功: {id}")
            return True

    @staticmethod
    async def delete_subject(id: str) -> bool:
        """删除学科及其所有相关节点"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (s:Subject {id: $id})
                OPTIONAL MATCH (s)-[:HAS_CHAPTER]->(c:Chapter)
                OPTIONAL MATCH (c)-[:HAS_KNOWLEDGE_POINT]->(kp:KnowledgePoint)
                DETACH DELETE kp, c, s
                RETURN count(s) as deleted
            """, id=id)
            record = await result.single()
            deleted = record["deleted"] if record else 0
            logger.info(f"删除学科{'成功' if deleted else '失败, 未找到'}: {id}")
            return bool(deleted)

    # ─── 章节 CRUD ───────────────────────────────────────────────

    @staticmethod
    async def create_chapter(
        subject_id: str, id: str, name: str, order: int
    ) -> dict:
        """创建章节"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (s:Subject {id: $subject_id})
                CREATE (c:Chapter {id: $id, name: $name, order: $order})
                CREATE (s)-[:HAS_CHAPTER {order: $order}]->(c)
                RETURN c.id as id, c.name as name, c.order as order
            """, subject_id=subject_id, id=id, name=name, order=order)
            record = await result.single()
            if not record:
                raise ValueError(f"创建章节失败, 学科不存在: {subject_id}")
            logger.info(f"创建章节成功: {id}")
            return {
                "id": record["id"],
                "name": record["name"],
                "order": record["order"],
            }

    @staticmethod
    async def update_chapter(
        id: str, name: Optional[str] = None, order: Optional[int] = None
    ) -> bool:
        """更新章节"""
        driver = get_neo4j()
        async with driver.session() as session:
            sets = []
            params: dict = {"id": id}
            if name is not None:
                sets.append("c.name = $name")
                params["name"] = name
            if order is not None:
                sets.append("c.order = $order")
                params["order"] = order
            if not sets:
                return True
            result = await session.run(
                f"MATCH (c:Chapter {{id: $id}}) SET {', '.join(sets)} RETURN c",
                **params
            )
            record = await result.single()
            logger.info(f"更新章节{'成功' if record else '失败, 未找到'}: {id}")
            return bool(record)

    @staticmethod
    async def delete_chapter(id: str) -> bool:
        """删除章节及其知识点"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (c:Chapter {id: $id})
                OPTIONAL MATCH (c)-[:HAS_KNOWLEDGE_POINT]->(kp:KnowledgePoint)
                DETACH DELETE kp, c
                RETURN count(c) as deleted
            """, id=id)
            record = await result.single()
            deleted = record["deleted"] if record else 0
            logger.info(f"删除章节{'成功' if deleted else '失败, 未找到'}: {id}")
            return bool(deleted)

    # ─── 知识点 CRUD ─────────────────────────────────────────────

    @staticmethod
    async def create_knowledge_point(
        chapter_id: str, id: str, name: str,
        description: Optional[str] = None, importance: int = 3
    ) -> dict:
        """创建知识点"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (c:Chapter {id: $chapter_id})
                CREATE (kp:KnowledgePoint {
                    id: $id, name: $name,
                    description: $description, importance: $importance
                })
                CREATE (c)-[:HAS_KNOWLEDGE_POINT]->(kp)
                RETURN kp.id as id, kp.name as name,
                       kp.importance as importance, kp.description as description
            """, chapter_id=chapter_id, id=id, name=name,
                 description=description or "", importance=importance)
            record = await result.single()
            if not record:
                raise ValueError(f"创建知识点失败, 章节不存在: {chapter_id}")
            logger.info(f"创建知识点成功: {id}")
            return {
                "id": record["id"],
                "name": record["name"],
                "importance": record["importance"],
                "description": record["description"],
            }

    @staticmethod
    async def update_knowledge_point(
        id: str, name: Optional[str] = None,
        description: Optional[str] = None, importance: Optional[int] = None
    ) -> bool:
        """更新知识点"""
        driver = get_neo4j()
        async with driver.session() as session:
            sets = []
            params: dict = {"id": id}
            if name is not None:
                sets.append("kp.name = $name")
                params["name"] = name
            if description is not None:
                sets.append("kp.description = $description")
                params["description"] = description
            if importance is not None:
                sets.append("kp.importance = $importance")
                params["importance"] = importance
            if not sets:
                return True
            result = await session.run(
                f"MATCH (kp:KnowledgePoint {{id: $id}}) SET {', '.join(sets)} RETURN kp",
                **params
            )
            record = await result.single()
            logger.info(f"更新知识点{'成功' if record else '失败, 未找到'}: {id}")
            return bool(record)

    @staticmethod
    async def delete_knowledge_point(id: str) -> bool:
        """删除知识点"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (kp:KnowledgePoint {id: $id})
                DETACH DELETE kp
                RETURN count(kp) as deleted
            """, id=id)
            record = await result.single()
            deleted = record["deleted"] if record else 0
            logger.info(f"删除知识点{'成功' if deleted else '失败, 未找到'}: {id}")
            return bool(deleted)

    # ─── 关系 CRUD ───────────────────────────────────────────────

    @staticmethod
    async def create_relation(from_id: str, to_id: str, type: str) -> bool:
        """创建知识点间关系"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (a:KnowledgePoint {id: $from_id})
                MATCH (b:KnowledgePoint {id: $to_id})
                CREATE (a)-[r:{rel_type}]->(b)
                RETURN count(r) as created
            """.replace("{rel_type}", type), from_id=from_id, to_id=to_id)
            record = await result.single()
            created = record["created"] if record else 0
            logger.info(f"创建关系{'成功' if created else '失败, 知识点不存在'}: {from_id} -> {to_id}")
            return bool(created)

    @staticmethod
    async def delete_relation(from_id: str, to_id: str, type: str) -> bool:
        """删除知识点间关系"""
        driver = get_neo4j()
        async with driver.session() as session:
            result = await session.run("""
                MATCH (a:KnowledgePoint {id: $from_id})
                -[r:{rel_type}]->
                (b:KnowledgePoint {id: $to_id})
                DELETE r
                RETURN count(r) as deleted
            """.replace("{rel_type}", type), from_id=from_id, to_id=to_id)
            record = await result.single()
            deleted = record["deleted"] if record else 0
            logger.info(f"删除关系{'成功' if deleted else '失败, 未找到'}: {from_id} -> {to_id}")
            return bool(deleted)
