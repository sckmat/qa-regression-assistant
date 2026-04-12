from sqlalchemy.schema import CreateSchema

from shared.db.session import (
    build_engine,
    build_session_factory,
    make_session_dependency,
)
from services.data_service.app.core.config import settings
from services.data_service.app.models import test_case  # noqa: F401
from services.data_service.app.models.base import Base

# Отдельный engine для data_service.
engine = build_engine(
    database_url=settings.database_url,
    echo=settings.data_service_db_echo,
)

# Фабрика сессий, которую использует только data_service.
SessionFactory = build_session_factory(engine)

# FastAPI dependency для получения БД-сессии в роуте.
get_db_session = make_session_dependency(SessionFactory)


async def init_db() -> None:
    """
    Создает схему и таблицы data_service.
    """
    async with engine.begin() as connection:
        await connection.execute(
            CreateSchema(settings.data_service_db_schema, if_not_exists=True)
        )
        await connection.run_sync(Base.metadata.create_all)
