from datetime import datetime, timezone
from typing import List

from sqlalchemy import ARRAY, JSON, TIMESTAMP, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int]

    header: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str | None] = mapped_column(nullable=True)
    tags: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    media: Mapped[List[str] | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=None,
        onupdate=datetime.now(timezone.utc),
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
