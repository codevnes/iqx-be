from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import ValidationError

from app.crud import crud_user
from app.models import user as models_user
from app.schemas import user as schemas_user
from app.schemas import token as schemas_token
from app.api.v1 import deps
from app.core.config import settings
from app.core import security
from app.core.notifications import send_discord_notification

router = APIRouter()

@router.post("/register", response_model=schemas_user.UserRead)
async def register(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas_user.UserCreate,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Create new user.
    """
    user = await crud_user.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud_user.user.create(db, obj_in=user_in)
    
    # Gửi thông báo đến Discord
    notification_message = f"🎉 **Thành viên đăng ký thành công !**\n" \
                          f"**Email:** {user.email}\n" \
                          f"**Phone:** {user.phone}\n" \
                          f"**Tên:** {user.full_name}\n" \
                          f"**Thời gian:** {user.create_date.strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Sử dụng background task để không làm chậm phản hồi API
    background_tasks.add_task(send_discord_notification, notification_message)
    
    return user

@router.post("/login", response_model=schemas_token.Token)
async def login(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await crud_user.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.post("/refresh-token", response_model=schemas_token.Token)
async def refresh_token(
    *,
    db: AsyncSession = Depends(deps.get_db),
    refresh_token_in: schemas_token.RefreshToken,
) -> Any:
    """
    Refresh access token.
    """
    try:
        payload = jwt.decode(
            refresh_token_in.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas_token.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, invalid refresh token",
        )
    
    user = await crud_user.user.get(db, id=token_data.sub)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    } 