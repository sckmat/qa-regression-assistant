from services.llm_service.app.core.config import settings
from services.llm_service.app.providers.factory import build_llm_provider
from services.llm_service.app.schemas.rerank import (
    RerankCandidateInput,
    RerankRequest,
    RerankResponse,
)


class RerankService:
    """
    Сервис rerank через выбранный LLM provider.
    """

    def __init__(self):
        self.provider = build_llm_provider()

    async def rerank(
        self,
        payload: RerankRequest,
    ) -> RerankResponse:
        llm_output = await self.provider.rerank(
            change_summary=payload.change_summary,
            candidates=payload.candidates,
            top_n=payload.top_n,
        )

        # На всякий случай:
        # - оставляем только релевантные
        # - сортируем по llm_score по убыванию
        # - обрезаем до top_n
        filtered_items = [
            item for item in llm_output.items if item.is_relevant
        ]
        filtered_items.sort(key=lambda item: item.llm_score, reverse=True)
        filtered_items = filtered_items[: payload.top_n]

        return RerankResponse(
            provider=settings.llm_provider,
            model=settings.llm_model,
            items=filtered_items,
        )