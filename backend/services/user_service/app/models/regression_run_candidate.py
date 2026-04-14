from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.user_service.app.core.config import settings
from services.user_service.app.models.base import Base


class RegressionRunCandidate(Base):
    """
    Таблица найденных кандидатов для конкретного запуска анализа.

    Здесь храним уже не "текстовое summary", а структурированный результат:
    - какой test case был найден;
    - с каким score;
    - по каким matched terms.
    """

    __tablename__ = "regression_run_candidates"
    __table_args__ = {"schema": settings.user_service_db_schema}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    regression_run_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{settings.user_service_db_schema}.regression_runs.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # id тест-кейса из data_service
    source_test_case_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    relevance_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # Сохраняем список совпавших слов как JSON-массив.
    matched_terms: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    regression_run: Mapped["RegressionRun"] = relationship(
        back_populates="candidates",
    )