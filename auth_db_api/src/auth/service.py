from datetime import datetime
from src.auth.repository import TokensRepository
from src.auth.schemas import TokenSchema

class TokenService:
    @classmethod
    async def add (cls, token: TokenSchema):
        token_dict = token.to_dict()
        await TokensRepository.add(token_dict)

    @classmethod
    async def get(cls, token_id: int):
        token = await TokensRepository.get(token_id)
        res = TokenSchema.model_validate(token, from_attributes=True)
        return res

    @classmethod
    async def list(
        cls,
        user_id: int | None = None,
        refresh_token_hash: str | None = None,
        issued_at: datetime | None = None,
        expires_at: datetime | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        is_reboked: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        filter = {
            k: v
            for k, v in {
                "user_id": user_id,
                "refresh_token_hash": refresh_token_hash,
                "issued_at": issued_at,
                "expires_at": expires_at,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "is_reboked": is_reboked,

            }.items()
            if v is not None
        }
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
