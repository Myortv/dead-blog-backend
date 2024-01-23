from typing import Optional, List

from datetime import timedelta

from os.path import dirname, abspath, join

import aiohttp

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

from cryptography.hazmat.primitives import serialization

from fastapiplugins.token import TokenManager


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='env.sh', env_file_encoding='utf-8')

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'Blog'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/docs'

    refresh_token_url: str = 'api/v1/token/refresh'


    refresh_token_expires: timedelta = timedelta(weeks=1)
    REFRESH_TOKEN_HOURS: int
    access_token_expires: timedelta = timedelta(minutes=30)
    ACCESS_TOKEN_MINUTES: int


    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: Optional[str] = 'localhost'

    PRIVATE_JWT_KEY: Optional[str] = None
    PUBLIC_JWT_KEY: Optional[str] = None
    JWT_ALGORITHM: str = 'RS256'
    PEM_PASS: str

    AIOHTTP_SESSION: Optional[aiohttp.ClientSession] = None

    admin_role: Optional[str] = 'admin'

    @property
    def aiohttp_session(self):
        if not self.AIOHTTP_SESSION:
            self.AIOHTTP_SESSION = aiohttp.ClientSession()
        return self.AIOHTTP_SESSION

    def load_public_key(self):
        if not self.PUBLIC_JWT_KEY:
            with open(join(BASE_DIR, 'public_key.pem'), 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                )
                self.PUBLIC_JWT_KEY = public_key
        return self.PUBLIC_JWT_KEY

    def load_privat_key(self):
        if not self.PRIVATE_JWT_KEY:
            with open(join(BASE_DIR, 'private_key.pem'), 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=bytes(self.PEM_PASS, 'utf-8'),
                )
                self.PRIVATE_JWT_KEY = private_key
        return self.PRIVATE_JWT_KEY

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
settings.load_public_key()
settings.load_privat_key()

tags_metadata = [
    {
        "name": "User",
        "description": "Users",
    },
    {
        "name": "Token",
        "description": "Jwt token",
    },
    {
        "name": "Blog",
        "description": "Blog posts",
    },
    {
        "name": "Category",
        "description": "Categories for blog",
    },
    {
        "name": "Comment",
        "description": "Comments for blog posts",
    },
]


token_manager = TokenManager(
    settings.PRIVATE_JWT_KEY,
    settings.PUBLIC_JWT_KEY,
    settings.JWT_ALGORITHM,
)

