from aio_pika import ExchangeType

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.core.configs import settings, tags_metadata

from fastapiplugins.exceptions import prepare_exceptions

from fastapiplugins.controllers import (
    DatabaseManager,
    exceptions as plugins_controllers_exceptions,
)
from fastapiplugins.token import exceptions as token_exceptions


handled_exceptions = prepare_exceptions(
    plugins_controllers_exceptions,
    token_exceptions
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.0.1',
    docs_url=settings.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    exception_handlers=handled_exceptions,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from app.api.v1 import (
    token,
    user,
    blog,
    category,
    comment,
)


app.include_router(
    token.api,
    prefix=settings.API_V1_STR + '/token',
    tags=["Token"]
)

app.include_router(
    user.api,
    prefix=settings.API_V1_STR + '/user',
    tags=["User"]
)

app.include_router(
    blog.api,
    prefix=settings.API_V1_STR + '/blog',
    tags=["Blog"]
)
app.include_router(
    category.api,
    prefix=settings.API_V1_STR + '/category',
    tags=["Category"]
)
app.include_router(
    comment.api,
    prefix=settings.API_V1_STR + '/comment',
    tags=["Comment"]
)


@app.on_event('startup')
async def startup():
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )


@app.on_event('shutdown')
async def shutdown():
    await DatabaseManager.stop()
    await settings.aiohttp_session.close()
