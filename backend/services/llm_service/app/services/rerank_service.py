from services.llm_service.app.core.config import settings
from services.llm_service.app.providers.factory import build_llm_provider
from services.llm_service.app.schemas.rerank import (
    RerankRequest,
    RerankResponse,
)


class RerankService:
    async def rerank(
        self,
        payload: RerankRequest,
    ) -> RerankResponse:

        provider_name = payload.provider or settings.llm_provider

        provider = build_llm_provider(provider_name)

        llm_output = await provider.rerank(
            change_summary=payload.change_summary,
            candidates=payload.candidates,
            top_n=payload.top_n,
        )

        filtered_items = [
            item for item in llm_output.items if item.is_relevant
        ]
        filtered_items.sort(key=lambda item: item.llm_score, reverse=True)
        filtered_items = filtered_items[: payload.top_n]

        if provider_name == "ollama":
            model = settings.ollama_llm_model
        else:
            model = settings.openai_llm_model

        return RerankResponse(
            provider=provider_name,
            model=model,
            items=filtered_items,
        )