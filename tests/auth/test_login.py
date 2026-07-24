from datetime import timedelta

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.security import TokenType, decode_token

from app.shared.timezone import now
from tests.helpers import create_user


def test_login_with_correct_credentials_returns_token(
    session: Session,
    client: TestClient,
) -> None:
    user = create_user(session)

    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "password123"},
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body["token_type"] == "bearer"

    user_id, token_id = decode_token(
        body["access_token"],
        token_type=TokenType.ACCESS_TOKEN,
    )
    assert user_id == user.id
    assert len(token_id) == 32


def test_login_with_correct_credentials_updates_last_login(
    session: Session,
    client: TestClient,
) -> None:
    user = create_user(session)
    before_last_login = now() - timedelta(seconds=5)

    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "password123"},
    )

    assert response.status_code == status.HTTP_200_OK

    session.refresh(user)
    assert user.last_login is not None
    assert before_last_login < user.last_login


@pytest.mark.parametrize(
    "email,password",
    [
        ("user@example.com", "WrongPassword!"),
        ("unknown@example.com", "Password123!"),
    ],
    ids=["wrong_password", "nonexistent_user"],
)
def test_login_with_incorrect_credentials_returns_unauthorized(
    session: Session,
    client: TestClient,
    email: str,
    password: str,
) -> None:
    create_user(session, email="user@example.com")

    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.headers["www-authenticate"] == "Bearer"


def test_login_with_inactive_user_returns_forbidden(
    session: Session,
    client: TestClient,
) -> None:
    user = create_user(session, is_active=False)

    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "password123"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "email,password",
    [
        ("User@Example.com", "password123"),
        ("  user@example.com  ", "password123"),
        ("user@example.com", "  password123  "),
    ],
    ids=["email_uppercase", "email_whitespace", "password_whitespace"],
)
def test_login_with_normalized_credentials_returns_token(
    session: Session,
    client: TestClient,
    email: str,
    password: str,
) -> None:
    create_user(session, email="user@example.com")

    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.parametrize(
    "form_data",
    [
        {"username": "user@example.com"},
        {"password": "Password123!"},
    ],
    ids=["missing_password", "missing_username"],
)
def test_login_with_invalid_form_returns_unprocessable_content(
    form_data: dict[str, str],
    client: TestClient,
) -> None:
    response = client.post("/auth/login", data=form_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
