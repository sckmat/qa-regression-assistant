from services.data_service.app.core.config import settings
from services.data_service.app.providers.factory import build_embedding_provider


class EmbeddingService:
    """
    Тонкая обертка над провайдером embeddings.
    """

    def __init__(self):
        self.provider = build_embedding_provider(settings)

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return await self.provider.embed_texts(texts)