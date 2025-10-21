from typing import List
from fastapi import FastAPI
from src.posts.schemas import PostSchema
from src.posts.service import PostService
from src.api.schemas import ResponseData, ResponseOK

app = FastAPI()


@app.post("/api/v1/posts", response_model=ResponseOK)
async def add_post(new_post: PostSchema) -> dict:
    await PostService.add(new_post)
    return {"success": True}

@app.get("/api/v1/posts", response_model=ResponseData)
async def get_all_posts(
    author_id: int | None = None,
    parent_post_id: int | None = None,
    header: str | None = None,
    content: str | None = None,
    tags: List[str] | None = None,
    media: List[str] | None = None,
    is_deleted: bool | None = None,
    is_visible: bool | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict:
    data = await PostService.list(
        author_id = author_id,
        parent_post_id = parent_post_id,
        header = header,
        content = content,
        tags = tags,
        media = media,
        is_deleted = is_deleted,
        is_visible = is_visible,
        limit = limit,
        offset = offset
    )
    return {"success": True, "data": data}

@app.get("/api/v1/posts/count", response_model=ResponseData)
async def count_all_posts() -> dict:
    count = await PostService.count()
    return {"success": True, "data": count}


@app.get("/api/v1/posts/{post_id}", response_model=ResponseData)
async def get_post_by_id(post_id: int) -> dict:
    data = await PostService.get(post_id)
    return {"success": True, "data": data}

@app.get("/api/v1/posts/{post_id}/comments", response_model=ResponseData)
async def get_comments(post_id: int) -> dict:
    data = await PostService.get_comments(post_id)
    return {"success": True, "data": data}

@app.delete("/api/v1/posts", response_model=ResponseOK)
async def delete_all_posts() -> dict:
    await PostService.delete_all()
    return {"success": True}

@app.delete("/api/v1/posts/{post_id}", response_model=ResponseOK)
async def delete_token_by_id(post_id: int) -> dict:
    await PostService.delete(post_id=post_id)
    return {"success": True}
