from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.db import get_db_session
from services.user_service.app.schemas.regression_run import (
    RegressionRunCreate,
    RegressionRunDetailRead,
    RegressionRunRead,
)
from services.user_service.app.services.regression_run_service import (
    RegressionRunService,
)

router = APIRouter(tags=["Regression Runs"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.post(
    "/projects/{project_id}/regression-runs",
    response_model=RegressionRunDetailRead,
    status_code=201,
)
async def create_regression_run(
    project_id: int,
    payload: RegressionRunCreate,
    session: DbSession,
) -> RegressionRunDetailRead:
    """
    Создает новый запуск анализа регресса для проекта
    и сразу возвращает найденных кандидатов.
    """
    service = RegressionRunService(session)
    return await service.create_run(project_id, payload)


@router.get(
    "/projects/{project_id}/regression-runs",
    response_model=list[RegressionRunRead],
)
async def list_regression_runs(
    project_id: int,
    session: DbSession,
) -> list[RegressionRunRead]:
    """
    Возвращает список запусков по проекту.
    """
    service = RegressionRunService(session)
    runs = await service.list_runs(project_id)
    return [RegressionRunRead.model_validate(run) for run in runs]


@router.get(
    "/regression-runs/{run_id}",
    response_model=RegressionRunDetailRead,
)
async def get_regression_run(
    run_id: int,
    session: DbSession,
) -> RegressionRunDetailRead:
    """
    Возвращает один запуск анализа по id вместе с найденными кандидатами.
    """
    service = RegressionRunService(session)
    return await service.get_run(run_id)