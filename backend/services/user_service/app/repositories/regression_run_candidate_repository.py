from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models.regression_run_candidate import (
    RegressionRunCandidate,
)


class RegressionRunCandidateRepository:
    """
    Repository-слой для таблицы regression_run_candidates.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(
        self,
        regression_run_id: int,
        candidates_payload: list[dict],
    ) -> list[RegressionRunCandidate]:
        entities: list[RegressionRunCandidate] = []

        for item in candidates_payload:
            entity = RegressionRunCandidate(
                regression_run_id=regression_run_id,
                source_test_case_id=item["source_test_case_id"],
                title=item["title"],
                relevance_score=item["relevance_score"],
                matched_terms=item["matched_terms"],
                explanation=item.get("explanation"),
            )
            entities.append(entity)

        self.session.add_all(entities)
        await self.session.flush()
        return entities

    async def list_by_run_id(
        self,
        regression_run_id: int,
    ) -> list[RegressionRunCandidate]:
        result = await self.session.execute(
            select(RegressionRunCandidate)
            .where(RegressionRunCandidate.regression_run_id == regression_run_id)
            .order_by(
                RegressionRunCandidate.relevance_score.desc(),
                RegressionRunCandidate.id.asc(),
            )
        )
        return list(result.scalars().all())