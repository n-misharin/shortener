import random
import string

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from shortener.db.models import URLStorage


BASE_SUFFIX_LENGTH = 5


class ExistURLException(Exception):
    pass


def generate_random_suffix(length: int) -> str:
    return "".join(random.choices(string.digits + string.ascii_letters, k=length))


async def generate_not_exist_url(session: AsyncSession, length: int) -> str:
    # TODO: new algorithm
    while True:
        suffix = generate_random_suffix(length)
        exist_url = await get_url_by_suffix(session, suffix)
        if not exist_url:
            break
    return suffix


async def make_short(session: AsyncSession, long_url: str) -> URLStorage:
    exist_long = await get_url_by_long(session, long_url)
    if exist_long:
        return exist_long

    suffix = await generate_not_exist_url(session, BASE_SUFFIX_LENGTH)

    return await add_url(session, long_url, suffix)


async def make_vip(session: AsyncSession, long_url: str, suffix: str) -> URLStorage:
    exist_long = await get_url_by_long(session, long_url)
    if exist_long:
        return exist_long

    exist_short = await get_url_by_suffix(session, suffix)
    if exist_short:
        raise ExistURLException(f"URL with suffix=`{suffix}` already exist")

    return await add_url(session, long_url, suffix)


async def get_url_by_long(session: AsyncSession, long_url: str) -> URLStorage | None:
    query = select(URLStorage).where(URLStorage.long_url == long_url)
    return await session.scalar(query)


async def get_url_by_suffix(session: AsyncSession, suffix: str) -> URLStorage | None:
    query = select(URLStorage).where(URLStorage.short_url == suffix)
    return await session.scalar(query)


async def add_url(session: AsyncSession, long_url: str, suffix: str) -> URLStorage:
    # TODO: URL validation and suffix validation
    new_url = URLStorage(long_url=long_url, short_url=suffix)
    try:
        session.add(new_url)
        await session.commit()
        await session.refresh(new_url)
    except IntegrityError as exception:
        raise ExistURLException(
            f"URL with suffix=`{suffix}` or long_url=`{long_url}` already exist") from exception
    return new_url
