from shared.config.base import BaseAppSettings


class LLMServiceSettings(BaseAppSettings):
    llm_service_name: str = "llm-service"
    llm_service_host: str = "127.0.0.1"
    llm_service_port: int = 8002
    llm_service_debug: bool = True

    openai_base_url: str
    openai_api_key: str | None = None
    openai_llm_model: str = "gpt-4.1-mini"

    ollama_llm_base_url: str
    ollama_llm_model: str = "llama3.1"

    openai_enabled: bool = True
    ollama_enabled: bool = False

    default_llm_provider: str = "openai"

    llm_timeout_seconds: int = 120


settings = LLMServiceSettings()