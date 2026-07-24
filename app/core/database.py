from sqlmodel import SQLModel, create_engine

from .config import settings

# Convención de nombres
_naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s_%(column_0_name)s",
}
SQLModel.metadata.naming_convention = _naming_convention

# Motor de base de datos
engine = create_engine(
    str(settings.postgres_dsn),
    pool_recycle=1800,  # 30 minutos
    pool_size=5,
    max_overflow=10,
    connect_args={"options": "-c timezone=America/Mexico_City"},
    echo=settings.is_debug,
    echo_pool=False,
)
