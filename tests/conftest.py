from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

from app.main import app
from app.shared.dependencies import get_session

engine = create_engine(
    str(settings.get_postgres_dsn(host="postgres-test")),
    echo=False,
)


@pytest.fixture
def session() -> Generator[Session]:
    """Sesión de base de datos."""
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db_session:
        yield db_session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client(session: Session) -> Generator[TestClient]:
    """Cliente FastAPI con sobrescritura de dependencias."""
    app.dependency_overrides[get_session] = lambda: session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
