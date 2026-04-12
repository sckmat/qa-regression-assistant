from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """
    Базовый класс для настроек сервиса.

    Почему он вынесен в shared:
    - все сервисы в этом репозитории будут читать настройки из `.env`;
    - нам удобно один раз определить общие правила работы с конфигом.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
