from sqlalchemy import delete, select, func, insert

from src.core import async_session_factory
from src.users.models import Users


class UsersRepository:
    @classmethod
    async def add(cls, values: dict):
        stmt = insert(Users).values(**values)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get(cls, user_id: int):
        query = select(Users).where(Users.id == user_id)
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
        query = select(Users).filter_by(**filter).limit(limit).offset(offset)
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalars().all()
        return res

    @classmethod
    async def count(cls) -> int | None:
        query = select(func.count(Users.id))
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalar_one_or_none()
        return res

    @classmethod
    async def delete(cls, user_id: int):
        stmt = delete(Users).where(Users.id == user_id)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_all(cls):
        stmt = delete(Users)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()
