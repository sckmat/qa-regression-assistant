from shared.config.base import BaseAppSettings


class DataServiceSettings(BaseAppSettings):
    """
    Настройки именно для data_service.

    Все значения читаются из `.env`.
    Префикс DATA_SERVICE_ нужен, чтобы настройки разных сервисов не смешивались.
    """

    database_url: str

    data_service_name: str = "data-service"
    data_service_host: str = "127.0.0.1"
    data_service_port: int = 8001
    data_service_debug: bool = True
    data_service_db_echo: bool = False
    data_service_db_schema: str = "data_service"


settings = DataServiceSettings()
