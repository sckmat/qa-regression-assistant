from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Базовый declarative class только для моделей user_service.

    Это важно:
    у каждого сервиса может быть свой Base, чтобы метаданные сервисов
    не смешивались и create_all() не создавал таблицы чужих сервисов.
    """
    pass
