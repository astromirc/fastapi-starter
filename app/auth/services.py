from fastapi import BackgroundTasks
from sqlmodel import Session

from app.core.security import (
    TokenType,
    create_reset_password_token,
    decode_token,
    verify_password,
)

from app.shared.errors import InactiveUserError, InvalidTokenError
from app.users.models import User
from app.users.services import get_user_by_email, get_user_by_id, update_password

from .tasks import send_password_changed_email, send_reset_password_email

DUMMY_PASSWORD_HASH = "$2b$12$09Zfwqma9ovyIVqXyYM/H.vTc39vwZmG2gNl7c9Lcfxk98P4bn5f."  # noqa: S105


def authenticate_user(*, session: Session, username: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=username)

    if user is None:
        # Verificación simulada para evitar diferencias en tiempos de respuesta
        verify_password(password, DUMMY_PASSWORD_HASH)
        return None

    if not verify_password(password.strip(), user.hashed_password):
        return None

    return user


def forgot_password(
    *,
    session: Session,
    email: str,
    background_tasks: BackgroundTasks,
) -> None:
    user = get_user_by_email(session=session, email=email)

    if user is None or not user.is_active:
        return

    token = create_reset_password_token(user.id)
    background_tasks.add_task(send_reset_password_email, user.email, token)


def reset_password(
    *,
    session: Session,
    token: str,
    password: str,
    background_tasks: BackgroundTasks,
) -> None:
    user_id, _ = decode_token(token, token_type=TokenType.RESET_PASSWORD)
    user = get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise InvalidTokenError(
            "El enlace para restablecer tu contraseña no es válido o ha expirado.",
        )

    if not user.is_active:
        raise InactiveUserError()

    update_password(session=session, user=user, password=password)
    background_tasks.add_task(send_password_changed_email, user.email)
