from shared.config.base import BaseAppSettings


class DataServiceSettings(BaseAppSettings):
    database_url: str

    data_service_name: str = "data-service"
    data_service_host: str = "127.0.0.1"
    data_service_port: int = 8001
    data_service_debug: bool = True
    data_service_db_echo: bool = False
    data_service_db_schema: str = "data_service"

    # Настройки embeddings
    embedding_provider: str = "ollama"   # ollama | openai
    embedding_model: str = "nomic-embed-text-v2-moe"
    embedding_dim: int = 768
    embedding_batch_size: int = 16

    # Ollama
    ollama_base_url: str = "http://127.0.0.1:11434"

    # OpenAI
    openai_base_url: str = "https://api.openai.com"
    openai_api_key: str | None = None


settings = DataServiceSettings()