from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.project import Project


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.flush()
        return project

    async def list_by_user(self, user_id: int) -> list[Project]:
        result = await self.session.execute(
            select(Project).where(Project.owner_user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, project_id: int) -> Project | None:
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, project: Project) -> None:
        await self.session.delete(project)
        await self.session.flush()