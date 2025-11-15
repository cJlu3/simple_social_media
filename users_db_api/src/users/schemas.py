from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int

    username: str
    avatar_url: str | None = None
    email: str
    password_hash: str | None = None

    created_at: datetime
    disactivated_at: datetime | None = None
    birth_date: datetime | None = None

    is_verified: bool = False
    is_admin: bool = False

    def to_dict(self) -> dict:
        return self.model_dump(exclude={"id"})

    # def __str__(self) -> str:
    #     line = f"\n\
    #         author_id           = {self.author_id}\n\
    #         header              = {self.header}\n\
    #         tags                = {self.tags}\n\
    #         media               = {self.media}\n\
    #         created_at          = {self.created_at}\n\
    #         is_deleted          = {self.is_deleted}"
    #     return line
