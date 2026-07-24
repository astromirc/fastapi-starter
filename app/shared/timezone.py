from datetime import datetime
from zoneinfo import ZoneInfo

_TZ = ZoneInfo("America/Mexico_City")


def now() -> datetime:
    """Retorna la fecha y hora actual con zona horaria."""
    return datetime.now(_TZ)


def strptime(value: str, fmt: str) -> datetime:
    """
    Parsea un texto a datetime asignándole la zona horaria.

    Ejemplo:
        strptime("2026-07-24 15:30:00", "%Y-%m-%d %H:%M:%S")
    """
    return datetime.strptime(value, fmt).replace(tzinfo=_TZ)


def strftime(value: datetime, fmt: str) -> str:
    """
    Formatea un objeto datetime a cadena de texto.

    Ejemplo:
        strftime(now(), "%Y-%m-%d %H:%M:%S")
    """
    return value.strftime(fmt)
