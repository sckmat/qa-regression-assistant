from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from services.user_service.app.core.config import settings
from services.user_service.app.models.base import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"
    __table_args__ = {"schema": settings.user_service_db_schema}

    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.user_service_db_schema}.users.id"),
        primary_key=True,
    )

    default_search_mode: Mapped[str] = mapped_column(
        String(50),
        default="semantic_llm",
    )

    preferred_llm_provider: Mapped[str] = mapped_column(
        String(50),
        default="openai",
    )