from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.models.test_case_embedding import TestCaseEmbedding


class TestCaseEmbeddingRepository:
    """
    Repository для таблицы test_case_embeddings.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_test_case_id(
        self,
        test_case_id: int,
    ) -> TestCaseEmbedding | None:
        result = await self.session.execute(
            select(TestCaseEmbedding).where(
                TestCaseEmbedding.test_case_id == test_case_id
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        test_case_id: int,
        embedding: list[float],
        embedding_provider: str,
        embedding_model: str,
    ) -> TestCaseEmbedding:
        entity = await self.get_by_test_case_id(test_case_id)

        if entity is None:
            entity = TestCaseEmbedding(
                test_case_id=test_case_id,
                embedding=embedding,
                embedding_provider=embedding_provider,
                embedding_model=embedding_model,
            )
            self.session.add(entity)
        else:
            entity.embedding = embedding
            entity.embedding_provider = embedding_provider
            entity.embedding_model = embedding_model

        await self.session.flush()
        return entity