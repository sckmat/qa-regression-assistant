from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.api.dependencies.current_user import get_current_user
from services.user_service.app.core.db import get_db_session
from services.user_service.app.models.user import User
from services.user_service.app.schemas.project import ProjectCreate, ProjectRead
from services.user_service.app.services.project_service import ProjectService

router = APIRouter(tags=["Projects"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    "/projects",
    response_model=ProjectRead,
    status_code=201,
)
async def create_project(
    payload: ProjectCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> ProjectRead:
    service = ProjectService(session)

    project = await service.create_project(
        payload=payload,
        user_id=current_user.id,
    )

    return ProjectRead.model_validate(project)


@router.get(
    "/projects",
    response_model=list[ProjectRead],
)
async def list_projects(
    current_user: CurrentUser,
    session: DbSession,
) -> list[ProjectRead]:
    service = ProjectService(session)

    projects = await service.list_projects(current_user.id)

    return [ProjectRead.model_validate(p) for p in projects]


@router.get(
    "/projects/{project_id}",
    response_model=ProjectRead,
)
async def get_project(
    project_id: int,
    current_user: CurrentUser,
    session: DbSession,
) -> ProjectRead:
    service = ProjectService(session)

    project = await service.get_project(project_id, current_user.id)

    return ProjectRead.model_validate(project)


@router.delete(
    "/projects/{project_id}",
    status_code=204,
)
async def delete_project(
    project_id: int,
    current_user: CurrentUser,
    session: DbSession,
) -> Response:
    service = ProjectService(session)

    await service.delete_project(project_id, current_user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)