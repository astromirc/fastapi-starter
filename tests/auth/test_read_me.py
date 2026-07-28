from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.helpers import create_user, get_auth_headers


def test_read_me_with_valid_token_returns_user_data(
    session: Session,
    client: TestClient,
) -> None:
    user = create_user(session)

    response = client.get("/users/me", headers=get_auth_headers(user))
    assert response.status_code == status.HTTP_200_OK

    body = response.json()
    assert body["id"] == str(user.id)
    assert body["email"] == user.email
    assert body["name"] == user.name
    assert body["is_superuser"] is False
    assert body["is_active"] is True
    assert "hashed_password" not in body


def test_read_me_without_token_returns_unauthorized(client: TestClient) -> None:
    response = client.get("/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.headers["www-authenticate"] == "Bearer"
