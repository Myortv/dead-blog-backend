from typing import List

from pydantic import SecretStr

from asyncpg import Connection


from fastapiplugins.controllers import (
    DatabaseManager as DM,
)


@DM.acqure_connection()
async def get_by_code(
    code: SecretStr,
    conn: Connection = None,
) -> dict:
    result = await conn.fetch(
        'select * from account_creation_code where code = $1',
        code.get_secret_value(),
    )
    return result

