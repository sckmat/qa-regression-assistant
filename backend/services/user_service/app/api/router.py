from fastapi import APIRouter

from services.user_service.app.api.routes.health import router as health_router
from services.user_service.app.api.routes.projects import router as projects_router
from services.user_service.app.api.routes.regression_runs import (
    router as regression_runs_router,
)
from services.user_service.app.api.routes.test_cases import router as test_cases_router
from services.user_service.app.api.routes import auth


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(projects_router, prefix="/api/v1")
api_router.include_router(regression_runs_router, prefix="/api/v1")
api_router.include_router(test_cases_router, prefix="/api/v1")
api_router.include_router(auth.router, prefix="/api/v1")