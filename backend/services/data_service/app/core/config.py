from shared.config.base import BaseAppSettings


class DataServiceSettings(BaseAppSettings):
    database_url: str

    data_service_name: str = "data-service"
    data_service_host: str = "127.0.0.1"
    data_service_port: int = 8001
    data_service_debug: bool = True
    data_service_db_echo: bool = False
    data_service_db_schema: str = "data_service"

    # ===== Embeddings =====
    default_embedding_provider: str = "openai"
    embedding_dim: int = 768
    embedding_batch_size: int = 16

    # OpenAI
    openai_base_url: str
    openai_api_key: str | None = None
    openai_embedding_model: str = "text-embedding-3-small"

    # Ollama
    ollama_embedding_base_url: str
    ollama_embedding_model: str = "nomic-embed-text"


settings = DataServiceSettings()