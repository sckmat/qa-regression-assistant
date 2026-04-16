from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from services.user_service.app.schemas.regression_run_candidate import (
    RegressionRunCandidateRead,
)


class RegressionRunCreate(BaseModel):
    """
    Схема входящего запроса на создание запуска анализа.
    """

    change_summary: str = Field(
        ...,
        min_length=1,
        description="Описание изменений, по которым нужно собрать регресс.",
    )

    candidate_limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Сколько кандидатов запрашивать у data_service.",
    )

    search_mode: Literal["lexical", "semantic"] = Field(
        default="lexical",
        description="Режим retrieval в data_service.",
    )


class RegressionRunRead(BaseModel):
    """
    Короткая схема ответа по запуску анализа.
    Подходит для списков.
    """

    id: int
    project_id: int
    change_summary: str
    status: str
    result_summary: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class RegressionRunDetailRead(RegressionRunRead):
    """
    Детальная схема ответа:
    помимо самого запуска содержит найденных кандидатов.
    """

    candidates: list[RegressionRunCandidateRead] = Field(default_factory=list)