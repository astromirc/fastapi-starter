from uuid import uuid4

import pytest
from sqlmodel import Session

from app.core.security import create_access_token, create_reset_password_token

from app.shared.dependencies import get_current_user
from app.shared.errors import InactiveUserError, InvalidTokenError
from tests.helpers import create_user


def test_get_current_user_with_valid_token_returns_user(session: Session) -> None:
    user = create_user(session)

    result = get_current_user(session=session, token=create_access_token(user.id))

    assert result.id == user.id
    assert result.email == user.email


def test_get_current_user_with_nonexistent_user_raises_invalid_token(
    session: Session,
) -> None:
    orphan_token = create_access_token(uuid4())

    with pytest.raises(InvalidTokenError):
        get_current_user(session=session, token=orphan_token)


def test_get_current_user_with_inactive_user_raises_inactive_user(
    session: Session,
) -> None:
    user = create_user(session, is_active=False)

    with pytest.raises(InactiveUserError):
        get_current_user(session=session, token=create_access_token(user.id))


def test_get_current_user_with_wrong_token_type_raises_invalid_token(
    session: Session,
) -> None:
    user = create_user(session)

    with pytest.raises(InvalidTokenError):
        get_current_user(
            session=session,
            token=create_reset_password_token(user.id),
        )


def test_get_current_user_with_malformed_token_raises_invalid_token(
    session: Session,
) -> None:
    with pytest.raises(InvalidTokenError):
        get_current_user(session=session, token="not.a.valid.jwt")
