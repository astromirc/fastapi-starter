from datetime import datetime
from uuid import UUID, uuid7

from pydantic import EmailStr
from sqlmodel import DateTime, Field, SQLModel

from app.shared.timezone import now


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid7, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=50)
    name: str = Field(max_length=50)
    hashed_password: str = Field(max_length=60)
    is_superuser: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=now,
        sa_type=DateTime(timezone=True),
    )
    last_login: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
    )
