from typing import Optional, List
from fastapi import HTTPException, status
from src.posts.schemas import (
    PostCreateSchema,
    PostUpdateSchema,
    PostSchema,
    CommentCreateSchema,
)
from src.posts.http_clients import PostsDBClient, UsersDBClient


class PostService:
    """Сервис для работы с постами"""

    @staticmethod
    async def create_post(author_id: int, post_data: PostCreateSchema) -> PostSchema:
        """Создает новый пост"""
        post_dict = {
            "author_id": author_id,
            "header": post_data.header,
            "content": post_data.content,
            "tags": post_data.tags,
            "media": post_data.media,
            "parent_post_id": post_data.parent_post_id,
            "is_deleted": False,
            "is_visible": True,
        }

        try:
            await PostsDBClient.create_post(post_dict)
            # Получаем созданный пост (нужно будет добавить метод получения последнего поста)
            # Пока что возвращаем упрощенную версию
            posts = await PostsDBClient.get_posts(author_id=author_id, limit=1)
            if posts:
                post = posts[0]
                return PostSchema(
                    id=post["id"],
                    author_id=post["author_id"],
                    parent_post_id=post.get("parent_post_id"),
                    header=post["header"],
                    content=post["content"],
                    tags=post.get("tags", []),
                    media=post.get("media"),
                    created_at=post["created_at"],
                    is_deleted=post.get("is_deleted", False),
                    is_visible=post.get("is_visible", True),
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании поста",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании поста: {str(e)}",
            )

    @staticmethod
    async def get_post(
        post_id: int, current_user_id: Optional[int] = None
    ) -> PostSchema:
        """Получает пост по ID"""
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден"
            )

        if post.get("is_deleted"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден"
            )

        # Получаем статистику (лайки, репосты, комментарии)
        # Пока что возвращаем базовую информацию
        return PostSchema(
            id=post["id"],
            author_id=post["author_id"],
            parent_post_id=post.get("parent_post_id"),
            header=post["header"],
            content=post["content"],
            tags=post.get("tags", []),
            media=post.get("media"),
            created_at=post["created_at"],
            is_deleted=post.get("is_deleted", False),
            is_visible=post.get("is_visible", True),
        )

    @staticmethod
    async def get_feed(
        current_user_id: int, limit: int = 20, offset: int = 0
    ) -> List[PostSchema]:
        """Получает ленту постов (пока что просто все посты)"""
        posts = await PostsDBClient.get_posts(limit=limit, offset=offset)
        result = []
        for post in posts:
            result.append(
                PostSchema(
                    id=post["id"],
                    author_id=post["author_id"],
                    parent_post_id=post.get("parent_post_id"),
                    header=post["header"],
                    content=post["content"],
                    tags=post.get("tags", []),
                    media=post.get("media"),
                    created_at=post["created_at"],
                    is_deleted=post.get("is_deleted", False),
                    is_visible=post.get("is_visible", True),
                )
            )
        return result

    @staticmethod
    async def get_user_posts(
        user_id: int, limit: int = 20, offset: int = 0
    ) -> List[PostSchema]:
        """Получает посты пользователя"""
        posts = await PostsDBClient.get_posts(
            author_id=user_id, limit=limit, offset=offset
        )
        result = []
        for post in posts:
            result.append(
                PostSchema(
                    id=post["id"],
                    author_id=post["author_id"],
                    parent_post_id=post.get("parent_post_id"),
                    header=post["header"],
                    content=post["content"],
                    tags=post.get("tags", []),
                    media=post.get("media"),
                    created_at=post["created_at"],
                    is_deleted=post.get("is_deleted", False),
                    is_visible=post.get("is_visible", True),
                )
            )
        return result

    @staticmethod
    async def update_post(
        post_id: int, author_id: int, post_data: PostUpdateSchema
    ) -> PostSchema:
        """Обновляет пост (только автор может обновлять)"""
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден"
            )

        if post["author_id"] != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав на редактирование этого поста",
            )

        # Обновление поста (нужно добавить метод в PostsDBClient)
        # Пока что возвращаем существующий пост
        return await PostService.get_post(post_id, author_id)

    @staticmethod
    async def delete_post(post_id: int, author_id: int) -> bool:
        """Удаляет пост (только автор может удалять)"""
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден"
            )

        if post["author_id"] != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав на удаление этого поста",
            )

        return await PostsDBClient.delete_post(post_id)

    @staticmethod
    async def get_comments(post_id: int) -> List[PostSchema]:
        """Получает комментарии к посту"""
        comments = await PostsDBClient.get_comments(post_id)
        result = []
        for comment in comments:
            result.append(
                PostSchema(
                    id=comment["id"],
                    author_id=comment["author_id"],
                    parent_post_id=comment.get("parent_post_id"),
                    header=comment.get("header", ""),
                    content=comment["content"],
                    tags=comment.get("tags", []),
                    media=comment.get("media"),
                    created_at=comment["created_at"],
                    is_deleted=comment.get("is_deleted", False),
                    is_visible=comment.get("is_visible", True),
                )
            )
        return result

    @staticmethod
    async def create_comment(
        post_id: int, author_id: int, comment_data: CommentCreateSchema
    ) -> PostSchema:
        """Создает комментарий к посту"""
        # Проверяем, что пост существует
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден"
            )

        post_dict = {
            "author_id": author_id,
            "header": "",  # Комментарии без заголовка
            "content": comment_data.content,
            "tags": comment_data.tags,
            "media": comment_data.media,
            "parent_post_id": post_id,
            "is_deleted": False,
            "is_visible": True,
        }

        try:
            await PostsDBClient.create_post(post_dict)
            comments = await PostsDBClient.get_comments(post_id)
            if comments:
                comment = comments[-1]  # Последний комментарий
                return PostSchema(
                    id=comment["id"],
                    author_id=comment["author_id"],
                    parent_post_id=comment.get("parent_post_id"),
                    header=comment.get("header", ""),
                    content=comment["content"],
                    tags=comment.get("tags", []),
                    media=comment.get("media"),
                    created_at=comment["created_at"],
                    is_deleted=comment.get("is_deleted", False),
                    is_visible=comment.get("is_visible", True),
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании комментария",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании комментария: {str(e)}",
            )
