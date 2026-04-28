from services.llm_service.app.core.config import settings
from services.llm_service.app.providers.openai_compatible_provider import (
    OpenAICompatibleProvider,
)


def build_llm_provider(provider_name: str):
    if provider_name == "ollama":
        return OpenAICompatibleProvider(
            base_url=settings.ollama_llm_base_url,
            model=settings.ollama_llm_model,
            timeout_seconds=settings.llm_timeout_seconds,
        )

    return OpenAICompatibleProvider(
        base_url=settings.openai_base_url,
        model=settings.openai_llm_model,
        timeout_seconds=settings.llm_timeout_seconds,
        api_key=settings.openai_api_key,
    )