from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shortener.db.connection.session import get_session
from shortener.schemas.make_shorter import MakeShorterRequest, ShortingURL
from shortener.utils.make_shorter import make_short

api_router = APIRouter(prefix="/link", tags=["api"])


@api_router.post(
    "/make_shorter",
    response_model=ShortingURL,
    status_code=status.HTTP_200_OK,
)
async def make_shorter(
        data: MakeShorterRequest,
        session: AsyncSession = Depends(get_session),
):
    result = await make_short(session, data)
    return result
