from fastapi import APIRouter

from services.data_service.app.api.routes.health import router as health_router
from services.data_service.app.api.routes.test_cases import router as test_cases_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(test_cases_router, prefix="/api/v1")
