from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.db import get_db_session
from services.user_service.app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserRead,
)
from services.user_service.app.services.auth_service import AuthService
from services.user_service.app.api.dependencies.current_user import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_db_session)):
    service = AuthService(session)
    user = await service.register(payload.email, payload.password, payload.full_name)
    return UserRead.model_validate(user)


@router.post("/login", response_model=UserRead)
async def login(payload: LoginRequest, response: Response, session: AsyncSession = Depends(get_db_session)):
    service = AuthService(session)
    user, access_token, refresh_token = await service.login(
        payload.email, payload.password
    )

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return UserRead.model_validate(user)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "ok"}


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return UserRead.model_validate(current_user)