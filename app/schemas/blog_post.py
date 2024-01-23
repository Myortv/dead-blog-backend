from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, SecretStr


class PostInDB(BaseModel):
    id: int
    category_id: int
    title: str
    caption: Optional[str] = None
    body: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class PostPage(BaseModel):
    posts: List[PostInDB]
    total: Optional[int] = 0


class PostCreate(BaseModel):
    category_id: int
    title: str
    caption: Optional[str] = None
    body: str


class PostUpdate(BaseModel):
    category_id: int
    title: str
    caption: Optional[str] = None
    body: str

