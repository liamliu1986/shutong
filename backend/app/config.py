"""
应用配置模块
使用 pydantic-settings 管理配置，支持从环境变量和 .env 文件加载
"""
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import model_validator


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基础配置
    APP_NAME: str = "书童"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # MongoDB 配置
    MONGODB_URI: str = "mongodb://localhost:27017"

    # Neo4j 配置
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # JWT 认证配置
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 百度 OCR API 配置
    BAIDU_OCR_API_KEY: str = ""
    BAIDU_OCR_SECRET_KEY: str = ""

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    @model_validator(mode="after")
    def check_secret_key(self):
        """应用启动时检查 SECRET_KEY 是否已设置"""
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY 环境变量未设置，请设置一个强密钥")
        return self

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
