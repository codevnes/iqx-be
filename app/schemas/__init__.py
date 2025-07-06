from app.schemas.user import User, UserCreate, UserUpdate, UserInDB
from app.schemas.token import Token, TokenPayload
from app.schemas.company import Company, CompanyCreate, CompanyUpdate

from typing import Generic, TypeVar, Sequence, Optional, Dict, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)
    search: Optional[str] = None
    page: int = Field(1, ge=1)

class PaginatedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    page_size: int
    pages: int
    
    @classmethod
    def create(cls, items: Sequence[T], total: int, params: PaginationParams) -> "PaginatedResponse[T]":
        page_size = params.limit
        page = params.page
        pages = (total + page_size - 1) // page_size if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )
