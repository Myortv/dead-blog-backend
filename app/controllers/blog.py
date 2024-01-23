from typing import List

from asyncpg import Connection

from app.schemas.blog_post import (
    PostInDB,
    PostPage,
    PostCreate,
    PostUpdate,
)

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
    insert_q,
    update_q,
    delete_q,
)


@DM.acqure_connection()
async def get_latest(
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[PostInDB]:
    result = await conn.fetch(
        'select '
            '* '
        'from '
            'blog_post '
        'order by '
            'COALESCE(updated_at, created_at) DESC '
        'offset $1 '
        'limit $2 ',
        offset,
        limit,
    )
    if not result:
        return result
    posts = [PostInDB(**row) for row in result]
    total = await conn.fetchval(
        'select count(*) from blog_post',
    )
    if not total:
        total = 0
    return PostPage(posts=posts, total=total)



@DM.acqure_connection()
async def get_by_category(
    category_id: int,
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[PostInDB]:
    result = await conn.fetch(
        'select '
            '* '
        'from '
            'blog_post '
        'where '
            'category_id = $1 '
        'order by '
            'COALESCE(updated_at, created_at) DESC '
        'offset $2 '
        'limit $3 ',
        category_id,
        offset,
        limit,
    )
    if not result:
        return result
    posts = [PostInDB(**row) for row in result]
    total = await conn.fetchval(
        'select count(*) from blog_post where category_id = $1',
        category_id
    )
    if not total:
        total = 0
    return PostPage(posts=posts, total=total)


@DM.acqure_connection()
async def get_by_id(
    post_id: int,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *select_q(
            'blog_post',
            id=post_id,
        )
    )
    if result:
        return PostInDB(**result)


@DM.acqure_connection()
async def create(
    post_data: PostCreate,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *insert_q(
            post_data,
            'blog_post',
        )
    )
    if result:
        return PostInDB(**result)


@DM.acqure_connection()
async def update(
    post_id: int,
    post_data: PostUpdate,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *update_q(
            post_data,
            'blog_post',
            id=post_id,
        )
    )
    if result:
        return PostInDB(**result)


@DM.acqure_connection()
async def delete(
    post_id: int,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *delete_q(
            'blog_post',
            id=post_id,
        )
    )
    if result:
        return PostInDB(**result)
