from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.database import engine
from app.core.security import TokenType, decode_token

from app.shared.errors import (
    InactiveUserError,
    InvalidTokenError,
    PermissionDeniedError,
)
from app.users.models import User
from app.users.services import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


def get_current_user(
    session: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    user_id, _ = decode_token(token, token_type=TokenType.ACCESS_TOKEN)
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise InvalidTokenError()

    if not user.is_active:
        raise InactiveUserError()

    return user


def get_current_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise PermissionDeniedError()

    return current_user


DBSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]
