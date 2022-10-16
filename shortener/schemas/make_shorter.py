from pydantic import BaseModel, HttpUrl, Field, validator, UUID4
from url_normalize import url_normalize

from shortener.utils.url_from_suffix import url_from_suffix


class MakeShorterRequest(BaseModel):
    long_url: HttpUrl = Field(title="URL to be shortened")

    @validator("long_url")
    def normalize_link(cls, link: HttpUrl):
        return url_normalize(link)


class ShortingURL(BaseModel):
    id: UUID4
    long_url: HttpUrl = Field(title="URL to be shortened")
    short_url: str = Field(title="Short URL")

    @validator("short_url")
    def get_short_url(cls, suffix: str):
        return url_normalize(url_from_suffix(suffix))

    class Config:
        orm_mode = True
