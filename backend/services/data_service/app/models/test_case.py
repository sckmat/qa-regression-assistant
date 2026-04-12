from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from services.data_service.app.core.config import settings
from services.data_service.app.models.base import Base


class TestCase(Base):
    """
    Таблица тест-кейсов.

    Важный момент:
    здесь хранится только `project_id` как число без foreign key на `user_service.projects`.
    Для отдельных сервисов это нормальная практика: data_service не должен напрямую зависеть
    от таблиц другого сервиса на уровне БД.
    """

    __tablename__ = "test_cases"
    __table_args__ = {"schema": settings.data_service_db_schema}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    preconditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    steps: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expected_result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)
    priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Склеенный текст, по которому удобно делать простой текстовый поиск.
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
