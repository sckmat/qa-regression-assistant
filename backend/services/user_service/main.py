from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.user_service.app.api.router import api_router
from services.user_service.app.core.config import settings
from services.user_service.app.core.db import init_db

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Lifecycle-хук приложения.

    На старте:
    - создаем схему PostgreSQL для user_service, если ее еще нет;
    - создаем таблицы текущего сервиса.

    Для MVP это допустимый подход.
    Позже лучше перейти на Alembic-миграции.
    """
    await init_db()
    yield


app = FastAPI(
    title=settings.user_service_name,
    debug=settings.user_service_debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
