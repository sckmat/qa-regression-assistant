from services.data_service.app.providers.factory import build_embedding_provider


class EmbeddingService:
    """
    Динамический выбор embedding provider.
    """

    async def embed_texts(
        self,
        texts: list[str],
        provider_name: str | None = None,
    ) -> list[list[float]]:
        provider = build_embedding_provider(provider_name)

        print(f"[EMBEDDING] provider={provider_name}")

        return await provider.embed_texts(texts)