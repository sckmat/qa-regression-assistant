from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError


class DataServiceTestCaseRead(BaseModel):
    """
    Упрощенная схема тест-кейса, которую возвращает data_service.
    Нам не нужны все поля для orchestration-логики,
    но удобно распарсить объект в типизированный вид.
    """

    id: int
    project_id: int
    title: str
    raw_text: str


class DataServiceSearchCandidate(BaseModel):
    """
    Один кандидат из ответа data_service.
    """

    test_case: DataServiceTestCaseRead
    relevance_score: int
    matched_terms: list[str]


class DataServiceSearchResponse(BaseModel):
    """
    Ответ data_service на поиск тест-кейсов.
    """

    project_id: int
    query: str
    candidates: list[DataServiceSearchCandidate]


class DataServiceClient:
    """
    Небольшой HTTP-клиент для вызова data_service.

    Почему вынесено в отдельный класс:
    - user_service не должен собирать URL и HTTP-логику прямо в service-слое;
    - так проще потом заменить transport, добавить retry, auth между сервисами и т.д.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def search_test_cases(
        self,
        project_id: int,
        query: str,
        limit: int,
    ) -> DataServiceSearchResponse:
        url = f"{self.base_url}/api/v1/projects/{project_id}/test-cases/search"
        payload = {
            "query": query,
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=5.0)
            ) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            data: dict[str, Any] = response.json()
            return DataServiceSearchResponse.model_validate(data)

        except httpx.ConnectError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Cannot connect to data_service: {exc}",
            ) from exc

        except httpx.HTTPStatusError as exc:
            response_text = exc.response.text
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "data_service returned an error. "
                    f"Status={exc.response.status_code}, body={response_text}"
                ),
            ) from exc

        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Invalid response format from data_service: {exc}",
            ) from exc

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Request to data_service failed: {exc}",
            ) from exc