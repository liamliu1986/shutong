from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class ChildModel(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    name: str
    grade: int = Field(ge=7, le=12)
    subjects: List[str] = []


class UserModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: str
    password_hash: str
    children: List[ChildModel] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
