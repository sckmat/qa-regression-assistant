from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.data_service.app.api.router import api_router
from services.data_service.app.core.config import settings
from services.data_service.app.core.db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifecycle-хук data_service.

    На старте сервис:
    - создает отдельную схему PostgreSQL для data_service;
    - создает таблицы текущего сервиса.

    Для MVP это удобно, потому что можно быстро поднять сервис локально.
    Позже этот код лучше заменить Alembic-миграциями.
    """
    await init_db()
    yield


app = FastAPI(
    title=settings.data_service_name,
    debug=settings.data_service_debug,
    lifespan=lifespan,
)

app.include_router(api_router)
