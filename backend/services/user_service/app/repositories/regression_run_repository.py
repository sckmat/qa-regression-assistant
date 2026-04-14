from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.regression_run import RegressionRun


class RegressionRunRepository:
    """
    Repository-слой для таблицы regression_runs.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        project_id: int,
        change_summary: str,
        status: str = "created",
        result_summary: str | None = None,
    ) -> RegressionRun:
        """
        Создает запуск анализа, но не коммитит транзакцию сразу.

        мы хотим в рамках одной транзакции сохранить и сам run,
        и найденных кандидатов.
        """
        run = RegressionRun(
            project_id=project_id,
            change_summary=change_summary,
            status=status,
            result_summary=result_summary,
        )
        self.session.add(run)
        await self.session.flush()
        return run

    async def list_by_project_id(self, project_id: int) -> list[RegressionRun]:
        result = await self.session.execute(
            select(RegressionRun)
            .where(RegressionRun.project_id == project_id)
            .order_by(RegressionRun.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, run_id: int) -> RegressionRun | None:
        result = await self.session.execute(
            select(RegressionRun).where(RegressionRun.id == run_id)
        )
        return result.scalar_one_or_none()