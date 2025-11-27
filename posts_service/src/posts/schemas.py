from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PostCreateSchema(BaseModel):
    """Schema for creating a post"""

    header: str = Field(
        ..., min_length=1, max_length=255, description="Post title"
    )
    content: str = Field(default="", max_length=10000, description="Post content")
    tags: List[str] = Field(default=[], description="Post tags")
    media: Optional[List[str]] = Field(
        default=None, description="Links to media files"
    )
    parent_post_id: Optional[int] = Field(
        default=None, description="Parent post ID (for comments)"
    )


class PostUpdateSchema(BaseModel):
    """Schema for updating a post"""

    header: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, max_length=10000)
    tags: List[str] | None = None
    media: List[str] | None = None
    is_visible: bool | None = None


class PostSchema(BaseModel):
    """Post schema for responses"""

    id: int
    author_id: int
    parent_post_id: int | None = None
    header: str
    content: str
    tags: List[str]
    media: List[str] | None = None
    created_at: datetime
    is_deleted: bool
    is_visible: bool
    likes_count: int = 0
    reposts_count: int = 0
    comments_count: int = 0
    is_liked: bool = False
    is_reposted: bool = False


class CommentCreateSchema(BaseModel):
    """Schema for creating a comment"""

    content: str = Field(
        ..., min_length=1, max_length=10000, description="Comment content"
    )
    tags: List[str] = Field(default=[], description="Comment tags")
    media: Optional[List[str]] = Field(
        default=None, description="Links to media files"
    )
