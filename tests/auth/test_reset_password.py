from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session

from app.core.security import (
    create_access_token,
    create_reset_password_token,
    verify_password,
)

from tests.helpers import create_user


def test_reset_password_with_valid_token_updates_password(
    session: Session,
    client: TestClient,
    mocker: MockerFixture,
) -> None:
    mock_send = mocker.patch("app.auth.services.send_password_changed_email")
    user = create_user(session)
    token = create_reset_password_token(user.id)
    new_password = "NewPassword123!"

    response = client.post(
        "/auth/reset-password",
        json={"token": token, "password": new_password},
    )

    assert response.status_code == status.HTTP_200_OK
    mock_send.assert_called_once_with(user.email)

    session.refresh(user)
    assert verify_password(new_password, user.hashed_password)


def test_reset_password_with_invalid_token_returns_unauthorized(
    client: TestClient,
) -> None:
    response = client.post(
        "/auth/reset-password",
        json={"token": "invalid_token", "password": "NewPassword123!"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_reset_password_with_access_token_returns_unauthorized(
    session: Session,
    client: TestClient,
) -> None:
    user = create_user(session)
    access_token = create_access_token(user.id)

    response = client.post(
        "/auth/reset-password",
        json={"token": access_token, "password": "NewPassword123!"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_reset_password_with_inactive_user_returns_forbidden(
    session: Session,
    client: TestClient,
) -> None:
    user = create_user(session, is_active=False)
    token = create_reset_password_token(user.id)

    response = client.post(
        "/auth/reset-password",
        json={"token": token, "password": "NewPassword123!"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
