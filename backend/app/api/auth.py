from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """用户注册"""
    return await AuthService.register(user_data)


@router.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """用户登录"""
    return await AuthService.login(user_data)


@router.get("/users/me", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        children=current_user.get("children", [])
    )
