from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.core.config import settings
from services.data_service.app.models.test_case import TestCase
from services.data_service.app.repositories.test_case_embedding_repository import (
    TestCaseEmbeddingRepository,
)
from services.data_service.app.schemas.reindex import ProjectReindexResponse
from services.data_service.app.services.embedding_service import EmbeddingService


class IndexingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_service = EmbeddingService()
        self.embedding_repository = TestCaseEmbeddingRepository(session)

    async def reindex_project(self, project_id: int, payload) -> ProjectReindexResponse:

        result = await self.session.execute(
            select(TestCase)
            .where(TestCase.project_id == project_id)
            .order_by(TestCase.id.asc())
        )
        test_cases = list(result.scalars().all())

        provider = payload.embedding_provider or settings.default_embedding_provider

        if provider == "ollama":
            model = settings.ollama_embedding_model
        else:
            model = settings.openai_embedding_model

        if not test_cases:
            return ProjectReindexResponse(
                project_id=project_id,
                embedding_provider=provider,
                embedding_model=model,
                embedding_dim=settings.embedding_dim,
                processed_test_cases=0,
                indexed_test_cases=0,
                status="completed",
            )

        indexed_count = 0

        try:
            for batch in self._batched(test_cases, settings.embedding_batch_size):
                batch_texts = [
                    self._build_embedding_text(test_case) for test_case in batch
                ]

                embeddings = await self.embedding_service.embed_texts(
                    batch_texts,
                    provider_name=provider,  # 🔥
                )

                for test_case, embedding in zip(batch, embeddings):
                    await self.embedding_repository.upsert(
                        test_case_id=test_case.id,
                        embedding=embedding,
                        embedding_provider=provider,
                        embedding_model=model,
                    )
                    indexed_count += 1

            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise

        return ProjectReindexResponse(
            project_id=project_id,
            embedding_provider=provider,
            embedding_model=model,
            embedding_dim=settings.embedding_dim,
            processed_test_cases=len(test_cases),
            indexed_test_cases=indexed_count,
            status="completed",
        )

    def _build_embedding_text(self, test_case: TestCase) -> str:
        if test_case.raw_text and test_case.raw_text.strip():
            return test_case.raw_text.strip()

        parts = [
            test_case.title or "",
            test_case.preconditions or "",
            test_case.steps or "",
            test_case.expected_result or "",
        ]
        return "\n".join(part for part in parts if part).strip()

    def _batched(self, items: list[TestCase], batch_size: int):
        return [
            items[i : i + batch_size]
            for i in range(0, len(items), batch_size)
        ]