import httpx

from services.data_service.app.providers.embedding_provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    Провайдер embeddings через OpenAI API.

    Использует:
    POST {OPENAI_BASE_URL}/v1/embeddings
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        dimensions: int,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        payload = {
            "model": self.model,
            "input": texts,
            "encoding_format": "float",
            "dimensions": self.dimensions,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
            response = await client.post(
                f"{self.base_url}/v1/embeddings",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        data = response.json()
        items = data.get("data", [])
        embeddings = [item["embedding"] for item in items]

        if len(embeddings) != len(texts):
            raise ValueError(
                "OpenAI returned unexpected number of embeddings: "
                f"expected={len(texts)}, actual={len(embeddings)}"
            )

        for embedding in embeddings:
            if len(embedding) != self.dimensions:
                raise ValueError(
                    "OpenAI returned embedding with unexpected dimension: "
                    f"expected={self.dimensions}, actual={len(embedding)}"
                )

        return embeddings