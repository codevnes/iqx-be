from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import user as models_user
from app.schemas import user as schemas_user
from app.api.v1 import deps

router = APIRouter()

@router.get("/me", response_model=schemas_user.UserRead)
async def read_users_me(
    current_user: models_user.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user 