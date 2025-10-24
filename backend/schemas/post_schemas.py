from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_ad: Optional[bool] = False


class PostOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    file_path: str
    owner_id: int
    is_approved: bool
    is_ad: bool
    created_at: datetime


class Config:
    orm_mode = True 