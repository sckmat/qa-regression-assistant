from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """
    Схема входящего тела запроса на создание проекта.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название проекта. Должно быть уникальным внутри user_service.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Краткое описание проекта.",
    )


class ProjectRead(BaseModel):
    """
    Схема ответа с данными проекта.
    """

    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
