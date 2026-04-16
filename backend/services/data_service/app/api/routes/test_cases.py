from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.core.db import get_db_session
from services.data_service.app.schemas.test_case import (
    TestCaseImportRequest,
    TestCaseImportResponse,
    TestCaseRead,
    TestCaseSearchRequest,
    TestCaseSearchResponse,
)
from services.data_service.app.services.test_case_service import TestCaseService
from services.data_service.app.schemas.reindex import ProjectReindexResponse
from services.data_service.app.services.indexing_service import IndexingService
from services.data_service.app.schemas.semantic_search import (
    SemanticSearchRequest,
    SemanticSearchResponse,
)
from services.data_service.app.services.semantic_search_service import (
    SemanticSearchService,
)

router = APIRouter(tags=["Test Cases"])


@router.post(
    "/projects/{project_id}/test-cases/import",
    response_model=TestCaseImportResponse,
    status_code=status.HTTP_201_CREATED,
)
async def import_test_cases(
    project_id: int,
    payload: TestCaseImportRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Пакетно импортирует тест-кейсы для проекта.

    Почему проект приходит path-параметром:
    - так API явно показывает, к какому проекту относится импорт;
    - тело запроса содержит только сами тест-кейсы.
    """
    service = TestCaseService(session)
    items = await service.import_test_cases(project_id, payload)
    return TestCaseImportResponse(
        imported_count=len(items),
        project_id=project_id,
        items=items,
    )


@router.get(
    "/projects/{project_id}/test-cases",
    response_model=list[TestCaseRead],
)
async def list_test_cases(
    project_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Возвращает все тест-кейсы проекта.
    """
    service = TestCaseService(session)
    return await service.list_test_cases(project_id)


@router.get(
    "/test-cases/{test_case_id}",
    response_model=TestCaseRead,
)
async def get_test_case(
    test_case_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Возвращает один тест-кейс по id.
    """
    service = TestCaseService(session)
    return await service.get_test_case(test_case_id)


@router.post(
    "/projects/{project_id}/test-cases/search",
    response_model=TestCaseSearchResponse,
)
async def search_test_cases(
    project_id: int,
    payload: TestCaseSearchRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Ищет кандидатов по текстовому запросу.

    На этом этапе это не семантический поиск, а простой baseline retrieval:
    - через разбиение query на токены;
    - через ILIKE-фильтрацию;
    - через простое rule-based ранжирование.
    """
    service = TestCaseService(session)
    return await service.search_test_cases(
        project_id=project_id,
        query=payload.query,
        limit=payload.limit,
    )

@router.post(
    "/projects/{project_id}/test-cases/reindex",
    response_model=ProjectReindexResponse,
    status_code=200,
)
async def reindex_project_test_cases(
    project_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> ProjectReindexResponse:
    """
    Переиндексирует все тест-кейсы проекта:
    строит embeddings и сохраняет их в БД.
    """
    service = IndexingService(session)
    return await service.reindex_project(project_id)

@router.post(
    "/projects/{project_id}/test-cases/semantic-search",
    response_model=SemanticSearchResponse,
    status_code=200,
)
async def semantic_search_test_cases(
    project_id: int,
    payload: SemanticSearchRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SemanticSearchResponse:
    """
    Выполняет semantic search по embeddings test cases проекта.
    """
    service = SemanticSearchService(session)
    return await service.semantic_search(project_id, payload)