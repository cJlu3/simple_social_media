from datetime import datetime, timezone
from typing import List

from sqlalchemy import ARRAY, JSON, TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int]
    parent_post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), nullable=True)

    header: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(nullable=True, default="")
    tags: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True, default=[])
    media: Mapped[List[str] | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
