from pydantic import BaseModel, AnyUrl, Field


class MakeShorterRequest(BaseModel):
    long_url: AnyUrl = Field(title="URL to be shortened")


class MakeShorterResponse(MakeShorterRequest):
    short_url = AnyUrl = Field(title="Short URL")
