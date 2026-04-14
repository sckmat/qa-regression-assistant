from datetime import datetime

from pydantic import BaseModel


class RegressionRunCandidateRead(BaseModel):
    """
    Схема ответа по одному найденному кандидату.
    """

    id: int
    regression_run_id: int
    source_test_case_id: int
    title: str
    relevance_score: int
    matched_terms: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}