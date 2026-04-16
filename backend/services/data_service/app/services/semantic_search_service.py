from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.core.config import settings
from services.data_service.app.models.test_case import TestCase
from services.data_service.app.models.test_case_embedding import TestCaseEmbedding
from services.data_service.app.schemas.semantic_search import (
    SemanticSearchCandidateRead,
    SemanticSearchRequest,
    SemanticSearchResponse,
    SemanticSearchTestCaseRead,
)
from services.data_service.app.services.embedding_service import EmbeddingService


class SemanticSearchService:
    """
    Сервис semantic search по embeddings.

    Логика:
    1. Получаем embedding для query
    2. Делаем nearest-neighbor search по cosine distance
    3. Возвращаем top-k похожих test cases
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_service = EmbeddingService()

    async def semantic_search(
        self,
        project_id: int,
        payload: SemanticSearchRequest,
    ) -> SemanticSearchResponse:
        query_embedding = await self._embed_query(payload.query)

        # pgvector-python для SQLAlchemy позволяет использовать:
        # TestCaseEmbedding.embedding.cosine_distance(query_embedding)
        distance_expr = TestCaseEmbedding.embedding.cosine_distance(query_embedding).label(
            "cosine_distance"
        )

        stmt = (
            select(TestCase, distance_expr)
            .join(
                TestCaseEmbedding,
                TestCaseEmbedding.test_case_id == TestCase.id,
            )
            .where(TestCase.project_id == project_id)
            .order_by(distance_expr.asc(), TestCase.id.asc())
            .limit(payload.limit)
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        candidates: list[SemanticSearchCandidateRead] = []

        for test_case, cosine_distance in rows:
            # Для cosine distance более похожие объекты имеют меньшую дистанцию.
            # Для удобства клиента дополнительно отдаем similarity_score:
            # similarity_score = 1 - cosine_distance
            similarity_score = max(0.0, 1.0 - float(cosine_distance))

            candidates.append(
                SemanticSearchCandidateRead(
                    test_case=SemanticSearchTestCaseRead(
                        id=test_case.id,
                        project_id=test_case.project_id,
                        title=test_case.title,
                        raw_text=test_case.raw_text,
                    ),
                    cosine_distance=float(cosine_distance),
                    similarity_score=similarity_score,
                )
            )

        return SemanticSearchResponse(
            project_id=project_id,
            query=payload.query,
            embedding_provider=settings.embedding_provider,
            embedding_model=settings.embedding_model,
            candidates=candidates,
        )

    async def _embed_query(self, query: str) -> list[float]:
        embeddings = await self.embedding_service.embed_texts([query])
        if not embeddings:
            raise ValueError("Embedding provider returned empty embeddings list for query")
        return embeddings[0]