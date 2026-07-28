import pytest
from sqlmodel import Session

from app.shared.dependencies import get_current_superuser
from app.shared.errors import PermissionDeniedError
from tests.helpers import create_user


def test_get_current_superuser_returns_user_data(session: Session) -> None:
    user = create_user(session, is_superuser=True)

    result = get_current_superuser(current_user=user)

    assert result.id == user.id
    assert result.email == user.email
    assert result.is_superuser is True


def test_get_current_superuser_with_non_superuser_raises_permission_denied(
    session: Session,
) -> None:
    user = create_user(session, is_superuser=False)

    with pytest.raises(PermissionDeniedError):
        get_current_superuser(current_user=user)
