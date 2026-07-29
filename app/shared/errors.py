class AppError(Exception):
    message = "Ha ocurrido un error."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message if message is not None else self.message)


class InvalidTokenError(AppError):
    message = "El token no es válido o ha expirado."


class InvalidCredentialsError(AppError):
    message = "Los datos de acceso son incorrectos. Por favor, verifica tu información."


class InactiveUserError(AppError):
    message = "Tu cuenta está suspendida."


class PermissionDeniedError(AppError):
    message = "No tienes permisos para realizar esta acción."


class DuplicateEmailError(AppError):
    message = "Ya existe un usuario asociado al correo ingresado."
