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
    """Service for working with posts"""

    @staticmethod
    async def create_post(author_id: int, post_data: PostCreateSchema) -> PostSchema:
        """Creates a new post"""
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
            # Fetch the created post (need a method to get the latest post)
            # For now, return a simplified version
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
                detail="Error while creating post",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while creating post: {str(e)}",
            )

    @staticmethod
    async def get_post(
        post_id: int, current_user_id: int | None = None
    ) -> PostSchema:
        """Retrieves a post by ID"""
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        if post.get("is_deleted"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        # Fetch stats (likes, reposts, comments)
        # For now, return basic information
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
        """Retrieves the post feed (currently just all posts)"""
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
        """Retrieves posts for a user"""
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
        """Updates a post (only the author can update)"""
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        if post["author_id"] != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to edit this post",
            )

        # Post update (need to add a method in PostsDBClient)
        # For now, return the existing post
        return await PostService.get_post(post_id, author_id)

    @staticmethod
    async def delete_post(post_id: int, author_id: int) -> bool:
        """Deletes a post (only the author can delete)"""
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        if post["author_id"] != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this post",
            )

        return await PostsDBClient.delete_post(post_id)

    @staticmethod
    async def get_comments(post_id: int) -> List[PostSchema]:
        """Retrieves comments for a post"""
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
        """Creates a comment for a post"""
        # Verify that the post exists
        post = await PostsDBClient.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        post_dict = {
            "author_id": author_id,
            "header": "",  # Comments do not have a header
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
                comment = comments[-1]  # Latest comment
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
                detail="Error while creating comment",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while creating comment: {str(e)}",
            )
