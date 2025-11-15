from datetime import datetime, timedelta, timezone

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class Tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)

    refresh_token_hash: Mapped[str] = mapped_column(nullable=False)

    issued_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        nullable=False,
    )

    ip_address: Mapped[str | None] = mapped_column(nullable=False)
    user_agent: Mapped[str | None] = mapped_column(nullable=False)

    is_reboked: Mapped[bool] = mapped_column(default=False, nullable=False)
