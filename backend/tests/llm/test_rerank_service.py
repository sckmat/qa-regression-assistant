import pytest

from services.llm_service.app.services.rerank_service import RerankService
from services.llm_service.app.schemas.rerank import (
    RerankRequest,
    RerankCandidateInput,
)


class FakeProvider:
    async def rerank(self, change_summary, candidates, top_n):
        return type("obj", (), {
            "items": [
                type("item", (), {
                    "test_case_id": 1,
                    "is_relevant": True,
                    "llm_score": 90,
                    "explanation": "good",
                }),
                type("item", (), {
                    "test_case_id": 2,
                    "is_relevant": False,
                    "llm_score": 10,
                    "explanation": "bad",
                }),
            ]
        })


@pytest.mark.asyncio
async def test_rerank_filters_and_sorts():
    service = RerankService()
    service.provider = FakeProvider()

    payload = RerankRequest(
        provider="ollama",
        change_summary="login change",
        candidates=[
            RerankCandidateInput(
                test_case_id=1,
                title="Login success",
                raw_text="text",
            ),
            RerankCandidateInput(
                test_case_id=2,
                title="Other test",
                raw_text="text",
            ),
        ],
        top_n=5,
    )

    result = await service.rerank(payload)

    assert len(result.items) == 1
    assert result.items[0].test_case_id == 1