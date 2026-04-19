from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError

from services.user_service.app.schemas.retrieval_candidate import RetrievalCandidate


class DataServiceTestCaseRead(BaseModel):
    id: int
    project_id: int
    title: str
    raw_text: str


# ===== Lexical search =====

class DataServiceSearchCandidate(BaseModel):
    test_case: DataServiceTestCaseRead
    relevance_score: int
    matched_terms: list[str]


class DataServiceSearchResponse(BaseModel):
    project_id: int
    query: str
    candidates: list[DataServiceSearchCandidate]


# ===== Semantic search =====

class DataServiceSemanticCandidate(BaseModel):
    test_case: DataServiceTestCaseRead
    cosine_distance: float
    similarity_score: float


class DataServiceSemanticResponse(BaseModel):
    project_id: int
    query: str
    embedding_provider: str
    embedding_model: str
    candidates: list[DataServiceSemanticCandidate]


class DataServiceClient:
    """
    HTTP-клиент для вызова data_service.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def search_test_cases(
        self,
        project_id: int,
        query: str,
        limit: int,
    ) -> list[RetrievalCandidate]:
        url = f"{self.base_url}/api/v1/projects/{project_id}/test-cases/search"
        payload = {
            "query": query,
            "limit": limit,
        }

        data = await self._post_json(url=url, payload=payload)
        parsed = DataServiceSearchResponse.model_validate(data)

        return [
            RetrievalCandidate(
                source_test_case_id=item.test_case.id,
                title=item.test_case.title,
                raw_text=item.test_case.raw_text,
                normalized_score=item.relevance_score,
                retrieval_score=float(item.relevance_score),
                matched_terms=item.matched_terms,
                explanation=None,
            )
            for item in parsed.candidates
        ]

    async def semantic_search_test_cases(
        self,
        project_id: int,
        query: str,
        limit: int,
    ) -> list[RetrievalCandidate]:
        url = f"{self.base_url}/api/v1/projects/{project_id}/test-cases/semantic-search"
        payload = {
            "query": query,
            "limit": limit,
        }

        data = await self._post_json(url=url, payload=payload)
        parsed = DataServiceSemanticResponse.model_validate(data)

        return [
            RetrievalCandidate(
                source_test_case_id=item.test_case.id,
                title=item.test_case.title,
                raw_text=item.test_case.raw_text,
                normalized_score=round(item.similarity_score * 1000),
                retrieval_score=item.similarity_score,
                matched_terms=[],
                explanation=None,
            )
            for item in parsed.candidates
        ]

    async def _post_json(
        self,
        url: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(20.0, connect=5.0)
            ) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            return response.json()

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