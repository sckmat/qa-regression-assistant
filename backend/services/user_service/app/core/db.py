from sqlalchemy.schema import CreateSchema

from shared.db.session import (
    build_engine,
    build_session_factory,
    make_session_dependency,
)
from services.user_service.app.core.config import settings
from services.user_service.app.models import project, regression_run  # noqa: F401
from services.user_service.app.models.base import Base

# Отдельный engine для user_service.
# Позже другие сервисы смогут создать свои engine/session factory аналогично.
engine = build_engine(
    database_url=settings.database_url,
    echo=settings.user_service_db_echo,
)

# Фабрика сессий, которую использует именно user_service.
SessionFactory = build_session_factory(engine)

# FastAPI dependency для получения сессии в роуте.
get_db_session = make_session_dependency(SessionFactory)


async def init_db() -> None:
    """
    Создает схему и таблицы user_service.

    Почему это сделано здесь:
    - логика инициализации БД относится к конкретному сервису;
    - shared не должен знать про таблицы конкретного домена.
    """
    async with engine.begin() as connection:
        await connection.execute(
            CreateSchema(settings.user_service_db_schema, if_not_exists=True)
        )
        await connection.run_sync(Base.metadata.create_all)
