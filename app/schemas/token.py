from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[UUID] = None

class RefreshToken(BaseModel):
    refresh_token: str 