from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.schemas.user import ChildCreate
from app.database import get_mongodb
from datetime import datetime
from bson import ObjectId

router = APIRouter()


@router.get("/users/me/children")
async def get_children(current_user: dict = Depends(get_current_user)):
    """获取孩子列表"""
    return current_user.get("children", [])


@router.post("/users/me/children")
async def create_child(
    data: ChildCreate,
    current_user: dict = Depends(get_current_user)
):
    """添加孩子"""
    db = get_mongodb()

    child = {
        "id": str(ObjectId()),
        "name": data.name,
        "grade": data.grade,
        "subjects": data.subjects,
        "created_at": datetime.now()
    }

    await db.users.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$push": {"children": child}}
    )

    return child


@router.delete("/users/me/children/{child_id}")
async def delete_child(
    child_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除孩子"""
    db = get_mongodb()

    await db.users.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$pull": {"children": {"id": child_id}}}
    )

    return {"message": "删除成功"}
