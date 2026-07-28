from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.shared.errors import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    PermissionDeniedError,
)


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(InvalidCredentialsError)
    @app.exception_handler(InvalidTokenError)
    def unauthorized_handler(
        _request: Request,
        exc: InvalidCredentialsError | InvalidTokenError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InactiveUserError)
    def inactive_user_handler(
        _request: Request,
        exc: InactiveUserError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.message},
        )

    @app.exception_handler(PermissionDeniedError)
    def permission_denied_handler(
        _request: Request,
        exc: PermissionDeniedError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.message},
        )

    # Errores no controlados (asegura respuesta JSON)
    @app.exception_handler(Exception)
    def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Algo salió mal. Inténtalo de nuevo más tarde."},
        )
