from fastapi import APIRouter

from services.llm_service.app.schemas.rerank import (
    RerankRequest,
    RerankResponse,
)
from services.llm_service.app.services.rerank_service import RerankService
from services.llm_service.app.providers.factory import build_llm_provider

router = APIRouter(tags=["Rerank"])


@router.post("/rerank")
async def rerank_candidates(payload: RerankRequest):
    provider = build_llm_provider(payload.provider)

    service = RerankService(provider)

    return await service.rerank(payload)