ARG PYTHON_VERSION=3.14

# ------------------------ BASE ------------------------
FROM python:${PYTHON_VERSION}-slim AS base

RUN useradd -u 1000 -U -m appuser

ARG VENV_PATH="/home/appuser/.venv"

ENV TZ=America/Mexico_City \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="${VENV_PATH}" \
    PATH="${VENV_PATH}/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --chmod=755 bin/ /usr/local/bin/

USER appuser
WORKDIR /app

COPY --chown=appuser pyproject.toml uv.lock* ./

# ------------------------ LOCAL ------------------------
FROM base AS local

ENV ENVIRONMENT=local

RUN --mount=type=cache,target=/home/appuser/.cache/uv,uid=1000,gid=1000 \
    uv sync

# ------------------------ PRODUCTION ------------------------
FROM base AS production

ENV ENVIRONMENT=production \
    UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/home/appuser/.cache/uv,uid=1000,gid=1000 \
    uv sync --frozen --no-dev
