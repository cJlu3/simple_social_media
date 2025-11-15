from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.posts.schemas import (
    PostCreateSchema,
    PostUpdateSchema,
    PostSchema,
    CommentCreateSchema,
)
from src.posts.service import PostService
from src.posts.middleware import get_current_user_id, get_current_user_id_optional

app = FastAPI(
    title="Posts Service", description="Сервис для работы с постами", version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/v1/posts", response_model=PostSchema, status_code=status.HTTP_201_CREATED
)
async def create_post(
    post_data: PostCreateSchema, current_user_id: int = Depends(get_current_user_id)
):
    """Создает новый пост"""
    return await PostService.create_post(current_user_id, post_data)


@app.get("/api/v1/posts/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: int, current_user_id: Optional[int] = Depends(get_current_user_id_optional)
):
    """Получает пост по ID"""
    return await PostService.get_post(post_id, current_user_id)


@app.get("/api/v1/posts", response_model=List[PostSchema])
async def get_posts_feed(
    limit: int = 20,
    offset: int = 0,
    current_user_id: Optional[int] = Depends(get_current_user_id_optional),
):
    """Получает ленту постов"""
    if current_user_id:
        return await PostService.get_feed(current_user_id, limit, offset)
    else:
        # Для неаутентифицированных пользователей возвращаем публичные посты
        return await PostService.get_feed(0, limit, offset)


@app.get("/api/v1/users/{user_id}/posts", response_model=List[PostSchema])
async def get_user_posts(user_id: int, limit: int = 20, offset: int = 0):
    """Получает посты пользователя"""
    return await PostService.get_user_posts(user_id, limit, offset)


@app.put("/api/v1/posts/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int,
    post_data: PostUpdateSchema,
    current_user_id: int = Depends(get_current_user_id),
):
    """Обновляет пост (только автор)"""
    return await PostService.update_post(post_id, current_user_id, post_data)


@app.delete("/api/v1/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int, current_user_id: int = Depends(get_current_user_id)
):
    """Удаляет пост (только автор)"""
    await PostService.delete_post(post_id, current_user_id)
    return None


@app.get("/api/v1/posts/{post_id}/comments", response_model=List[PostSchema])
async def get_comments(post_id: int):
    """Получает комментарии к посту"""
    return await PostService.get_comments(post_id)


@app.post(
    "/api/v1/posts/{post_id}/comments",
    response_model=PostSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    post_id: int,
    comment_data: CommentCreateSchema,
    current_user_id: int = Depends(get_current_user_id),
):
    """Создает комментарий к посту"""
    return await PostService.create_comment(post_id, current_user_id, comment_data)


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "posts-service"}
