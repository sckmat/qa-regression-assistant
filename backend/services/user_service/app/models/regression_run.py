from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.user_service.app.core.config import settings
from services.user_service.app.models.base import Base


class RegressionRun(Base):
    """
    Таблица запусков анализа регресса.
    """

    __tablename__ = "regression_runs"
    __table_args__ = {"schema": settings.user_service_db_schema}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{settings.user_service_db_schema}.projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    change_summary: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="created",
        server_default="created",
    )

    result_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(back_populates="regression_runs")

    candidates: Mapped[list["RegressionRunCandidate"]] = relationship(
        back_populates="regression_run",
        cascade="all, delete-orphan",
    )