from pydantic import BaseModel, Field


class SemanticSearchRequest(BaseModel):
    """
    Запрос на семантический поиск test cases по проекту.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Текст запроса / описания изменений",
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Сколько кандидатов вернуть",
    )


class SemanticSearchTestCaseRead(BaseModel):
    """
    Упрощенная схема test case в ответе semantic search.
    """

    id: int
    project_id: int
    title: str
    raw_text: str

    model_config = {"from_attributes": True}


class SemanticSearchCandidateRead(BaseModel):
    """
    Один кандидат из semantic search.
    """

    test_case: SemanticSearchTestCaseRead
    cosine_distance: float
    similarity_score: float


class SemanticSearchResponse(BaseModel):
    """
    Ответ semantic search.
    """

    project_id: int
    query: str
    embedding_provider: str
    embedding_model: str
    candidates: list[SemanticSearchCandidateRead]