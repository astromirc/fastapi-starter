from typing import Any

from fastapi import APIRouter

from app.shared.dependencies import CurrentUser

from .models import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(current_user: CurrentUser) -> Any:
    return current_user
