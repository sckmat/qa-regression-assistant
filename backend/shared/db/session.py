from collections.abc import AsyncIterator
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def build_engine(database_url: str, echo: bool = False) -> AsyncEngine:
    """
    Создает AsyncEngine для PostgreSQL.

    Параметры:
    - database_url: строка подключения к PostgreSQL;
    - echo: печатать ли SQL-запросы в консоль.
    """
    return create_async_engine(
        database_url,
        echo=echo,
        future=True,
    )


def build_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """
    Создает фабрику асинхронных SQLAlchemy-сессий.

    expire_on_commit=False нужен, чтобы после commit объектом можно было
    пользоваться без повторного запроса к БД.
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def make_session_dependency(
    session_factory: async_sessionmaker[AsyncSession],
) -> Callable[[], AsyncIterator[AsyncSession]]:
    """
    Возвращает dependency-функцию для FastAPI.

    Идея в том, что каждый сервис сам создает session_factory,
    а shared лишь помогает собрать dependency.
    """

    async def _get_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    return _get_session
