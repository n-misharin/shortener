import random
import string

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from shortener.config import get_settings
from shortener.db.models import URLStorage
from shortener.schemas.make_shorter import MakeShorterRequest


async def make_short(session: AsyncSession, url: MakeShorterRequest) -> str:
    exist_query = select(exists().where(URLStorage.long_url == url.long_url))
    exist = await session.scalar(exist_query)
    if exist:
        # TODO:
        raise Exception

    # TODO: generate string
    while True:
        suffix = "".join(random.choices(string.digits + string.ascii_letters, k=5))
        exist_query = select(exists().where(URLStorage.short_url == suffix))
        exist = await session.scalar(exist_query)
        if not exist:
            break
    return url_from_suffix(suffix)


def url_from_suffix(suffix: str) -> str:
    settings = get_settings()
    short_url = f"{settings.APP_HOST}:{settings.APP_PORT}{settings.PATH_PREFIX}/{suffix}"
    return short_url
