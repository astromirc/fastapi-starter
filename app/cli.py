import typer
from pydantic import ValidationError
from sqlmodel import Session

from app.core.database import engine

from app.shared.errors import DuplicateEmailError
from app.users.models import UserCreate
from app.users.services import create_user

app = typer.Typer()


@app.command()
def createsuperuser() -> None:
    email = typer.prompt("Correo electrónico")
    name = typer.prompt("Nombre")
    password = typer.prompt(
        "Contraseña",
        hide_input=True,
        confirmation_prompt=True,
    )

    try:
        user_create = UserCreate.model_validate(
            {
                "email": email,
                "name": name,
                "password": password,
            }
        )
    except ValidationError:
        typer.secho(
            "Algo de lo que ingresaste es incorrecto, verifica tu información.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    with Session(engine) as session:
        try:
            create_user(session=session, user_create=user_create, is_superuser=True)
        except DuplicateEmailError as e:
            typer.secho(str(e), fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    typer.echo()
    typer.secho(
        f"Superusuario creado: {user_create.email}",
        fg=typer.colors.GREEN,
        bold=True,
    )


if __name__ == "__main__":
    app()
