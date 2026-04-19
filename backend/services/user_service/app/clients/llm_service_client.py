from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError

from services.user_service.app.schemas.retrieval_candidate import RetrievalCandidate


class LLMRerankCandidateRequest(BaseModel):
    test_case_id: int
    title: str
    raw_text: str
    retrieval_score: float | None = None


class LLMRerankRequest(BaseModel):
    change_summary: str
    top_n: int
    candidates: list[LLMRerankCandidateRequest]


class LLMRerankedItem(BaseModel):
    test_case_id: int
    is_relevant: bool
    llm_score: int
    explanation: str


class LLMRerankResponse(BaseModel):
    provider: str
    model: str
    items: list[LLMRerankedItem]


class LLMServiceClient:
    """
    HTTP-клиент для вызова llm_service.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def rerank_candidates(
        self,
        change_summary: str,
        candidates: list[RetrievalCandidate],
        top_n: int,
    ) -> list[RetrievalCandidate]:
        request_payload = LLMRerankRequest(
            change_summary=change_summary,
            top_n=top_n,
            candidates=[
                LLMRerankCandidateRequest(
                    test_case_id=item.source_test_case_id,
                    title=item.title,
                    raw_text=item.raw_text,
                    retrieval_score=item.retrieval_score,
                )
                for item in candidates
            ],
        )

        data = await self._post_json(
            url=f"{self.base_url}/api/v1/rerank",
            payload=request_payload.model_dump(),
        )
        parsed = LLMRerankResponse.model_validate(data)

        # Сопоставляем ответ LLM с исходными retrieval-кандидатами,
        # чтобы не потерять title/raw_text.
        original_map = {
            candidate.source_test_case_id: candidate
            for candidate in candidates
        }

        reranked: list[RetrievalCandidate] = []

        for item in parsed.items:
            original = original_map.get(item.test_case_id)
            if original is None:
                continue

            reranked.append(
                RetrievalCandidate(
                    source_test_case_id=original.source_test_case_id,
                    title=original.title,
                    raw_text=original.raw_text,
                    normalized_score=item.llm_score,
                    retrieval_score=original.retrieval_score,
                    matched_terms=original.matched_terms,
                    explanation=item.explanation,
                )
            )

        return reranked

    async def _post_json(
        self,
        url: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(40.0, connect=5.0)
            ) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            return response.json()

        except httpx.ConnectError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Cannot connect to llm_service: {exc}",
            ) from exc

        except httpx.HTTPStatusError as exc:
            response_text = exc.response.text
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "llm_service returned an error. "
                    f"Status={exc.response.status_code}, body={response_text}"
                ),
            ) from exc

        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Invalid response format from llm_service: {exc}",
            ) from exc

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Request to llm_service failed: {exc}",
            ) from exc