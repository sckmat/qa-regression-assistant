from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.db import get_db_session
from services.user_service.app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserRead,
)
from services.user_service.app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_db_session),
):
    service = AuthService(session)

    user = await service.register(
        payload.email,
        payload.password,
        payload.full_name,
    )

    return UserRead.model_validate(user)


@router.post("/login")
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
):
    service = AuthService(session)

    user, access_token, _ = await service.login(
        payload.email,
        payload.password,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead.model_validate(user),
    }


@router.get("/me", response_model=UserRead)
async def me(
    current_user=Depends(
        __import__("services.user_service.app.api.dependencies.current_user", fromlist=["get_current_user"]).get_current_user
    ),
):
    return UserRead.model_validate(current_user)