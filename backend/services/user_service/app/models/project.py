from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.user_service.app.core.config import settings
from services.user_service.app.models.base import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": settings.user_service_db_schema}

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    owner_user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{settings.user_service_db_schema}.users.id"),
        index=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    owner: Mapped["User"] = relationship(
        back_populates="projects"
    )

    regression_runs: Mapped[list["RegressionRun"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )