from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from app.core.config import settings
from app.core.email import send_email

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def _render_template(template_name: str, context: dict[str, Any] | None = None) -> str:
    ctx = {}
    if context:
        ctx.update(context)

    template = _env.get_template(template_name)
    return template.render(**ctx)


def send_reset_password_email(email: str, reset_token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    html = _render_template("reset_password.html", {"reset_url": reset_url})

    send_email(email, "Recupera el acceso a tu cuenta", html)


def send_password_changed_email(email: str) -> None:
    html = _render_template("password_changed.html")
    send_email(email, "Tu contraseña ha sido actualizada", html)
