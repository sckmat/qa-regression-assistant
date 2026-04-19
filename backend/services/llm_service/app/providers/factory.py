from services.llm_service.app.core.config import settings
from services.llm_service.app.providers.llm_provider import LLMProvider
from services.llm_service.app.providers.ollama_provider import OllamaProvider
from services.llm_service.app.providers.openai_provider import OpenAIProvider


def build_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower().strip()

    if provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_llm_base_url,
            model=settings.llm_model,
            timeout_seconds=settings.llm_timeout_seconds,
            api_key=None,
        )

    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai"
            )

        return OpenAIProvider(
            base_url=settings.openai_base_url,
            model=settings.llm_model,
            timeout_seconds=settings.llm_timeout_seconds,
            api_key=settings.openai_api_key,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")