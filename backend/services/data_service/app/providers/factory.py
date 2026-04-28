from services.data_service.app.core.config import settings
from services.data_service.app.providers.ollama_embedding_provider import (
    OllamaEmbeddingProvider,
)
from services.data_service.app.providers.openai_embedding_provider import (
    OpenAIEmbeddingProvider,
)


def build_embedding_provider(provider_name: str | None = None):
    provider = (provider_name or settings.default_embedding_provider).lower()

    if provider == "ollama":
        return OllamaEmbeddingProvider(
            base_url=settings.ollama_embedding_base_url,
            model=settings.ollama_embedding_model,
            dimensions=settings.embedding_dim,
        )

    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")

        return OpenAIEmbeddingProvider(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            model=settings.openai_embedding_model,
            dimensions=settings.embedding_dim,
        )

    raise ValueError(f"Unsupported embedding provider: {provider}")