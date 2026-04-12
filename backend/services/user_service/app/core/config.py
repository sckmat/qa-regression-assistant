from shared.config.base import BaseAppSettings


class UserServiceSettings(BaseAppSettings):
    """
    Настройки именно для user_service.

    Все значения читаются из `.env`.
    Префикс USER_SERVICE_ позволяет не смешивать настройки разных сервисов.
    """

    database_url: str

    user_service_name: str = "user-service"
    user_service_host: str = "127.0.0.1"
    user_service_port: int = 8000
    user_service_debug: bool = True
    user_service_db_echo: bool = False
    user_service_db_schema: str = "user_service"


settings = UserServiceSettings()
