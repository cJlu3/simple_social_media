import datetime as dt

from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    user_id: int

    refresh_token_hash: str

    issued_at: dt.datetime
    expires_at: dt.datetime

    ip_address: str | None
    user_agent: str | None

    is_reboked: bool = Field(default=False)

    def to_dict(self) -> dict:
        return self.model_dump()

    def __str__(self) -> str:
        line = f"\n\
            user_id             = {self.user_id}\n\
            refresh_token_hash  = {self.refresh_token_hash}\n\
            issued_at           = {self.issued_at}\n\
            expires_at          = {self.expires_at}\n\
            ip_address          = {self.ip_address}\n\
            user_agent          = {self.user_agent}\n\
            is_reboked          = {self.is_reboked}"
        return line
