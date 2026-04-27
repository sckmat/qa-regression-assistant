from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.db import get_db_session
from services.user_service.app.schemas.project import ProjectCreate, ProjectRead
from services.user_service.app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("", response_model=ProjectRead, status_code=201)
async def create_project(
    payload: ProjectCreate,
    session: DbSession,
) -> ProjectRead:
    """
    Создает новый проект.
    """
    service = ProjectService(session)
    project = await service.create_project(payload)
    return ProjectRead.model_validate(project)


@router.get("", response_model=list[ProjectRead])
async def list_projects(session: DbSession) -> list[ProjectRead]:
    """
    Возвращает список всех проектов.
    """
    service = ProjectService(session)
    projects = await service.list_projects()
    return [ProjectRead.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, session: DbSession) -> ProjectRead:
    """
    Возвращает один проект по его id.
    """
    service = ProjectService(session)
    project = await service.get_project(project_id)
    return ProjectRead.model_validate(project)

@router.delete("/{project_id}", status_code=204,)
async def delete_project(project_id: int, session: DbSession,) -> Response:
    service = ProjectService(session)
    await service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)