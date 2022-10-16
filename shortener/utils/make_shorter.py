import random
import string

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from shortener.db.models import URLStorage
from shortener.schemas.make_shorter import MakeShorterRequest


async def make_short(session: AsyncSession, url: MakeShorterRequest) -> URLStorage:
    query = select(URLStorage).where(URLStorage.long_url == url.long_url)
    exist = await session.scalar(query)
    if exist:
        return exist

    # TODO: generate string
    while True:
        suffix = "".join(random.choices(string.digits + string.ascii_letters, k=5))
        exist_query = select(exists().where(URLStorage.short_url == suffix))
        exist = await session.scalar(exist_query)
        if not exist:
            break

    new_url = URLStorage(
        long_url=url.long_url,
        short_url=suffix,
    )
    session.add(new_url)
    await session.commit()
    await session.refresh(new_url)

    return new_url
