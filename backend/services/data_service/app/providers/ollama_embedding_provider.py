import httpx

from services.data_service.app.providers.embedding_provider import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    """
    Провайдер embeddings через Ollama.
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

    async def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings: list[list[float]] = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            for text in texts:
                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json={
                        "model": self.model,
                        "prompt": text,
                    },
                )

                if response.is_error:
                    raise RuntimeError(
                        f"Ollama embedding error: status={response.status_code}, body={response.text}"
                    )

                data = response.json()

                vector = data.get("embedding")

                if not vector:
                    raise ValueError(f"Invalid Ollama response: {data}")

                embeddings.append(vector)

        return embeddings