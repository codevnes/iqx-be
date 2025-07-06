from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.models.user import Role

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None

# Properties to receive on user creation
class UserCreate(UserBase):
    password: str

# Properties to receive on user update
class UserUpdate(UserBase):
    pass

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: UUID
    role: Role
    verified: bool

    class Config:
        from_attributes = True

# Properties to return to client
class UserRead(UserInDBBase):
    create_date: datetime
    update_date: Optional[datetime] = None

# Properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

# Alias for UserRead to maintain backward compatibility
User = UserRead 