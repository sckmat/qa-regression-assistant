from pydantic import BaseModel


class RetrievalCandidate(BaseModel):
    """
    Нормализованный кандидат внутри user_service.

    Мы приводим lexical и semantic ответы data_service
    к единому внутреннему виду, чтобы остальной код
    не зависел от конкретного режима поиска.
    """

    source_test_case_id: int
    title: str

    # Унифицированный score для хранения в существующей таблице.
    # Для lexical это обычный relevance_score.
    # Для semantic это round(similarity_score * 1000).
    normalized_score: int

    # Для lexical тут будут совпавшие токены.
    # Для semantic пока оставляем пустой список.
    matched_terms: list[str]