from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class Tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]

    refresh_token_hash: Mapped[str]

    issued_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    ip_address: Mapped[str | None]
    user_agent: Mapped[str | None]

    is_reboked: Mapped[bool] = mapped_column(default=False)
