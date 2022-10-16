from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shortener.db.connection.session import get_session
from shortener.db.models.url import URLStorage
from shortener.schemas.make_shorter import MakeShorterRequest, MakeShorterResponse
from shortener.utils.make_shorter import make_short

api_router = APIRouter(prefix="/link")


@api_router.post(
    "/make_shorter",
    response_model=MakeShorterResponse,
    status_code=status.HTTP_200_OK,
)
async def make_shorter(
        data: MakeShorterRequest,
        session: AsyncSession = Depends(get_session),
):
    result = await make_short(session, data)
    return f"{data.long_url} -> {result}"
