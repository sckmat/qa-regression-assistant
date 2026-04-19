from shared.config.base import BaseAppSettings


class LLMServiceSettings(BaseAppSettings):
    """
    Настройки llm_service.
    """

    llm_provider: str = "ollama"   # ollama | openai
    llm_model: str = "llama3.1"
    llm_timeout_seconds: int = 120

    ollama_llm_base_url: str = "http://127.0.0.1:11434/v1"

    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: str | None = None

    llm_service_name: str = "llm-service"
    llm_service_host: str = "127.0.0.1"
    llm_service_port: int = 8002
    llm_service_debug: bool = True


settings = LLMServiceSettings()