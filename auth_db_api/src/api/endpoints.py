from datetime import datetime
from fastapi import FastAPI
from src.auth.service import TokenService
from src.auth.schemas import TokenCreateSchema
from src.api.schemas import ResponseData, ResponseOK

app = FastAPI()


@app.post("/api/v1/tokens", response_model=ResponseOK)
async def add_token(new_token: TokenCreateSchema) -> dict:
    await TokenService.add(new_token)
    return {"success": True}

@app.get("/api/v1/tokens", response_model=ResponseData)
async def get_all_tokens(
    id: int | None = None,
    user_id: int | None = None,
    refresh_token_hash: str | None = None,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    is_reboked: bool | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict:
    filter = {
        k: v
        for k, v in {
            "id": id,
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
    data = await TokenService.list(
        filter=filter,
        limit = limit,
        offset = offset
    )
    return {"success": True, "data": data}

@app.get("/api/v1/tokens/count", response_model=ResponseData)
async def count_all_tokens() -> dict:
    count = await TokenService.count()
    return {"success": True, "data": count}

@app.delete("/api/v1/tokens", response_model=ResponseOK)
async def delete_all_tokens() -> dict:
    await TokenService.delete_all()
    return {"success": True}

@app.get("/api/v1/tokens/{token_id}", response_model=ResponseData)
async def get_token_by_id(token_id: int) -> dict:
    data = await TokenService.get(token_id)
    return {"success": True, "data": data}

@app.delete("/api/v1/tokens/{token_id}", response_model=ResponseOK)
async def delete_token_by_id(token_id: int) -> dict:
    await TokenService.delete(token_id=token_id)
    return {"success": True}
