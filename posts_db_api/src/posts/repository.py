from sqlalchemy import delete, select, func, insert, update

from src.core import async_session_factory
from src.posts.models import Posts


class PostsRepository:
    @classmethod
    async def add(cls, values: dict):
        stmt = insert(Posts).values(**values)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get(cls, post_id: int):
        query = select(Posts).where(Posts.id == post_id)
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalar_one()
        return res


    @classmethod
    async def list(
        cls,
        filter: dict,
        limit: int | None = None,
        offset: int | None = None,
    ):
        query = select(Posts).filter_by(**filter).limit(limit).offset(offset)
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalars().all()
        return res

    @classmethod
    async def count(cls) -> int | None:
        query = select(func.count(Posts.id))
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalar_one_or_none()
        return res

    @classmethod
    async def delete(cls, post_id: int):
        stmt = delete(Posts).where(Posts.id == post_id)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_all(cls):
        stmt = delete(Posts)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()
