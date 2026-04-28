from services.user_service.app.core.config import settings


class CapabilitiesService:
    def get_capabilities(self) -> dict:
        return {
            "llm_providers": [
                {
                    "code": "openai",
                    "label": "OpenAI",
                    "enabled": settings.openai_enabled,
                    "reason": None if settings.openai_enabled else "Недоступно",
                },
                {
                    "code": "ollama",
                    "label": "Ollama",
                    "enabled": settings.ollama_enabled,
                    "reason": None
                    if settings.ollama_enabled
                    else "Недоступно в текущем окружении",
                },
            ],
            "default_llm_provider": settings.default_llm_provider,
            "available_search_modes": [
                "lexical",
                "semantic",
                "semantic_llm",
            ],
        }