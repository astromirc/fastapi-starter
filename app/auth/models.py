from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class ForgotPassword(SQLModel):
    email: EmailStr


class ResetPassword(SQLModel):
    token: str
    password: str = Field(min_length=8, max_length=50)


class Message(SQLModel):
    message: str
