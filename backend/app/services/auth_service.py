from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from app.database import get_mongodb
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token


class AuthService:
    @staticmethod
    async def register(user_data: UserCreate) -> TokenResponse:
        db = get_mongodb()

        # 检查用户是否已存在
        existing_user = await db.users.find_one({
            "$or": [
                {"email": user_data.email},
                {"username": user_data.username}
            ]
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名或邮箱已存在"
            )

        # 创建用户
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = get_password_hash(user_data.password)
        del user_dict["password"]
        user_dict["children"] = []
        user_dict["created_at"] = datetime.now()
        user_dict["updated_at"] = datetime.now()

        result = await db.users.insert_one(user_dict)
        user_id = str(result.inserted_id)

        # 生成 Token
        access_token = create_access_token(data={"sub": user_id})

        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user_id,
                username=user_data.username,
                email=user_data.email,
                children=[]
            )
        )

    @staticmethod
    async def login(user_data: UserLogin) -> TokenResponse:
        db = get_mongodb()

        # 查找用户
        user = await db.users.find_one({"email": user_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )

        # 验证密码
        if not verify_password(user_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )

        # 生成 Token
        user_id = str(user["_id"])
        access_token = create_access_token(data={"sub": user_id})

        return TokenResponse(
            access_token=access_token,
            user=UserResponse(
                id=user_id,
                username=user["username"],
                email=user["email"],
                children=user.get("children", [])
            )
        )

    @staticmethod
    async def get_current_user(user_id: str) -> UserResponse:
        db = get_mongodb()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            children=user.get("children", [])
        )
