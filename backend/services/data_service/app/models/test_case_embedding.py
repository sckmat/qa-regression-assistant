from datetime import datetime

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from services.data_service.app.core.config import settings
from services.data_service.app.models.base import Base


class TestCaseEmbedding(Base):
    __tablename__ = "test_case_embeddings"
    __table_args__ = (
        UniqueConstraint("test_case_id", name="uq_test_case_embeddings_test_case_id"),
        {"schema": settings.data_service_db_schema},  # 🔥 ключевая строка
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    test_case_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{settings.data_service_db_schema}.test_cases.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    embedding: Mapped[list[float]] = mapped_column(
        VECTOR(settings.embedding_dim),
        nullable=False,
    )

    embedding_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    indexed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )