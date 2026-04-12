from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.project import Project
from services.user_service.app.repositories.project_repository import (
    ProjectRepository,
)
from services.user_service.app.schemas.project import ProjectCreate


class ProjectService:
    """
    Service-слой для проектов.

    Здесь находится бизнес-логика, например:
    - проверка уникальности названия;
    - интерпретация ошибок на языке API.
    """

    def __init__(self, session: AsyncSession):
        self.project_repository = ProjectRepository(session)

    async def create_project(self, payload: ProjectCreate) -> Project:
        existing_project = await self.project_repository.get_by_name(payload.name)
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Project with name '{payload.name}' already exists.",
            )

        return await self.project_repository.create(
            name=payload.name,
            description=payload.description,
        )

    async def list_projects(self) -> list[Project]:
        return await self.project_repository.get_all()

    async def get_project(self, project_id: int) -> Project:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )
        return project
