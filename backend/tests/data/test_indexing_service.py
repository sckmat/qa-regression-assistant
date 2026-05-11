import pytest

from services.data_service.app.services.indexing_service import IndexingService


class FakeEmbeddingService:
    async def embed_texts(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeRepo:
    async def upsert(self, **kwargs):
        return None


@pytest.mark.asyncio
async def test_build_embedding_text():
    service = IndexingService(session=None)

    class TC:
        title = "Title"
        preconditions = "Pre"
        steps = "Steps"
        expected_result = "Result"
        raw_text = None

    text = service._build_embedding_text(TC())

    assert "Title" in text
    assert "Steps" in text


def test_batched():
    service = IndexingService(session=None)

    result = service._batched([1, 2, 3], 2)

    assert len(result) == 2