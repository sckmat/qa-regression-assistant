from __future__ import annotations

import re
from typing import Iterable


class TextProcessingService:
    """
    Небольшой вспомогательный сервис для подготовки текста.

    Это не отдельный микросервис, а обычный внутренний helper-класс data_service.
    """

    _split_pattern = re.compile(r"[^\w]+", flags=re.UNICODE)
    _whitespace_pattern = re.compile(r"\s+")

    def normalize_text(self, value: str | None) -> str:
        """
        Нормализует текст:
        - приводит к нижнему регистру;
        - схлопывает повторные пробелы;
        - убирает лишние пробельные символы по краям.
        """
        if not value:
            return ""

        normalized = value.lower().strip()
        normalized = self._whitespace_pattern.sub(" ", normalized)
        return normalized

    def tokenize_query(self, query: str) -> list[str]:
        """
        Разбивает запрос на простые термины.

        Для MVP используем очень простое правило:
        - разбиваем по не-буквенно-цифровым символам;
        - убираем пустые токены;
        - оставляем токены длиной от 2 символов;
        - убираем дубликаты с сохранением порядка.
        """
        raw_parts = self._split_pattern.split(self.normalize_text(query))

        unique_terms: list[str] = []
        seen: set[str] = set()
        for item in raw_parts:
            if len(item) < 2:
                continue
            if item in seen:
                continue
            seen.add(item)
            unique_terms.append(item)

        return unique_terms

    def build_raw_text(
        self,
        *,
        title: str,
        preconditions: str | None,
        steps: str | None,
        expected_result: str | None,
        tags: Iterable[str] | None,
        priority: str | None,
        external_id: str | None,
    ) -> str:
        """
        Собирает единый текст документа из полей тест-кейса.

        Это удобно, потому что дальше можно искать по одному текстовому полю,
        а не по набору разрозненных колонок.
        """
        parts = [
            f"external_id: {external_id}" if external_id else None,
            f"title: {title}",
            f"preconditions: {preconditions}" if preconditions else None,
            f"steps: {steps}" if steps else None,
            f"expected_result: {expected_result}" if expected_result else None,
            f"tags: {', '.join(tags)}" if tags else None,
            f"priority: {priority}" if priority else None,
        ]
        return "\n".join(part for part in parts if part)
