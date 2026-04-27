import json

import httpx
from pydantic import ValidationError

from services.llm_service.app.providers.llm_provider import LLMProvider
from services.llm_service.app.schemas.rerank import (
    LLMStructuredRerankOutput,
    RerankCandidateInput,
)


class OpenAICompatibleProvider(LLMProvider):
    """
    Провайдер поверх OpenAI Responses API.
    Использует structured outputs через text.format/json_schema.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: int,
        api_key: str | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.api_key = api_key

    async def rerank(
        self,
        change_summary: str,
        candidates: list[RerankCandidateInput],
        top_n: int,
    ) -> LLMStructuredRerankOutput:
        candidates_payload = [
            {
                "test_case_id": candidate.test_case_id,
                "title": candidate.title,
                "raw_text": candidate.raw_text,
                "retrieval_score": candidate.retrieval_score,
            }
            for candidate in candidates
        ]

        instructions = (
            "Ты — QA assistant для отбора регрессионных тест-кейсов. "
            "Тебе дано описание изменений и список уже найденных кандидатов. "
            "Нужно выбрать наиболее релевантные тест-кейсы для регресса. "
            "Оценивай только по переданным данным. "
            "Не придумывай тест-кейсы, которых нет во входном списке. "
            f"Верни не более {top_n} элементов в items. "
            "Для каждого элемента верни test_case_id, is_relevant, llm_score от 0 до 100 "
            "и краткое explanation на русском языке."
        )

        user_payload = {
            "change_summary": change_summary,
            "top_n": top_n,
            "candidates": candidates_payload,
        }

        payload = {
            "model": self.model,
            "instructions": instructions,
            "input": json.dumps(user_payload, ensure_ascii=False, indent=2),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "rerank_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "test_case_id": {"type": "integer"},
                                        "is_relevant": {"type": "boolean"},
                                        "llm_score": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 100,
                                        },
                                        "explanation": {"type": "string"},
                                    },
                                    "required": [
                                        "test_case_id",
                                        "is_relevant",
                                        "llm_score",
                                        "explanation",
                                    ],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["items"],
                        "additionalProperties": False,
                    },
                }
            },
        }

        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout_seconds, connect=10.0)
        ) as client:
            response = await client.post(
                f"{self.base_url}/responses",
                json=payload,
                headers=headers,
            )

        if response.is_error:
            raise RuntimeError(
                f"OpenAI Responses API error: status={response.status_code}, body={response.text}"
            )

        data = response.json()

        content_text = self._extract_output_text(data)

        try:
            parsed = json.loads(content_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM returned invalid JSON: {content_text}"
            ) from exc

        try:
            return LLMStructuredRerankOutput.model_validate(parsed)
        except ValidationError as exc:
            raise ValueError(
                f"LLM JSON does not match schema: {exc}. Raw JSON: {parsed}"
            ) from exc

    def _extract_output_text(self, data: dict) -> str:
        """
        Извлекает текстовый output из ответа Responses API.
        Ищем assistant message -> content[type=output_text] -> text.
        """
        output = data.get("output", [])
        if not isinstance(output, list):
            raise ValueError(f"Unexpected Responses API format: {data}")

        collected_parts: list[str] = []

        for item in output:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "message":
                continue

            content = item.get("content", [])
            if not isinstance(content, list):
                continue

            for part in content:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "output_text":
                    text = part.get("text")
                    if isinstance(text, str) and text.strip():
                        collected_parts.append(text)

        if not collected_parts:
            raise ValueError(f"Could not extract output_text from Responses API: {data}")

        return "\n".join(collected_parts)