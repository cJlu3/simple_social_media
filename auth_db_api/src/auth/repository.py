from sqlalchemy import delete, select, func, insert, update

from src.core import async_session_factory
from src.auth.models import Tokens


class TokensRepository:
    @classmethod
    async def add(cls, values: dict):
        stmt = insert(Tokens).values(**values)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get(cls, token_id: int):
        query = select(Tokens).where(Tokens.id == token_id)
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
        query = select(Tokens).filter_by(**filter).limit(limit).offset(offset)
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalars().all()
        return res

    @classmethod
    async def count(cls) -> int | None:
        query = select(func.count(Tokens.id))
        async with async_session_factory() as session:
            query_res = await session.execute(query)
            res = query_res.scalar_one_or_none()
        return res

    @classmethod
    async def delete(cls, token_id: int):
        stmt = delete(Tokens).where(Tokens.id == token_id)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_all(cls):
        stmt = delete(Tokens)
        async with async_session_factory() as session:
            await session.execute(stmt)
            await session.commit()
