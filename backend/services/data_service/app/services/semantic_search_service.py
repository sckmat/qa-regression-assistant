from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.core.config import settings
from services.data_service.app.schemas.semantic_search import (
    SemanticSearchRequest,
    SemanticSearchResponse,
    SemanticSearchCandidateRead,
    SemanticSearchTestCaseRead,
)
from services.data_service.app.services.embedding_service import EmbeddingService


class SemanticSearchService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embedding_service = EmbeddingService()

    async def semantic_search(
        self,
        project_id: int,
        payload: SemanticSearchRequest,
    ) -> SemanticSearchResponse:

        provider = payload.embedding_provider or settings.default_embedding_provider

        if provider == "ollama":
            model = settings.ollama_embedding_model
        else:
            model = settings.openai_embedding_model

        query_embedding = (
            await self.embedding_service.embed_texts(
                [payload.query],
                provider_name=provider,
            )
        )[0]

        # 🔥 КЛЮЧЕВОЕ: конвертация list -> vector string
        embedding_str = f"[{','.join(map(str, query_embedding))}]"

        schema = settings.data_service_db_schema

        stmt = text(
            f"""
            SELECT
                tc.id,
                tc.project_id,
                tc.title,
                tc.raw_text,
                1 - (tce.embedding <=> CAST(:query_embedding AS vector)) AS similarity_score,
                (tce.embedding <=> CAST(:query_embedding AS vector)) AS cosine_distance
            FROM {schema}.test_case_embeddings tce
            JOIN {schema}.test_cases tc ON tc.id = tce.test_case_id
            WHERE tc.project_id = :project_id
            ORDER BY tce.embedding <=> CAST(:query_embedding AS vector)
            LIMIT :limit
            """
        )

        result = await self.session.execute(
            stmt,
            {
                "query_embedding": embedding_str,  # 🔥 теперь строка!
                "project_id": project_id,
                "limit": payload.limit,
            },
        )

        rows = result.fetchall()

        candidates = [
            SemanticSearchCandidateRead(
                test_case=SemanticSearchTestCaseRead(
                    id=row.id,
                    project_id=row.project_id,
                    title=row.title,
                    raw_text=row.raw_text,
                ),
                cosine_distance=row.cosine_distance,
                similarity_score=row.similarity_score,
            )
            for row in rows
        ]

        return SemanticSearchResponse(
            project_id=project_id,
            query=payload.query,
            embedding_provider=provider,
            embedding_model=model,
            candidates=candidates,
        )