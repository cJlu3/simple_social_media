from datetime import datetime
from typing import List

from pydantic import BaseModel


class PostSchema(BaseModel):
    author_id: int

    header: str
    content: str | None = None
    tags: List[str] | None = None
    media: List[str] | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_deleted: bool | None = None

    def to_dict(self) -> dict:
        return self.model_dump()

    def __str__(self) -> str:
        line = f"\n\
            author_id           = {self.author_id}\n\
            header              = {self.header}\n\
            tags                = {self.tags}\n\
            media               = {self.media}\n\
            created_at          = {self.created_at}\n\
            updated_at          = {self.updated_at}\n\
            is_deleted          = {self.is_deleted}"
        return line
