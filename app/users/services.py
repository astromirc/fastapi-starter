from uuid import UUID

from sqlmodel import Session, select

from app.core.security import hash_password

from app.shared.errors import DuplicateEmailError
from app.shared.timezone import now

from .models import User, UserCreate


def get_user_by_email(*, session: Session, email: str) -> User | None:
    email = email.lower().strip()
    stmt = select(User).where(User.email == email)
    return session.exec(stmt).first()


def get_user_by_id(*, session: Session, user_id: UUID) -> User | None:
    return session.get(User, user_id)


def update_last_login(*, session: Session, user: User) -> None:
    user.last_login = now()
    session.commit()


def create_user(
    *,
    session: Session,
    user_create: UserCreate,
    is_superuser: bool = False,
) -> User:
    if get_user_by_email(session=session, email=user_create.email) is not None:
        raise DuplicateEmailError()

    user = User(
        email=user_create.email.lower().strip(),
        name=user_create.name.strip().title(),
        hashed_password=hash_password(user_create.password.strip()),
        is_superuser=is_superuser,
    )
    session.add(user)
    session.commit()

    return user


def update_password(*, session: Session, user: User, password: str) -> None:
    user.hashed_password = hash_password(password.strip())
    session.commit()
