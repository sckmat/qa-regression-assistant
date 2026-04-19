from fastapi import APIRouter

from services.llm_service.app.api.routes.rerank import router as rerank_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(rerank_router)