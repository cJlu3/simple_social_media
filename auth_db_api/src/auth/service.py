from src.auth.repository import TokensRepository
from src.auth.schemas import TokenCreateSchema, TokenSchema


class TokenService:
    @classmethod
    async def add(cls, token: TokenCreateSchema):
        await TokensRepository.add(token.to_dict())

    @classmethod
    async def get(cls, token_id: int):
        token = await TokensRepository.get(token_id)
        res = TokenSchema.model_validate(token, from_attributes=True)
        return res

    @classmethod
    async def list(
        cls,
        filter: dict,
        limit: int | None = None,
        offset: int | None = None,
    ):
        lst = await TokensRepository.list(filter, limit=limit, offset=offset)
        res = []
        for item in lst:
            token = TokenSchema.model_validate(item, from_attributes=True)
            res.append(token)
        return res

    @classmethod
    async def count(cls):
        res = await TokensRepository.count()
        return res

    @classmethod
    async def delete(cls, token_id):
        await TokensRepository.delete(token_id)

    @classmethod
    async def delete_all(cls):
        await TokensRepository.delete_all()
