import uuid
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base

class Role(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    verified = Column(Boolean(), default=False, nullable=False)
    is_active = Column(Boolean(), default=True)

    create_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_date = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __mapper_args__ = {"eager_defaults": True} 