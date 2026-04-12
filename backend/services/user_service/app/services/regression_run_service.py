from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.regression_run import RegressionRun
from services.user_service.app.repositories.project_repository import (
    ProjectRepository,
)
from services.user_service.app.repositories.regression_run_repository import (
    RegressionRunRepository,
)
from services.user_service.app.schemas.regression_run import RegressionRunCreate


class RegressionRunService:
    """
    Service-слой для запусков анализа регресса.

    На текущем этапе здесь только базовая логика:
    - проверить, что проект существует;
    - создать запись о запуске;
    - вернуть пользователю результат.

    Позже именно сюда удобно добавить orchestration:
    - вызов data_service;
    - вызов llm_service;
    - сохранение результатов анализа.
    """

    def __init__(self, session: AsyncSession):
        self.project_repository = ProjectRepository(session)
        self.regression_run_repository = RegressionRunRepository(session)

    async def create_run(
        self,
        project_id: int,
        payload: RegressionRunCreate,
    ) -> RegressionRun:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )

        return await self.regression_run_repository.create(
            project_id=project_id,
            change_summary=payload.change_summary,
            status="created",
            result_summary="Run created. Data Service and LLM Service are not connected yet.",
        )

    async def list_runs(self, project_id: int) -> list[RegressionRun]:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )

        return await self.regression_run_repository.list_by_project_id(project_id)

    async def get_run(self, run_id: int) -> RegressionRun:
        run = await self.regression_run_repository.get_by_id(run_id)
        if run is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Regression run with id={run_id} not found.",
            )
        return run
