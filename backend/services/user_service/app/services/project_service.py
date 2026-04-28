from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.clients.data_service_client import DataServiceClient
from services.user_service.app.core.config import settings
from services.user_service.app.models.project import Project
from services.user_service.app.repositories.project_repository import ProjectRepository
from services.user_service.app.schemas.project import ProjectCreate


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.project_repository = ProjectRepository(session)
        self.data_service_client = DataServiceClient(
            base_url=settings.data_service_base_url
        )

    async def create_project(self, payload: ProjectCreate, user_id: int) -> Project:
        project = Project(
            name=payload.name,
            description=payload.description,
            owner_user_id=user_id,
        )

        await self.project_repository.create(project)
        await self.session.commit()
        await self.session.refresh(project)

        return project

    async def list_projects(self, user_id: int) -> list[Project]:
        return await self.project_repository.list_by_user(user_id)

    async def get_project(self, project_id: int, user_id: int) -> Project:
        return await self._ensure_project_access(project_id, user_id)

    async def delete_project(self, project_id: int, user_id: int) -> None:
        project = await self._ensure_project_access(project_id, user_id)

        try:
            await self.data_service_client.delete_project_data(project_id)
            await self.project_repository.delete(project)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def _ensure_project_access(self, project_id: int, user_id: int) -> Project:
        project = await self.project_repository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        if project.owner_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        return project