from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TestCaseImportItem(BaseModel):
    """
    Описание одного тест-кейса для импорта.
    """

    external_id: Optional[str] = Field(
        default=None,
        description="Внешний идентификатор из TMS / Allure / другой системы.",
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Краткое название тест-кейса.",
    )
    preconditions: Optional[str] = Field(
        default=None,
        description="Предусловия выполнения теста.",
    )
    steps: Optional[str] = Field(
        default=None,
        description="Шаги выполнения теста. Пока храним обычным текстом.",
    )
    expected_result: Optional[str] = Field(
        default=None,
        description="Ожидаемый результат.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Список тегов тест-кейса.",
    )
    priority: Optional[str] = Field(
        default=None,
        description="Приоритет тест-кейса, если он есть в источнике.",
    )
    raw_text: Optional[str] = Field(
        default=None,
        description="Полный текст тест-кейса. Если не передан, сервис соберет его сам.",
    )


class TestCaseImportRequest(BaseModel):
    """
    Пакетный импорт тест-кейсов.
    """

    items: list[TestCaseImportItem] = Field(
        ...,
        min_length=1,
        description="Список тест-кейсов для импорта.",
    )


class TestCaseRead(BaseModel):
    """
    Схема ответа с данными тест-кейса.
    """

    id: int
    project_id: int
    external_id: Optional[str]
    title: str
    preconditions: Optional[str]
    steps: Optional[str]
    expected_result: Optional[str]
    tags: list[str] = Field(default_factory=list)
    priority: Optional[str]
    raw_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TestCaseImportResponse(BaseModel):
    """
    Ответ после пакетного импорта.
    """

    imported_count: int
    project_id: int
    items: list[TestCaseRead]


class TestCaseSearchRequest(BaseModel):
    """
    Запрос на поиск тест-кейсов по тексту.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Текстовый запрос: описание изменений, релизные заметки и т.д.",
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Максимальное число результатов.",
    )


class TestCaseSearchResult(BaseModel):
    """
    Один найденный кандидат с простейшей оценкой релевантности.
    """

    test_case: TestCaseRead
    relevance_score: int
    matched_terms: list[str]


class TestCaseSearchResponse(BaseModel):
    """
    Итоговый ответ поиска.
    """

    project_id: int
    query: str
    candidates: list[TestCaseSearchResult]
