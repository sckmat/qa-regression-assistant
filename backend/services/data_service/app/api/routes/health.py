from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Простейший healthcheck для data_service.
    """
    return {"status": "ok"}
