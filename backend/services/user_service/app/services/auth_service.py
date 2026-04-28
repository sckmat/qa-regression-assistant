from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from services.user_service.app.models.user import User
from services.user_service.app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)

    async def register(self, email: str, password: str, full_name: str) -> User:
        existing = await self.user_repository.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
        )

        await self.user_repository.create(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def login(self, email: str, password: str) -> tuple[User, str, str]:
        user = await self.user_repository.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token({"sub": str(user.id)})

        return user, access_token

    async def refresh(self, refresh_token: str) -> str:
        payload = self._decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise Exception("Invalid token")

        user_id = payload.get("sub")

        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        return self._create_access_token(user.id)