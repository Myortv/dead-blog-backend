from typing import List

import ujson

from asyncpg import Connection

from app.schemas.category import (
    CategoryInDB,
    CategoryCreate,
    CategoryUpdate,
)

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
    insert_q,
    update_q,
    delete_q,
)


@DM.acqure_connection()
async def get_all(
    conn: Connection = None,
) -> List[CategoryInDB]:
    result = await conn.fetch(
        'select '
            '* '
        'from '
            'category '
        'order by '
            'is_pinned DESC '
    )
    if not result:
        return result
    categorys = [CategoryInDB(**row) for row in result]
    return categorys


@DM.acqure_connection()
async def get_by_id(
    category_id: int,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *select_q(
            'category',
            id=category_id,
        )
    )
    if result:
        return CategoryInDB(**result)


@DM.acqure_connection()
async def create(
    category_data: CategoryCreate,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *insert_q(
            category_data,
            'category',
        )
    )
    if result:
        return CategoryInDB(**result)


@DM.acqure_connection()
async def update(
    category_id: int,
    category_data: CategoryUpdate,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *update_q(
            category_data,
            'category',
            id=category_id,
        )
    )
    if result:
        return CategoryInDB(**result)


@DM.acqure_connection()
async def delete(
    category_id: int,
    conn: Connection = None,
):
    result = await conn.fetchrow(
        *delete_q(
            'category',
            id=category_id,
        )
    )
    if result:
        return CategoryInDB(**result)
