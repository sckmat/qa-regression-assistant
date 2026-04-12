from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle-хук приложения.

    Здесь выполняем инициализацию при старте приложения.
    Пока используем автоматическое создание таблиц.
    Для MVP это удобно.
    Позже лучше перейти на Alembic-миграции.
    """
    await create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_title,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
async def root():
    """
    Простейший healthcheck / проверка, что сервис поднялся.
    """
    return {
        "message": "User Service is running"
    }