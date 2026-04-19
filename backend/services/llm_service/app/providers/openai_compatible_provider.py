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
    Универсальный провайдер поверх OpenAI-compatible chat/completions API.

    Подходит и для:
    - OpenAI
    - Ollama (через /v1/chat/completions)
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
        messages = self._build_messages(
            change_summary=change_summary,
            candidates=candidates,
            top_n=top_n,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "rerank_response",
                "strict": True,
                "schema": LLMStructuredRerankOutput.model_json_schema(),
            },
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "stream": False,
            "response_format": response_format,
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
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise ValueError(f"Unexpected LLM response format: {data}") from exc

        if isinstance(content, list):
            # На всякий случай поддерживаем content как массив частей.
            content = "".join(
                part.get("text", "")
                for part in content
                if isinstance(part, dict)
            )

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"LLM returned invalid JSON: {content}") from exc

        try:
            return LLMStructuredRerankOutput.model_validate(parsed)
        except ValidationError as exc:
            raise ValueError(f"LLM JSON does not match schema: {exc}") from exc

    def _build_messages(
        self,
        change_summary: str,
        candidates: list[RerankCandidateInput],
        top_n: int,
    ) -> list[dict]:
        candidates_payload = [
            {
                "test_case_id": candidate.test_case_id,
                "title": candidate.title,
                "raw_text": candidate.raw_text,
                "retrieval_score": candidate.retrieval_score,
            }
            for candidate in candidates
        ]

        system_prompt = (
            "Ты — QA assistant для отбора регрессионных тест-кейсов. "
            "Тебе дано описание изменений и список уже найденных кандидатов. "
            "Нужно выбрать наиболее релевантные тест-кейсы для регресса. "
            "Для каждого кандидата верни test_case_id, is_relevant, llm_score от 0 до 100 "
            "и краткое explanation на русском языке. "
            "Оценивай только по переданным данным. "
            "Не придумывай тест-кейсы, которых нет во входном списке. "
            f"Верни не более {top_n} элементов в items."
        )

        user_payload = {
            "change_summary": change_summary,
            "top_n": top_n,
            "candidates": candidates_payload,
        }

        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": json.dumps(user_payload, ensure_ascii=False, indent=2),
            },
        ]