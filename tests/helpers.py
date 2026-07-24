from typing import Any
from uuid import uuid4

from sqlmodel import Session

from app.core.security import create_access_token, hash_password

from app.users.models import User


def create_user(session: Session, **overrides: Any) -> User:
    """Crea un usuario en la base de datos de testing."""
    defaults = {
        "email": f"{uuid4().hex}@test.com",
        "name": "Test User",
        "hashed_password": hash_password("password123"),
    }

    defaults.update(overrides)

    user = User.model_validate(defaults)
    session.add(user)
    session.commit()

    return user


def get_auth_headers(user: User) -> dict[str, str]:
    """Genera los headers de autenticación para un usuario."""
    token = create_access_token(user_id=user.id)
    return {"Authorization": f"Bearer {token}"}
