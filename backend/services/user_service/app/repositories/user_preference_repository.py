from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.user_preference import UserPreference


class UserPreferenceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, user_id: int) -> UserPreference:
        result = await self.session.execute(
            select(UserPreference).where(UserPreference.user_id == user_id)
        )
        pref = result.scalar_one_or_none()

        if pref:
            return pref

        pref = UserPreference(user_id=user_id)
        self.session.add(pref)
        await self.session.flush()

        return pref

    async def update(self, pref: UserPreference) -> UserPreference:
        await self.session.flush()
        return pref