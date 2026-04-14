from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.clients.data_service_client import (
    DataServiceClient,
    DataServiceSearchResponse,
)
from services.user_service.app.core.config import settings
from services.user_service.app.models.regression_run import RegressionRun
from services.user_service.app.models.regression_run_candidate import (
    RegressionRunCandidate,
)
from services.user_service.app.repositories.project_repository import (
    ProjectRepository,
)
from services.user_service.app.repositories.regression_run_candidate_repository import (
    RegressionRunCandidateRepository,
)
from services.user_service.app.repositories.regression_run_repository import (
    RegressionRunRepository,
)
from services.user_service.app.schemas.regression_run import (
    RegressionRunCreate,
    RegressionRunDetailRead,
)


class RegressionRunService:
    """
    Service-слой для запусков анализа регресса.

    На Этапе 3 user_service уже умеет:
    - проверить, что проект существует;
    - сходить в data_service;
    - получить кандидатов по change_summary;
    - сохранить запуск;
    - сохранить найденных кандидатов отдельными строками в БД.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.project_repository = ProjectRepository(session)
        self.regression_run_repository = RegressionRunRepository(session)
        self.regression_run_candidate_repository = RegressionRunCandidateRepository(
            session
        )
        self.data_service_client = DataServiceClient(
            base_url=settings.data_service_base_url
        )

    async def create_run(
        self,
        project_id: int,
        payload: RegressionRunCreate,
    ) -> RegressionRunDetailRead:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )

        # Сначала получаем кандидатов от data_service.
        search_response = await self.data_service_client.search_test_cases(
            project_id=project_id,
            query=payload.change_summary,
            limit=payload.candidate_limit,
        )

        result_summary = self._build_result_summary(search_response)
        candidates_payload = self._build_candidates_payload(search_response)

        try:
            run = await self.regression_run_repository.create(
                project_id=project_id,
                change_summary=payload.change_summary,
                status="completed",
                result_summary=result_summary,
            )

            await self.regression_run_candidate_repository.create_many(
                regression_run_id=run.id,
                candidates_payload=candidates_payload,
            )

            await self.session.commit()
            await self.session.refresh(run)

        except Exception:
            await self.session.rollback()
            raise

        saved_candidates = await self.regression_run_candidate_repository.list_by_run_id(
            run.id
        )
        return self._to_detail_response(run, saved_candidates)

    async def list_runs(self, project_id: int) -> list[RegressionRun]:
        project = await self.project_repository.get_by_id(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id={project_id} not found.",
            )

        return await self.regression_run_repository.list_by_project_id(project_id)

    async def get_run(self, run_id: int) -> RegressionRunDetailRead:
        run = await self.regression_run_repository.get_by_id(run_id)
        if run is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Regression run with id={run_id} not found.",
            )

        candidates = await self.regression_run_candidate_repository.list_by_run_id(
            run.id
        )
        return self._to_detail_response(run, candidates)

    def _build_candidates_payload(
        self,
        search_response: DataServiceSearchResponse,
    ) -> list[dict]:
        payload: list[dict] = []

        for candidate in search_response.candidates:
            payload.append(
                {
                    "source_test_case_id": candidate.test_case.id,
                    "title": candidate.test_case.title,
                    "relevance_score": candidate.relevance_score,
                    "matched_terms": candidate.matched_terms,
                }
            )

        return payload

    def _to_detail_response(
        self,
        run: RegressionRun,
        candidates: list[RegressionRunCandidate],
    ) -> RegressionRunDetailRead:
        return RegressionRunDetailRead(
            id=run.id,
            project_id=run.project_id,
            change_summary=run.change_summary,
            status=run.status,
            result_summary=run.result_summary,
            created_at=run.created_at,
            candidates=[candidate for candidate in candidates],
        )

    def _build_result_summary(
        self,
        search_response: DataServiceSearchResponse,
    ) -> str:
        """
        Оставляем result_summary как краткое человекочитаемое summary,
        но теперь полный результат лежит еще и в отдельной таблице.
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
            matched_terms = (
                ", ".join(candidate.matched_terms)
                if candidate.matched_terms
                else "—"
            )
            lines.append(
                f"{index}. test_case_id={candidate.test_case.id}, "
                f"title='{candidate.test_case.title}', "
                f"score={candidate.relevance_score}, "
                f"matched_terms=[{matched_terms}]"
            )

        return "\n".join(lines)