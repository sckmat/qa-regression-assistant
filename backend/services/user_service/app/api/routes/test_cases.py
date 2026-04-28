from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.db import get_db_session
from services.user_service.app.services.test_case_gateway_service import (
    TestCaseGatewayService,
)

from services.user_service.app.api.dependencies.current_user import get_current_user

router = APIRouter(tags=["Test Cases"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/projects/{project_id}/test-cases")
async def list_project_test_cases(
    project_id: int,
    session: DbSession,
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    service = TestCaseGatewayService(session)
    return await service.list_test_cases(project_id, current_user.id)


@router.get("/test-cases/{test_case_id}")
async def get_test_case(
    test_case_id: int,
    session: DbSession,
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    service = TestCaseGatewayService(session)
    return await service.get_test_case(test_case_id, current_user.id)


@router.post("/projects/{project_id}/test-cases/import-file", status_code=201)
async def import_project_test_cases_file(
    project_id: int,
    session: DbSession,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    service = TestCaseGatewayService(session)
    return await service.import_test_cases_file(
        project_id=project_id,
        file=file,
        user_id=current_user.id,
    )


@router.post("/projects/{project_id}/test-cases/reindex")
async def reindex_project_test_cases(
    project_id: int,
    session: DbSession,
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    service = TestCaseGatewayService(session)
    return await service.reindex_test_cases(
        project_id,
        current_user.id,
    )