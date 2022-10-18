from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shortener.db.connection.session import get_session
from shortener.schemas.make_shorter import MakeShorterRequest, ShortingURL
from shortener.utils.make_shorter import make_short, make_vip, ExistURLException

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
    if data.suffix is None:
        return await make_short(session, data.long_url)
    try:
        return await make_vip(session, data.long_url, data.suffix)
    except ExistURLException as exist_exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Suffix is busy"
        ) from exist_exc
