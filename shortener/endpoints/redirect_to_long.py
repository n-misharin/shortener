from fastapi import APIRouter, Request, Depends, Path, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from shortener.db.connection.session import get_session
from shortener.db.models.url import URLStorage

api_router = APIRouter()


@api_router.get(
    "/{suffix}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_long(
        request: Request,
        suffix: str = Path(...),
        session: AsyncSession = Depends(get_session),
):
    query = select(URLStorage).where(URLStorage.short_url == suffix)
    db_url = await session.scalar(query)
    if db_url:
        return RedirectResponse(db_url.long_url)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {request.url} doesn't exist"
    )
