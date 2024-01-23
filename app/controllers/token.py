from typing import List

import ujson

from asyncpg import Connection

from app.schemas.token import (
    JwtToken,
    SecretToken,
)

from fastapiplugins.controllers import (
    DatabaseManager as DM,
)


@DM.acqure_connection()
async def save_refresh_token(
    refresh_token: str,
    user_id: int,
    meta: dict,
    conn: Connection = None,
) -> dict:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetchrow(
        'insert into '
            'jwt_token ( '
                'token, '
                'user_account_id, '
                'meta '
            ') '
        'values '
            '($1, $2, $3) '
        'returning * ',
        refresh_token,
        user_id,
        meta,
    )
    if not result:
        return result
    token = JwtToken(**result)
    return token


@DM.acqure_connection()
async def close_token(
    refresh_token: str,
    conn: Connection = None,
):
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetchrow(
        'delete from '
            'jwt_token '
            'where token = $1 '
        'returning * ',
        refresh_token,
    )
    if not result:
        return result
    token = JwtToken(**result)
    return token


@DM.acqure_connection()
async def get_token(
    refresh_token: str,
    conn: Connection = None,
) -> dict:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetchrow(
        'select * from jwt_token where token = $1 ',
        refresh_token,
    )
    if not result:
        return result
    token = JwtToken(**result)
    return token


@DM.acqure_connection()
async def list(
    user_id: int,
    conn: Connection = None,
) -> List[dict]:
    await conn.set_type_codec(
        'json',
        encoder=ujson.dumps,
        decoder=ujson.loads,
        schema='pg_catalog',
    )
    result = await conn.fetch(
        'select * from jwt_token where user_account_id = $1',
        user_id,
    )
    if not result:
        return result
    tokens = [JwtToken(**token) for token in result]
    return tokens


