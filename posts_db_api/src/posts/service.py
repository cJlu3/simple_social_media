from datetime import datetime
from typing import List
from src.posts.repository import PostsRepository
from src.posts.schemas import PostSchema

class PostService:
    @classmethod
    async def add (cls, post: PostSchema):
        post_dict = post.to_dict()
        await PostsRepository.add(post_dict)

    @classmethod
    async def get(cls, post_id: int):
        post = await PostsRepository.get(post_id)
        res = PostSchema.model_validate(post, from_attributes=True)
        return res

    @classmethod
    async def get_comments(cls, post_id: int):
        comments = await PostsRepository.get_comments(post_id)
        res = []
        for item in comments:
            comment = PostSchema.model_validate(item, from_attributes=True)
            res.append(comment)
        return res

    @classmethod
    async def list(
        cls,
        author_id: int | None = None,
        parent_post_id: int | None = None,
        header: str | None = None,
        content: str | None = None,
        tags: List[str] | None = None,
        media: List[str] | None = None,
        created_at: datetime | None = None,
        is_deleted: bool | None = None,
        is_visible: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        filter = {
            k: v
            for k, v in {
                "author_id": author_id,
                "parent_post_id": parent_post_id,
                "header": header,
                "content": content,
                "tags": tags,
                "media": media,
                "created_at": created_at,
                "is_deleted": is_deleted,
                "is_visible": is_visible,
            }.items()
            if v is not None
        }
        lst = await PostsRepository.list(filter, limit=limit, offset=offset)
        res = []
        for item in lst:
            post = PostSchema.model_validate(item, from_attributes=True)
            res.append(post)
        return res

    @classmethod
    async def count(cls):
        res = await PostsRepository.count()
        return res

    @classmethod
    async def delete(cls, post_id):
        await PostsRepository.delete(post_id)

    @classmethod
    async def delete_all(cls):
        await PostsRepository.delete_all()
