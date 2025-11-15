from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    id: int | None
    user_id: int | None

    refresh_token_hash: str | None

    issued_at: datetime | None
    expires_at: datetime | None

    ip_address: str | None
    user_agent: str | None

    is_reboked: bool | None

    def to_dict(self) -> dict:
        return self.model_dump(exclude={"id", "expires_at"})


class TokenCreateSchema(BaseModel):
    user_id: int | None

    refresh_token_hash: str | None

    ip_address: str | None
    user_agent: str | None

    is_reboked: bool | None

    def to_dict(self) -> dict:
        return self.model_dump()
