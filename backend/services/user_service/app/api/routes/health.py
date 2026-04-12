from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Простейший healthcheck.

    Нужен для быстрой проверки:
    - сервис поднялся;
    - роутинг работает;
    - FastAPI-приложение отвечает.
    """
    return {"status": "ok"}
