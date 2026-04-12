from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.user_service.app.core.config import settings
from services.user_service.app.models.base import Base


class Project(Base):
    """
    Таблица проектов.

    Это верхнеуровневая сущность, вокруг которой строится пользовательский сценарий.
    В будущем к проекту будут привязаны тест-кейсы, импортированные артефакты,
    результаты retrieval и прочие сущности.
    """

    __tablename__ = "projects"
    __table_args__ = {"schema": settings.user_service_db_schema}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    regression_runs: Mapped[list["RegressionRun"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
