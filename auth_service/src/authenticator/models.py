from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from core import Base

class tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    access_token: Mapped[str]
    refresh_token: Mapped[str]
