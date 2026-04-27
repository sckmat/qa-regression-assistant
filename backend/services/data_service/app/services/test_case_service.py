from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.models.test_case import TestCase
from services.data_service.app.repositories.test_case_repository import TestCaseRepository
from services.data_service.app.schemas.test_case import (
    TestCaseImportItem,
    TestCaseImportRequest,
    TestCaseSearchResponse,
    TestCaseSearchResult,
)
from services.data_service.app.services.text_processing_service import TextProcessingService
from services.data_service.app.repositories.test_case_repository import (
    TestCaseRepository,
)
from services.data_service.app.repositories.test_case_embedding_repository import (
    TestCaseEmbeddingRepository,
)


class TestCaseService:
    """
    Сервисный слой data_service.

    Здесь находится прикладная логика:
    - сбор raw_text;
    - пакетный импорт тест-кейсов;
    - поиск и простое ранжирование кандидатов.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = TestCaseRepository(session)
        self.text_processing = TextProcessingService()
        self.test_case_repository = TestCaseRepository(session)
        self.test_case_embedding_repository = TestCaseEmbeddingRepository(session)

    async def import_test_cases(
        self,
        project_id: int,
        payload: TestCaseImportRequest,
    ) -> list[TestCase]:
        entities: list[TestCase] = []

        for item in payload.items:
            raw_text = item.raw_text or self.text_processing.build_raw_text(
                title=item.title,
                preconditions=item.preconditions,
                steps=item.steps,
                expected_result=item.expected_result,
                tags=item.tags,
                priority=item.priority,
                external_id=item.external_id,
            )

            entities.append(
                TestCase(
                    project_id=project_id,
                    external_id=item.external_id,
                    title=item.title,
                    preconditions=item.preconditions,
                    steps=item.steps,
                    expected_result=item.expected_result,
                    tags=item.tags,
                    priority=item.priority,
                    raw_text=raw_text,
                )
            )

        return await self.repository.create_many(entities)

    async def list_test_cases(self, project_id: int) -> list[TestCase]:
        return await self.repository.get_all_by_project_id(project_id)

    async def get_test_case(self, test_case_id: int) -> TestCase:
        test_case = await self.repository.get_by_id(test_case_id)
        if not test_case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Test case with id={test_case_id} not found",
            )
        return test_case

    async def search_test_cases(
        self,
        project_id: int,
        query: str,
        limit: int,
    ) -> TestCaseSearchResponse:
        terms = self.text_processing.tokenize_query(query)
        candidates = await self.repository.search_candidates(
            project_id=project_id,
            terms=terms,
            max_candidates=max(50, limit * 5),
        )

        ranked = []
        normalized_query = self.text_processing.normalize_text(query)

        for candidate in candidates:
            normalized_title = self.text_processing.normalize_text(candidate.title)
            normalized_document = self.text_processing.normalize_text(candidate.raw_text)

            matched_terms: list[str] = []
            score = 0

            for term in terms:
                in_title = term in normalized_title
                in_document = term in normalized_document

                if in_title or in_document:
                    matched_terms.append(term)
                if in_document:
                    score += 1
                if in_title:
                    score += 2

            # Дополнительный бонус за полное вхождение всего запроса в текст.
            if normalized_query and normalized_query in normalized_document:
                score += 3

            if score > 0:
                ranked.append(
                    TestCaseSearchResult(
                        test_case=candidate,
                        relevance_score=score,
                        matched_terms=matched_terms,
                    )
                )

        ranked.sort(
            key=lambda item: (
                item.relevance_score,
                item.test_case.id,
            ),
            reverse=True,
        )

        return TestCaseSearchResponse(
            project_id=project_id,
            query=query,
            candidates=ranked[:limit],
        )

    async def delete_project_test_cases(self, project_id: int) -> dict:
        test_case_ids = await self.test_case_repository.list_ids_by_project_id(project_id)

        deleted_embeddings = await self.test_case_embedding_repository.delete_by_test_case_ids(
            test_case_ids
        )
        deleted_test_cases = await self.test_case_repository.delete_by_project_id(project_id)

        await self.session.commit()

        return {
            "project_id": project_id,
            "deleted_test_cases": deleted_test_cases,
            "deleted_embeddings": deleted_embeddings,
            "status": "completed",
        }