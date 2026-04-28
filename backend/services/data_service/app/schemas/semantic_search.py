from pydantic import BaseModel, Field


class SemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)

    embedding_provider: str | None = None


class SemanticSearchTestCaseRead(BaseModel):
    id: int
    project_id: int
    title: str
    raw_text: str

    model_config = {"from_attributes": True}


class SemanticSearchCandidateRead(BaseModel):
    test_case: SemanticSearchTestCaseRead
    cosine_distance: float
    similarity_score: float


class SemanticSearchResponse(BaseModel):
    project_id: int
    query: str
    embedding_provider: str
    embedding_model: str
    candidates: list[SemanticSearchCandidateRead]