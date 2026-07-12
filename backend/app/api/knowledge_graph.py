"""
知识图谱 API 路由
提供学科、知识点、掌握度等接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.services.knowledge_graph_service import KnowledgeGraphService
from app.schemas.knowledge_graph import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    ChapterCreate,
    ChapterUpdate,
    KnowledgePointCreate,
    KnowledgePointUpdate,
    KnowledgePointPosition,
    RelationCreate,
    SubjectGraphResponse,
    MasteryEntry,
)

router = APIRouter()


# ─── 学科端点 ──────────────────────────────────────────────────────


@router.get("/subjects", response_model=List[SubjectResponse])
async def get_subjects(current_user: dict = Depends(get_current_user)):
    """获取所有学科列表"""
    return await KnowledgeGraphService.get_subjects()


@router.post("/subjects", response_model=SubjectResponse, status_code=201)
async def create_subject(
    data: SubjectCreate,
    current_user: dict = Depends(get_current_user),
):
    """创建学科"""
    try:
        return await KnowledgeGraphService.create_subject(
            id=data.id, name=data.name, grade_level=data.grade_level
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/subjects/{subject_id}")
async def update_subject(
    subject_id: str,
    data: SubjectUpdate,
    current_user: dict = Depends(get_current_user),
):
    """更新学科"""
    success = await KnowledgeGraphService.update_subject(
        id=subject_id, name=data.name, grade_level=data.grade_level
    )
    if not success:
        raise HTTPException(status_code=404, detail="学科未找到")
    return {"message": "更新成功"}


@router.delete("/subjects/{subject_id}")
async def delete_subject(
    subject_id: str,
    current_user: dict = Depends(get_current_user),
):
    """删除学科"""
    success = await KnowledgeGraphService.delete_subject(id=subject_id)
    if not success:
        raise HTTPException(status_code=404, detail="学科未找到")
    return {"message": "删除成功"}


# ─── 章节端点 ──────────────────────────────────────────────────────


@router.get("/subjects/{subject_id}/graph", response_model=SubjectGraphResponse)
async def get_subject_graph(
    subject_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取学科知识图谱"""
    return await KnowledgeGraphService.get_subject_graph(subject_id)


@router.post("/subjects/{subject_id}/chapters", status_code=201)
async def create_chapter(
    subject_id: str,
    data: ChapterCreate,
    current_user: dict = Depends(get_current_user),
):
    """创建章节"""
    try:
        return await KnowledgeGraphService.create_chapter(
            subject_id=subject_id, id=data.id,
            name=data.name, order=data.order
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/chapters/{chapter_id}")
async def update_chapter(
    chapter_id: str,
    data: ChapterUpdate,
    current_user: dict = Depends(get_current_user),
):
    """更新章节"""
    success = await KnowledgeGraphService.update_chapter(
        id=chapter_id, name=data.name, order=data.order
    )
    if not success:
        raise HTTPException(status_code=404, detail="章节未找到")
    return {"message": "更新成功"}


@router.delete("/chapters/{chapter_id}")
async def delete_chapter(
    chapter_id: str,
    current_user: dict = Depends(get_current_user),
):
    """删除章节"""
    success = await KnowledgeGraphService.delete_chapter(id=chapter_id)
    if not success:
        raise HTTPException(status_code=404, detail="章节未找到")
    return {"message": "删除成功"}


# ─── 知识点端点 ────────────────────────────────────────────────────


@router.post("/chapters/{chapter_id}/knowledge-points", status_code=201)
async def create_knowledge_point(
    chapter_id: str,
    data: KnowledgePointCreate,
    current_user: dict = Depends(get_current_user),
):
    """创建知识点"""
    try:
        return await KnowledgeGraphService.create_knowledge_point(
            chapter_id=chapter_id, id=data.id,
            name=data.name, description=data.description,
            importance=data.importance,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/knowledge-points/{kp_id}")
async def update_knowledge_point(
    kp_id: str,
    data: KnowledgePointUpdate,
    current_user: dict = Depends(get_current_user),
):
    """更新知识点"""
    success = await KnowledgeGraphService.update_knowledge_point(
        id=kp_id, name=data.name,
        description=data.description, importance=data.importance,
    )
    if not success:
        raise HTTPException(status_code=404, detail="知识点未找到")
    return {"message": "更新成功"}


@router.delete("/knowledge-points/{kp_id}")
async def delete_knowledge_point(
    kp_id: str,
    current_user: dict = Depends(get_current_user),
):
    """删除知识点"""
    success = await KnowledgeGraphService.delete_knowledge_point(id=kp_id)
    if not success:
        raise HTTPException(status_code=404, detail="知识点未找到")
    return {"message": "删除成功"}


@router.put("/knowledge-points/positions")
async def batch_save_positions(
    positions: List[KnowledgePointPosition],
    current_user: dict = Depends(get_current_user),
):
    """批量保存知识点位置"""
    pos_list = [{"id": p.id, "x": p.x, "y": p.y} for p in positions]
    await KnowledgeGraphService.save_positions(pos_list)
    return {"message": f"已保存 {len(pos_list)} 个节点位置"}


# ─── 关系端点 ──────────────────────────────────────────────────────


@router.post("/relations", status_code=201)
async def create_relation(
    data: RelationCreate,
    current_user: dict = Depends(get_current_user),
):
    """创建知识点间关系"""
    success = await KnowledgeGraphService.create_relation(
        from_id=data.from_id, to_id=data.to_id, type=data.type
    )
    if not success:
        raise HTTPException(
            status_code=400, detail="创建关系失败，请确认两个知识点都存在"
        )
    return {"message": "关系创建成功"}


@router.delete("/relations")
async def delete_relation(
    from_id: str,
    to_id: str,
    type: str,
    current_user: dict = Depends(get_current_user),
):
    """删除知识点间关系"""
    success = await KnowledgeGraphService.delete_relation(
        from_id=from_id, to_id=to_id, type=type
    )
    if not success:
        raise HTTPException(status_code=404, detail="关系未找到")
    return {"message": "关系删除成功"}


# ─── 初始化端点 ────────────────────────────────────────────────────


@router.post("/subjects/init-math")
async def init_math_graph(current_user: dict = Depends(get_current_user)):
    """初始化数学知识图谱"""
    await KnowledgeGraphService.init_math_graph()
    return {"message": "数学知识图谱初始化完成"}


# ─── 掌握度端点 ────────────────────────────────────────────────────


@router.get("/children/{child_id}/mastery", response_model=List[MasteryEntry])
async def get_child_mastery(
    child_id: str,
    subject_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取孩子知识点掌握度"""
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")
    return await KnowledgeGraphService.get_child_mastery(child_id, subject_id)


@router.post("/children/{child_id}/mastery/refresh")
async def refresh_child_mastery(
    child_id: str,
    subject_name: str,
    current_user: dict = Depends(get_current_user),
):
    """全量刷新孩子知识点掌握度"""
    user_children = [c["id"] for c in current_user.get("children", [])]
    if child_id not in user_children:
        raise HTTPException(status_code=403, detail="无权访问该孩子的数据")
    await KnowledgeGraphService.update_child_mastery(child_id, subject_name)
    return {"message": "掌握度刷新成功"}
