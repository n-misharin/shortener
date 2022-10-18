from typing import Optional

from pydantic import BaseModel, HttpUrl, Field, validator, UUID4
from url_normalize import url_normalize

from shortener.utils import url_from_suffix


class MakeShorterRequest(BaseModel):
    # pylint: disable=E0213
    long_url: HttpUrl = Field(title="URL to be shortened")
    suffix: Optional[str] = Field(title="Suffix for shor URL", default=None)

    @validator("long_url")
    def normalize_link(cls, link: HttpUrl): # noqa
        return url_normalize(link)


class ShortingURL(BaseModel):
    # pylint: disable=E0213
    id: UUID4
    long_url: HttpUrl = Field(title="URL to be shortened")
    short_url: str = Field(title="Short URL")

    @validator("short_url")
    def get_short_url(cls, suffix: str):
        return url_normalize(url_from_suffix(suffix))

    class Config:
        orm_mode = True
