from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.api.dependencies.current_user import get_current_user
from services.user_service.app.core.db import get_db_session
from services.user_service.app.models.user import User
from services.user_service.app.repositories.user_preference_repository import (
    UserPreferenceRepository,
)
from services.user_service.app.schemas.user_preference import (
    UserPreferenceRead,
    UserPreferenceUpdate,
)
from services.user_service.app.services.capabilities_service import CapabilitiesService

router = APIRouter(tags=["User Preferences"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/me/preferences", response_model=UserPreferenceRead)
async def get_preferences(
    current_user: CurrentUser,
    session: DbSession,
):
    repo = UserPreferenceRepository(session)
    pref = await repo.get_or_create(current_user.id)
    return UserPreferenceRead.model_validate(pref)


@router.patch("/me/preferences", response_model=UserPreferenceRead)
async def update_preferences(
    payload: UserPreferenceUpdate,
    current_user: CurrentUser,
    session: DbSession,
):
    repo = UserPreferenceRepository(session)
    pref = await repo.get_or_create(current_user.id)

    if payload.default_search_mode:
        pref.default_search_mode = payload.default_search_mode

    if payload.preferred_llm_provider:
        pref.preferred_llm_provider = payload.preferred_llm_provider

    await repo.update(pref)
    await session.commit()

    return UserPreferenceRead.model_validate(pref)


@router.get("/app/capabilities")
async def get_capabilities():
    service = CapabilitiesService()
    return service.get_capabilities()