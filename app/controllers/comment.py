from typing import List

from asyncpg import Connection

from app.schemas.blog_comment import (
    PostCommentInDB,
    PostCommentPage,
    PostCommentCreate,
    PostCommentUpdate,
)

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
    insert_q,
    update_q,
    delete_q,
)


@DM.acqure_connection()
async def get_by_post_id(
    post_id: int,
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[PostCommentInDB]:
    result = await conn.fetch(
        'select '
            '* '
        'from '
            'blog_post_comment '
        'where '
            'blog_post_id = $1 '
        'order by '
            'created_at DESC '
        'offset $2 '
        'limit $3 ',
        post_id,
        offset,
        limit,
    )
    if not result:
        return result
    comments = [PostCommentInDB(**row) for row in result]
    total = await conn.fetchval(
        'select count(*) from blog_post_comment where blog_post_id = $1',
        post_id
    )
    if not total:
        total = 0
    return PostCommentPage(total=total, comments=comments)


@DM.acqure_connection()
async def get_by_id(
    comment_id: int,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *select_q(
            'blog_post_comment',
            id=comment_id,
        )
    )
    if result:
        return PostCommentInDB(**result)


@DM.acqure_connection()
async def create(
    comment_data: PostCommentCreate,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *insert_q(
            comment_data,
            'blog_post_comment',
        )
    )
    if result:
        return PostCommentInDB(**result)


@DM.acqure_connection()
async def update(
    comment_id: int,
    comment_data: PostCommentUpdate,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *update_q(
            comment_data,
            'blog_post_comment',
            id=comment_id,
        )
    )
    if result:
        return PostCommentInDB(**result)


@DM.acqure_connection()
async def delete(
    comment_id: int,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *delete_q(
            'blog_post_comment',
            id=comment_id,
        )
    )
    if result:
        return PostCommentInDB(**result)
