from datetime import timedelta
from enum import StrEnum
from uuid import UUID, uuid4

from bcrypt import checkpw, gensalt, hashpw
from jwt import (
    InvalidTokenError as PyJWTError,
    decode,
    encode,
)

from app.shared.errors import InvalidTokenError
from app.shared.timezone import now

from .config import settings


# Password Utilities
def hash_password(password: str) -> str:
    """Genera el hash de una contraseña."""
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña en texto plano contra su hash."""
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# Token Utilities
class TokenType(StrEnum):
    """Tipos de tokens JWT disponibles en la aplicación."""

    ACCESS_TOKEN = "access_token"  # noqa: S105
    RESET_PASSWORD = "reset_password"  # noqa: S105


def encode_token(
    *,
    user_id: UUID,
    token_type: TokenType,
    expires_in_minutes: int,
) -> str:
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": int((now() + timedelta(minutes=expires_in_minutes)).timestamp()),
        "jti": uuid4().hex,
    }

    return encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str, *, token_type: TokenType) -> tuple[UUID, str]:
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        if payload.get("type") != token_type:
            raise InvalidTokenError()

        sub = payload.get("sub")
        if not isinstance(sub, str):
            raise InvalidTokenError()

        jti = payload.get("jti")
        if not isinstance(jti, str) or len(jti) != 32:  # noqa: PLR2004
            raise InvalidTokenError()

        return UUID(sub), jti
    except PyJWTError, ValueError, TypeError:
        raise InvalidTokenError()


def create_access_token(user_id: UUID) -> str:
    """Crea un token de acceso."""
    return encode_token(
        user_id=user_id,
        token_type=TokenType.ACCESS_TOKEN,
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_reset_password_token(user_id: UUID) -> str:
    """Crea un token de restablecimiento de contraseña."""
    return encode_token(
        user_id=user_id,
        token_type=TokenType.RESET_PASSWORD,
        expires_in_minutes=5,
    )
