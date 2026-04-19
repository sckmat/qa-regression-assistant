from pydantic import BaseModel


class RetrievalCandidate(BaseModel):
    """
    Нормализованный кандидат внутри user_service.

    Приводим lexical, semantic и semantic+llm
    к единому внутреннему виду.
    """

    source_test_case_id: int
    title: str
    raw_text: str

    # То, что сохраняем в существующую колонку relevance_score.
    normalized_score: int

    # Исходный retrieval score:
    # - для lexical это relevance_score
    # - для semantic это similarity_score
    # - для semantic_llm можно сохранить semantic score,
    #   а normalized_score уже будет llm_score
    retrieval_score: float | None = None

    matched_terms: list[str]
    explanation: str | None = None