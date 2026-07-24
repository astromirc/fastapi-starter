from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session

from tests.helpers import create_user


def test_forgot_password_with_valid_user_returns_accepted(
    session: Session,
    client: TestClient,
    mocker: MockerFixture,
) -> None:
    mock_send = mocker.patch("app.auth.services.send_reset_password_email")
    user = create_user(session)

    response = client.post("/auth/forgot-password", json={"email": user.email})

    assert response.status_code == status.HTTP_202_ACCEPTED
    mock_send.assert_called_once()


def test_forgot_password_with_unknown_user_returns_accepted(
    client: TestClient,
    mocker: MockerFixture,
) -> None:
    mock_send = mocker.patch("app.auth.services.send_reset_password_email")

    response = client.post(
        "/auth/forgot-password",
        json={"email": "unknown@example.com"},
    )

    assert response.status_code == status.HTTP_202_ACCEPTED
    mock_send.assert_not_called()


def test_forgot_password_with_inactive_user_returns_accepted(
    session: Session,
    client: TestClient,
    mocker: MockerFixture,
) -> None:
    mock_send = mocker.patch("app.auth.services.send_reset_password_email")
    user = create_user(session, is_active=False)

    response = client.post("/auth/forgot-password", json={"email": user.email})

    assert response.status_code == status.HTTP_202_ACCEPTED
    mock_send.assert_not_called()
