from pydantic import BaseModel, Field


class RerankCandidateInput(BaseModel):
    """
    Кандидат, пришедший из retrieval-слоя.
    """

    test_case_id: int
    title: str
    raw_text: str
    retrieval_score: float | None = None


class RerankRequest(BaseModel):
    """
    Запрос на rerank.
    """

    change_summary: str = Field(..., min_length=1)
    candidates: list[RerankCandidateInput] = Field(default_factory=list)
    top_n: int = Field(default=5, ge=1, le=20)
    provider: str | None = None


class LLMRerankedItem(BaseModel):
    """
    Один элемент ответа модели.
    """

    test_case_id: int
    is_relevant: bool
    llm_score: int = Field(..., ge=0, le=100)
    explanation: str


class LLMStructuredRerankOutput(BaseModel):
    """
    Структура, которую должна вернуть модель в JSON.
    """

    items: list[LLMRerankedItem]


class RerankResponse(BaseModel):
    """
    Ответ API llm_service.
    """

    provider: str
    model: str
    items: list[LLMRerankedItem]