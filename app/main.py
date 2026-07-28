from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import setup_exception_handlers

from app.auth.routers import router as auth_router
from app.users.routers import router as users_router

app = FastAPI(
    title=settings.NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    debug=settings.is_debug,
    docs_url="/docs" if settings.is_debug else None,
    redoc_url="/redoc" if settings.is_debug else None,
    openapi_url="/openapi.json" if settings.is_debug else None,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)


# Exceptions
setup_exception_handlers(app)


# Routers
app.include_router(auth_router)
app.include_router(users_router)


# Root
@app.get("/")
def root() -> dict[str, str]:
    return {"name": app.title, "description": app.description, "version": app.version}
