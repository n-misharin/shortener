import random
import string

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from shortener.db.models import URLStorage
from shortener.schemas.make_shorter import MakeShorterRequest


async def make_short(session: AsyncSession, url: MakeShorterRequest) -> URLStorage:
    exist = await get_url_by_long(session, url.long_url)
    if exist:
        return exist

    # TODO: generate string
    while True:
        suffix = "".join(random.choices(string.digits + string.ascii_letters, k=5))
        exist_query = select(exists().where(URLStorage.short_url == suffix))
        exist = await session.scalar(exist_query)
        if not exist:
            break

    return await add_long_url(session, url.long_url, suffix)


async def get_url_by_long(session: AsyncSession, long_url: str) -> URLStorage | None:
    query = select(URLStorage).where(URLStorage.long_url == long_url)
    return await session.scalar(query)


async def add_long_url(session: AsyncSession, long_url: str, suffix: str) -> URLStorage:
    new_url = URLStorage(long_url=long_url, short_url=suffix)
    # TODO: exception
    session.add(new_url)
    await session.commit()
    await session.refresh(new_url)
    return new_url
