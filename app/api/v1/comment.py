from typing import Optional


from fastapi import APIRouter, Depends, HTTPException

from app.controllers import comment as comment_controller

from app.schemas.blog_comment import (
    PostCommentInDB,
    PostCommentPage,
    PostCommentCreate,
    PostCommentUpdate,
)

from app.permissions import comment as comment_permissions
from app.utils.deps import identify_request


api = APIRouter()


@api.get('/page/by-blog-post', response_model=PostCommentPage)
async def get_comment_by_post_id(
    post_id: int,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if result := await comment_controller.get_by_post_id(
        post_id,
        offset,
        limit,
    ):
        return result
    raise HTTPException(404)


@api.get('/', response_model=PostCommentInDB)
async def get_comment_by_id(
    comment_id: int
):
    if result := await comment_controller.get_by_id(comment_id):
        return result
    raise HTTPException(404)


@api.post('/', response_model=PostCommentInDB)
async def create(
    comment_data: PostCommentCreate,
    # identity: dict = Depends(identify_request),
):
    # if await comment_permissions.is_admin(identity):
    if result := await comment_controller.create(
        comment_data
    ):
        return result
    raise HTTPException(404)
    # raise HTTPException(403)


@api.put('/', response_model=PostCommentInDB)
async def update(
    comment_id: int,
    comment_data: PostCommentUpdate,
    identity: dict = Depends(identify_request),
):
    if await comment_permissions.is_admin(identity):
        if result := await comment_controller.update(
            comment_id,
            comment_data
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


@api.delete('/', response_model=PostCommentInDB)
async def delete(
    comment_id: int,
    identity: dict = Depends(identify_request),
):
    if await comment_permissions.is_admin(identity):
        if result := await comment_controller.delete(
            comment_id
        ):
            return result
        raise HTTPException(404)
    raise HTTPException(403)


