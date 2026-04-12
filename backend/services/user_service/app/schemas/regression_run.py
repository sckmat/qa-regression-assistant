from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RegressionRunCreate(BaseModel):
    """
    Схема входящего запроса на создание запуска анализа.
    """

    change_summary: str = Field(
        ...,
        min_length=1,
        description="Описание изменений, по которым нужно собрать регресс.",
    )


class RegressionRunRead(BaseModel):
    """
    Схема ответа с данными о запуске анализа.
    """

    id: int
    project_id: int
    change_summary: str
    status: str
    result_summary: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
