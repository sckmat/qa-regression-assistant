from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.project import Project
from services.user_service.app.repositories.project_repository import (
    ProjectRepository,
)
from services.user_service.app.schemas.project import ProjectCreate
from services.user_service.app.clients.data_service_client import DataServiceClient
from services.user_service.app.core.config import settings

class ProjectService:
    """
    Service-слой для проектов.

    Здесь находится бизнес-логика, например:
    - проверка уникальности названия;
    - интерпретация ошибок на языке API.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.project_repository = ProjectRepository(session)
        self.data_service_client = DataServiceClient(
            base_url=settings.data_service_base_url
        )

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

    async def delete_project(self, project_id: int) -> None:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )

        try:
            await self.data_service_client.delete_project_data(project_id)
            await self.project_repository.delete(project)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
