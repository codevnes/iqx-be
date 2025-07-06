from typing import Generator, Optional
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import crud_user
from app.models.user import User
from app.schemas.token import TokenPayload
from app.schemas import PaginationParams
from app.db.session import get_db

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    current_user = await crud_user.user.get(db, id=token_data.sub)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


def get_pagination_params(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None)
) -> PaginationParams:
    """
    A dependency that returns pagination parameters.
    Can be reused across multiple API endpoints.
    """
    skip = (page - 1) * page_size
    return PaginationParams(skip=skip, limit=page_size, search=search, page=page) 