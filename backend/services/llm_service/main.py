from fastapi import FastAPI

from services.llm_service.app.api.router import api_router
from services.llm_service.app.core.config import settings

app = FastAPI(
    title=settings.llm_service_name,
    debug=settings.llm_service_debug,
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health() -> dict:
    return {
        "status": "ok",
        "service": settings.llm_service_name,
        "provider": settings.llm_provider,
        "model": settings.llm_model,
    }