from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token

from app.shared.dependencies import DBSession
from app.shared.errors import InactiveUserError, InvalidCredentialsError
from app.users.services import update_last_login

from . import services
from .models import ForgotPassword, Message, ResetPassword, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    session: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = services.authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )

    if user is None:
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InactiveUserError()

    update_last_login(session=session, user=user)
    token = create_access_token(user.id)

    return Token(access_token=token)


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
def forgot_password(
    session: DBSession,
    data: ForgotPassword,
    background_tasks: BackgroundTasks,
) -> Message:
    services.forgot_password(
        session=session,
        email=data.email,
        background_tasks=background_tasks,
    )

    return Message(
        message=(
            f"Se ha enviado un correo a {data.email} "
            "con las instrucciones para restablecer tu contraseña."
        ),
    )


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    session: DBSession,
    data: ResetPassword,
    background_tasks: BackgroundTasks,
) -> Message:
    services.reset_password(
        session=session,
        token=data.token,
        password=data.password,
        background_tasks=background_tasks,
    )

    return Message(message="Tu contraseña ha sido actualizada exitosamente.")
