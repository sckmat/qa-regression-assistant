from pydantic import BaseModel


class ProjectReindexResponse(BaseModel):
    """
    Ответ после переиндексации проекта.
    """

    project_id: int
    embedding_provider: str
    embedding_model: str
    embedding_dim: int
    processed_test_cases: int
    indexed_test_cases: int
    status: str