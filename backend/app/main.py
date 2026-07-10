"""
书童 - 智能学习助手 Web 应用
FastAPI 主应用入口
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import connect_mongodb, close_mongodb, connect_neo4j, close_neo4j
from app.api import auth

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# API 路由
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时连接数据库
    logger.info("正在启动应用...")
    await connect_mongodb()
    await connect_neo4j()
    logger.info("数据库连接完成")
    yield
    # 关闭时断开数据库连接
    logger.info("正在关闭应用...")
    await close_mongodb()
    await close_neo4j()
    logger.info("数据库连接已关闭")


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="书童 - 智能学习助手 API",
        lifespan=lifespan
    )

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
    app.include_router(api_router)

    # 根路由
    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running"
        }

    # 健康检查路由
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


# 创建应用实例
app = create_app()
