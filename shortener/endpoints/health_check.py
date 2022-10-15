from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shortener.db.connection.session import get_session
from shortener.db.models.url import URLStorage

api_router = APIRouter(
    prefix="/health_check",
)


@api_router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def health_check(
        _: Request,
        session: AsyncSession = Depends(get_session),
):
    # async with session as db:
    query = select(URLStorage)
    url = await session.execute(query)
    res = url.first()[0]

    return f"{res.long_url} -> {res.short_url}"
