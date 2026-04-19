from shared.config.base import BaseAppSettings


class UserServiceSettings(BaseAppSettings):
    database_url: str

    user_service_name: str = "user-service"
    user_service_host: str = "127.0.0.1"
    user_service_port: int = 8000
    user_service_debug: bool = True
    user_service_db_echo: bool = False
    user_service_db_schema: str = "user_service"

    # Data service
    data_service_base_url: str = "http://127.0.0.1:8001"

    # LLM service
    llm_service_base_url: str = "http://127.0.0.1:8002"


settings = UserServiceSettings()