from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data_service.app.models.test_case import TestCase


class TestCaseRepository:
    """
    Репозиторий для работы с таблицей test_cases.

    Здесь нет бизнес-логики: только запросы к БД.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, test_cases: list[TestCase]) -> list[TestCase]:
        self.session.add_all(test_cases)
        await self.session.commit()
        for item in test_cases:
            await self.session.refresh(item)
        return test_cases

    async def get_all_by_project_id(self, project_id: int) -> list[TestCase]:
        result = await self.session.execute(
            select(TestCase)
            .where(TestCase.project_id == project_id)
            .order_by(TestCase.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, test_case_id: int) -> TestCase | None:
        result = await self.session.execute(
            select(TestCase).where(TestCase.id == test_case_id)
        )
        return result.scalar_one_or_none()

    async def search_candidates(
        self,
        project_id: int,
        terms: list[str],
        max_candidates: int = 200,
    ) -> list[TestCase]:
        """
        Возвращает первичный кандидатный набор.

        Для MVP используем простой подход:
        - фильтруем тест-кейсы по project_id;
        - ищем совпадения по title и raw_text через ILIKE;
        - затем уже в сервисе считаем простую relevance score.

        Это не финальный retrieval, а только базовый шаг.
        """
        base_query = select(TestCase).where(TestCase.project_id == project_id)

        if terms:
            conditions = []
            for term in terms:
                pattern = f"%{term}%"
                conditions.append(TestCase.title.ilike(pattern))
                conditions.append(TestCase.raw_text.ilike(pattern))

            base_query = base_query.where(or_(*conditions))

        result = await self.session.execute(
            base_query.order_by(TestCase.id.desc()).limit(max_candidates)
        )
        return list(result.scalars().all())
