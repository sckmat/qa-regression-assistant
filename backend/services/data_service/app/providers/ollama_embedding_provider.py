import httpx

from services.data_service.app.providers.embedding_provider import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    """
    Провайдер embeddings через локальный Ollama.

    Использует:
    POST {OLLAMA_BASE_URL}/api/embed
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        dimensions: int,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.dimensions = dimensions

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        payload = {
            "model": self.model,
            "input": texts,
            "truncate": True,
            "dimensions": self.dimensions,
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
            response = await client.post(f"{self.base_url}/api/embed", json=payload)
            response.raise_for_status()

        data = response.json()
        embeddings = data.get("embeddings", [])

        if len(embeddings) != len(texts):
            raise ValueError(
                "Ollama returned unexpected number of embeddings: "
                f"expected={len(texts)}, actual={len(embeddings)}"
            )

        for embedding in embeddings:
            if len(embedding) != self.dimensions:
                raise ValueError(
                    "Ollama returned embedding with unexpected dimension: "
                    f"expected={self.dimensions}, actual={len(embedding)}"
                )

        return embeddings