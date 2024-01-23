from typing import List, Optional


from fastapi import APIRouter, Depends, HTTPException

from app.controllers import blog as blog_controller

from app.schemas.blog_post import (
    PostInDB,
    PostPage,
    PostCreate,
    PostUpdate,
)

from app.permissions import blog_post as blog_post_permissions
from app.utils.deps import identify_request


api = APIRouter()


@api.get('/latest', response_model=PostPage)
async def get_last_posts(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if result := await blog_controller.get_latest(
        offset,
        limit,
    ):
        return result
    raise HTTPException(404)


@api.get('/page/by-category', response_model=PostPage)
async def get_post_by_category(
    category_id: int,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if result := await blog_controller.get_by_category(
        category_id,
        offset,
        limit,
    ):
        return result
    raise HTTPException(404)


@api.get('/', response_model=PostInDB)
async def get_post_by_id(
    post_id: int
):
    if result := await blog_controller.get_by_id(post_id):
        return result
    raise HTTPException(404)


@api.post('/', response_model=PostInDB)
async def create(
    post_data: PostCreate,
    identity: dict = Depends(identify_request),
):
    if await blog_post_permissions.is_admin(identity):
        if result := await blog_controller.create(
            post_data
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


@api.put('/', response_model=PostInDB)
async def update(
    post_id: int,
    post_data: PostUpdate,
    identity: dict = Depends(identify_request),
):
    if await blog_post_permissions.is_admin(identity):
        if result := await blog_controller.update(
            post_id,
            post_data
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


@api.delete('/', response_model=PostInDB)
async def delete(
    post_id: int,
    identity: dict = Depends(identify_request),
):
    if await blog_post_permissions.is_admin(identity):
        if result := await blog_controller.delete(
            post_id
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


