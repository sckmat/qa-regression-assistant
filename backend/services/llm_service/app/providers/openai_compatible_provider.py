import json

import httpx
from pydantic import ValidationError

from services.llm_service.app.providers.llm_provider import LLMProvider
from services.llm_service.app.schemas.rerank import (
    LLMStructuredRerankOutput,
    RerankCandidateInput,
)


class OpenAICompatibleProvider(LLMProvider):

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
        print(f"[LLM] Request to: {self.base_url}")
        print(f"[LLM] Model: {self.model}")
        print(f"[LLM] Сandidates: {candidates}")
        print(f"[LLM] top_n: {top_n}")
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
            "Тебе дано описание изменений и список кандидатов тест-кейсов. "

            "Твоя задача — проанализировать ВСЕ переданные кандидаты и сформировать ранжированный список "
            "тест-кейсов для регрессионного тестирования. "

            "Важно: не останавливайся после нахождения первого подходящего тест-кейса. "
            "Ты обязан оценить каждый тест-кейс из списка candidates, а затем вернуть top_n элементов, "
            "начиная с самых релевантных. "

            "Описание изменений может быть коротким, обобщенным или написанным как релизная заметка. "
            "Не требуй, чтобы в описании изменений были перечислены все частные случаи. "
            "Если в изменении указана функциональная область или механизм, считай релевантными тесты, "
            "которые проверяют этот механизм, его позитивные сценарии, негативные сценарии, граничные случаи, "
            "валидацию, ошибки API, состояние после выполнения действия и обратную совместимость поведения. "

            "Пример: если указано 'Изменена работа reset-ссылки', релевантны тесты про запрос reset-ссылки, "
            "валидную reset-ссылку, истекший reset-токен, одноразовость ссылки, повторный запрос восстановления, "
            "недействительный токен, смену пароля по ссылке, вход со старым и новым паролем после смены. "

            "ВАЖНО:\n"
            "1. Оценивай только по переданным кандидатам. Не придумывай тест-кейсы, которых нет во входном списке.\n"
            "2. Обработай каждый элемент из candidates перед формированием ответа.\n"
            "3. Если тест-кейс относится к той же измененной функциональной области и проверяет возможный регрессионный риск — "
            "считай его релевантным.\n"
            "4. Не отбрасывай тест только потому, что конкретный подслучай не указан в описании изменений.\n"
            "5. Если тест относится к другой функциональности и не может быть затронут изменением — верни его с is_relevant = false "
            "и кратко объясни, почему он не подходит.\n"
            "6. Не возвращай только один элемент, если среди кандидатов есть другие релевантные или потенциально связанные тест-кейсы.\n"
            "7. Если релевантных тест-кейсов нет, все равно верни до top_n наиболее близких кандидатов с is_relevant = false "
            "и объясни, почему они не подходят.\n"

            "Правила оценки llm_score:\n"
            "- 90-100: тест напрямую проверяет измененное поведение;\n"
            "- 75-89: тест проверяет тот же механизм или важный регрессионный риск вокруг изменения;\n"
            "- 60-74: тест проверяет смежный сценарий в той же функциональной области;\n"
            "- 1-59: тест слабосвязан или нерелевантен;\n"
            "- 0: тест полностью относится к другой функциональности.\n"

            f"Верни ровно до {top_n} элементов в items. "
            "Если кандидатов меньше top_n, верни все переданные кандидаты. "
            "Если кандидатов больше top_n, верни top_n лучших кандидатов после оценки всех candidates. "

            "Порядок элементов в items должен быть по убыванию релевантности: "
            "сначала is_relevant = true с наибольшим llm_score, затем менее релевантные кандидаты. "

            "Для каждого элемента верни:\n"
            "- test_case_id\n"
            "- is_relevant (true/false)\n"
            "- llm_score от 0 до 100\n"
            "- explanation на русском языке.\n"

            "Для релевантного теста в explanation укажи, какую часть изменения или какой регрессионный риск он покрывает. "
            "Для нерелевантного теста в explanation явно укажи, почему он не подходит к описанию изменений. "
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

        print("LLM result raw: %s", data)

        content_text = self._extract_output_text(data)

        print("LLM result: %s", content_text)

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