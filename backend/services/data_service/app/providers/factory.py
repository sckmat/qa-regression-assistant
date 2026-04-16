from services.data_service.app.core.config import DataServiceSettings
from services.data_service.app.providers.embedding_provider import EmbeddingProvider
from services.data_service.app.providers.ollama_embedding_provider import (
    OllamaEmbeddingProvider,
)
from services.data_service.app.providers.openai_embedding_provider import (
    OpenAIEmbeddingProvider,
)


def build_embedding_provider(settings: DataServiceSettings) -> EmbeddingProvider:
    provider = settings.embedding_provider.lower().strip()

    if provider == "ollama":
        return OllamaEmbeddingProvider(
            base_url=settings.ollama_base_url,
            model=settings.embedding_model,
            dimensions=settings.embedding_dim,
        )

    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai"
            )

        return OpenAIEmbeddingProvider(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
            dimensions=settings.embedding_dim,
        )

    raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")