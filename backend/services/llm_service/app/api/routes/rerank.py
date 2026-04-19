from fastapi import APIRouter

from services.llm_service.app.schemas.rerank import (
    RerankRequest,
    RerankResponse,
)
from services.llm_service.app.services.rerank_service import RerankService

router = APIRouter(tags=["Rerank"])


@router.post(
    "/rerank",
    response_model=RerankResponse,
    status_code=200,
)
async def rerank_candidates(
    payload: RerankRequest,
) -> RerankResponse:
    """
    Выполняет LLM rerank уже найденных retrieval-кандидатов.
    """
    service = RerankService()
    return await service.rerank(payload)