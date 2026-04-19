from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.clients.data_service_client import DataServiceClient
from services.user_service.app.clients.llm_service_client import LLMServiceClient
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
from services.user_service.app.schemas.retrieval_candidate import RetrievalCandidate


class RegressionRunService:
    """
    Service-слой для запусков анализа регресса.

    Поддерживаемые режимы:
    - lexical
    - semantic
    - semantic_llm
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
        self.llm_service_client = LLMServiceClient(
            base_url=settings.llm_service_base_url
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

        candidates = await self._get_candidates(
            project_id=project_id,
            query=payload.change_summary,
            limit=payload.candidate_limit,
            search_mode=payload.search_mode,
        )

        result_summary = self._build_result_summary(
            candidates=candidates,
            search_mode=payload.search_mode,
        )
        candidates_payload = self._build_candidates_payload(candidates)

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

    async def _get_candidates(
        self,
        project_id: int,
        query: str,
        limit: int,
        search_mode: str,
    ) -> list[RetrievalCandidate]:
        if search_mode == "lexical":
            return await self.data_service_client.search_test_cases(
                project_id=project_id,
                query=query,
                limit=limit,
            )

        if search_mode == "semantic":
            return await self.data_service_client.semantic_search_test_cases(
                project_id=project_id,
                query=query,
                limit=limit,
            )

        if search_mode == "semantic_llm":
            semantic_candidates = await self.data_service_client.semantic_search_test_cases(
                project_id=project_id,
                query=query,
                limit=limit,
            )

            if not semantic_candidates:
                return []

            return await self.llm_service_client.rerank_candidates(
                change_summary=query,
                candidates=semantic_candidates,
                top_n=limit,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported search_mode: {search_mode}",
        )

    def _build_candidates_payload(
        self,
        candidates: list[RetrievalCandidate],
    ) -> list[dict]:
        payload: list[dict] = []

        for candidate in candidates:
            payload.append(
                {
                    "source_test_case_id": candidate.source_test_case_id,
                    "title": candidate.title,
                    "relevance_score": candidate.normalized_score,
                    "matched_terms": candidate.matched_terms,
                    "explanation": candidate.explanation,
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
        candidates: list[RetrievalCandidate],
        search_mode: str,
    ) -> str:
        if not candidates:
            return (
                f"Data Service connected successfully. Search mode: {search_mode}. "
                "No candidate test cases were found for the provided change summary."
            )

        lines = [
            "Data Service connected successfully.",
            f"Search mode: {search_mode}.",
            f"Found candidates: {len(candidates)}.",
            "Top matches:",
        ]

        for index, candidate in enumerate(candidates, start=1):
            matched_terms = ", ".join(candidate.matched_terms) if candidate.matched_terms else "—"
            explanation = candidate.explanation or "—"
            lines.append(
                f"{index}. test_case_id={candidate.source_test_case_id}, "
                f"title='{candidate.title}', "
                f"score={candidate.normalized_score}, "
                f"matched_terms=[{matched_terms}], "
                f"explanation='{explanation}'"
            )

        return "\n".join(lines)