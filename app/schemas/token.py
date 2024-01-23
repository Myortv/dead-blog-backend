from datetime import datetime

from pydantic import BaseModel, SecretStr


class SecretToken(BaseModel):
    token: SecretStr


class JwtToken(BaseModel):
    token: str
    meta: dict
    user_account_id: int
