from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.project import Project


class ProjectRepository:
    """
    Repository-слой для таблицы projects.

    Важно:
    repository не содержит бизнес-логики.
    Его задача — только работа с БД.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, description: str | None) -> Project:
        project = Project(name=name, description=description)
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def get_all(self) -> list[Project]:
        result = await self.session.execute(
            select(Project).order_by(Project.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, project_id: int) -> Project | None:
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Project | None:
        result = await self.session.execute(
            select(Project).where(Project.name == name)
        )
        return result.scalar_one_or_none()

    async def delete(self, project) -> None:
        await self.session.delete(project)
        await self.session.flush()
