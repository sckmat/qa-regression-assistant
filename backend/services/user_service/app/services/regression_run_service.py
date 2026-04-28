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
from services.user_service.app.repositories.user_preference_repository import (
    UserPreferenceRepository,
)
from services.user_service.app.schemas.regression_run import (
    RegressionRunCreate,
    RegressionRunDetailRead,
)
from services.user_service.app.schemas.retrieval_candidate import RetrievalCandidate
from services.user_service.app.services.capabilities_service import CapabilitiesService


class RegressionRunService:
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
        user_id: int,
    ) -> RegressionRunDetailRead:
        project = await self._ensure_project_access(project_id, user_id)

        candidates = await self._get_candidates(
            project=project,
            query=payload.change_summary,
            limit=payload.candidate_limit,
            search_mode=payload.search_mode,
        )

        result_summary = self._build_result_summary(
            candidates=candidates,
            search_mode=payload.search_mode,
        )

        candidates_payload = self._build_candidates_payload(candidates)

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

        saved_candidates = await self.regression_run_candidate_repository.list_by_run_id(
            run.id
        )

        return self._to_detail_response(run, saved_candidates)

    async def list_runs(
        self,
        project_id: int,
        user_id: int,
    ) -> list[RegressionRun]:
        await self._ensure_project_access(project_id, user_id)

        return await self.regression_run_repository.list_by_project_id(project_id)

    async def get_run(
        self,
        run_id: int,
        user_id: int,
    ) -> RegressionRunDetailRead:
        run = await self.regression_run_repository.get_by_id(run_id)

        if run is None:
            raise HTTPException(404, "Run not found")

        # 🔥 ВАЖНО: проверка через проект
        await self._ensure_project_access(run.project_id, user_id)

        candidates = await self.regression_run_candidate_repository.list_by_run_id(
            run.id
        )

        return self._to_detail_response(run, candidates)

    async def _ensure_project_access(self, project_id: int, user_id: int):
        project = await self.project_repository.get_by_id(project_id)

        if project is None:
            raise HTTPException(404, "Project not found")

        if project.owner_user_id != user_id:
            raise HTTPException(403, "Access denied")

        return project


    async def _get_candidates(
        self,
        project,
        query: str,
        limit: int,
        search_mode: str,
    ) -> list[RetrievalCandidate]:

        if search_mode == "lexical":
            return await self.data_service_client.search_test_cases(
                project_id=project.id,
                query=query,
                limit=limit,
            )

        if search_mode == "semantic":
            return await self.data_service_client.semantic_search_test_cases(
                project_id=project.id,
                query=query,
                limit=limit,
            )

        if search_mode == "semantic_llm":
            semantic_candidates = await self.data_service_client.semantic_search_test_cases(
                project_id=project.id,
                query=query,
                limit=limit,
            )

            if not semantic_candidates:
                return []

            pref_repo = UserPreferenceRepository(self.session)
            pref = await pref_repo.get_or_create(project.owner_user_id)

            capabilities = CapabilitiesService().get_capabilities()

            enabled_map = {
                p["code"]: p["enabled"] for p in capabilities["llm_providers"]
            }

            preferred = pref.preferred_llm_provider

            if not enabled_map.get(preferred):
                provider = capabilities["default_llm_provider"]
            else:
                provider = preferred

            return await self.llm_service_client.rerank_candidates(
                change_summary=query,
                candidates=semantic_candidates,
                top_n=limit,
                provider=provider,
            )

        raise HTTPException(400, f"Unsupported search_mode: {search_mode}")

    def _build_candidates_payload(self, candidates):
        return [
            {
                "source_test_case_id": c.source_test_case_id,
                "title": c.title,
                "relevance_score": c.normalized_score,
                "matched_terms": c.matched_terms,
                "explanation": c.explanation,
            }
            for c in candidates
        ]

    def _to_detail_response(self, run, candidates):
        return RegressionRunDetailRead(
            id=run.id,
            project_id=run.project_id,
            change_summary=run.change_summary,
            status=run.status,
            result_summary=run.result_summary,
            created_at=run.created_at,
            candidates=[c for c in candidates],
        )

    def _build_result_summary(self, candidates, search_mode):
        if not candidates:
            return "Анализ завершен. Подходящие тест-кейсы не найдены."

        return f"Найдено {len(candidates)} тест-кейсов."