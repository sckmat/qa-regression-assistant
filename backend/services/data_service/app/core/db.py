from sqlalchemy import text
from sqlalchemy.schema import CreateSchema

from shared.db.session import (
    build_engine,
    build_session_factory,
    make_session_dependency,
)
from services.data_service.app.core.config import settings
from services.data_service.app.models.base import Base
from services.data_service.app.models.test_case import TestCase  # noqa: F401
from services.data_service.app.models.test_case_embedding import (  # noqa: F401
    TestCaseEmbedding,
)

engine = build_engine(
    database_url=settings.database_url,
    echo=settings.data_service_db_echo,
)

SessionFactory = build_session_factory(engine)
get_db_session = make_session_dependency(SessionFactory)


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.execute(
            CreateSchema(settings.data_service_db_schema, if_not_exists=True)
        )

        # Включаем pgvector extension в базе.
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        await connection.run_sync(Base.metadata.create_all)