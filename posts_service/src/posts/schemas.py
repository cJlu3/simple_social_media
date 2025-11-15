from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PostCreateSchema(BaseModel):
    """Схема для создания поста"""

    header: str = Field(
        ..., min_length=1, max_length=255, description="Заголовок поста"
    )
    content: str = Field(default="", max_length=10000, description="Содержимое поста")
    tags: List[str] = Field(default=[], description="Теги поста")
    media: Optional[List[str]] = Field(
        default=None, description="Ссылки на медиа файлы"
    )
    parent_post_id: Optional[int] = Field(
        default=None, description="ID родительского поста (для комментариев)"
    )


class PostUpdateSchema(BaseModel):
    """Схема для обновления поста"""

    header: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=10000)
    tags: Optional[List[str]] = None
    media: Optional[List[str]] = None
    is_visible: Optional[bool] = None


class PostSchema(BaseModel):
    """Схема поста для ответа"""

    id: int
    author_id: int
    parent_post_id: Optional[int] = None
    header: str
    content: str
    tags: List[str]
    media: Optional[List[str]] = None
    created_at: datetime
    is_deleted: bool
    is_visible: bool
    likes_count: int = 0
    reposts_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    is_reposted: bool = False


class CommentCreateSchema(BaseModel):
    """Схема для создания комментария"""

    content: str = Field(
        ..., min_length=1, max_length=10000, description="Содержимое комментария"
    )
    tags: List[str] = Field(default=[], description="Теги комментария")
    media: Optional[List[str]] = Field(
        default=None, description="Ссылки на медиа файлы"
    )
