from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, SecretStr


class PostCommentInDB(BaseModel):
    id: int
    blog_post_id: int
    user_name: str
    body: str
    created_at: datetime


class PostCommentPage(BaseModel):
    total: int
    comments: List[PostCommentInDB]


class PostCommentCreate(BaseModel):
    blog_post_id: int
    user_name: str
    body: str


class PostCommentUpdate(BaseModel):
    blog_post_id: int
    user_name: str
    body: str

