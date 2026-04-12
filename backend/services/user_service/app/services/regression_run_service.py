from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.clients.data_service_client import (
    DataServiceClient,
    DataServiceSearchResponse,
)
from services.user_service.app.core.config import settings
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

    На этом этапе user_service уже умеет:
    - проверить, что проект существует;
    - сходить в data_service;
    - получить кандидатов по change_summary;
    - сохранить результат запуска у себя в БД.
    """

    def __init__(self, session: AsyncSession):
        self.project_repository = ProjectRepository(session)
        self.regression_run_repository = RegressionRunRepository(session)
        self.data_service_client = DataServiceClient(
            base_url=settings.data_service_base_url
        )

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

        # Шаг 1. Запрашиваем кандидатов у data_service.
        search_response = await self.data_service_client.search_test_cases(
            project_id=project_id,
            query=payload.change_summary,
            limit=payload.candidate_limit,
        )

        # Шаг 2. Собираем краткий summary, который сохраняем в БД.
        result_summary = self._build_result_summary(search_response)

        # Шаг 3. Сохраняем сам запуск уже как completed.
        return await self.regression_run_repository.create(
            project_id=project_id,
            change_summary=payload.change_summary,
            status="completed",
            result_summary=result_summary,
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

    def _build_result_summary(
        self,
        search_response: DataServiceSearchResponse,
    ) -> str:
        """
        Пока не сохраняем кандидатов в отдельную таблицу.
        На этом этапе делаем простой, но полезный вариант:
        складываем краткий человекочитаемый summary в result_summary.
        """

        if not search_response.candidates:
            return (
                "Data Service connected successfully. "
                "No candidate test cases were found for the provided change summary."
            )

        lines = [
            "Data Service connected successfully.",
            f"Found candidates: {len(search_response.candidates)}.",
            "Top matches:",
        ]

        for index, candidate in enumerate(search_response.candidates, start=1):
            matched_terms = ", ".join(candidate.matched_terms) if candidate.matched_terms else "—"
            lines.append(
                f"{index}. test_case_id={candidate.test_case.id}, "
                f"title='{candidate.test_case.title}', "
                f"score={candidate.relevance_score}, "
                f"matched_terms=[{matched_terms}]"
            )

        return "\n".join(lines)