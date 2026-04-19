from abc import ABC, abstractmethod

from services.llm_service.app.schemas.rerank import (
    LLMStructuredRerankOutput,
    RerankCandidateInput,
)


class LLMProvider(ABC):
    """
    Абстрактный провайдер LLM.
    """

    @abstractmethod
    async def rerank(
        self,
        change_summary: str,
        candidates: list[RerankCandidateInput],
        top_n: int,
    ) -> LLMStructuredRerankOutput:
        raise NotImplementedError