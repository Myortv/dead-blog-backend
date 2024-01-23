from typing import Optional
from datetime import datetime

from pydantic import BaseModel, SecretStr


class CategoryInDB(BaseModel):
    id: int
    title: str
    caption: Optional[str] = None
    is_pinned: bool


class CategoryCreate(BaseModel):
    title: str
    caption: Optional[str] = None
    is_pinned: bool


class CategoryUpdate(BaseModel):
    title: str
    caption: Optional[str] = None
    is_pinned: bool

