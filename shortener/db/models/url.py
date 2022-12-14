from sqlalchemy import Column, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from shortener.db import DeclarativeBase


class URLStorage(DeclarativeBase):
    __tablename__ = "url_storage"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        doc="Unique id",
    )

    long_url = Column(
        "long_url",
        TEXT,
        nullable=False,
        index=True,
        unique=True,
        doc="Long URL",
    )

    short_url = Column(
        "short_url",
        TEXT,
        nullable=False,
        index=True,
        unique=True,
        doc="Suffix of short URL",
    )

    # click_count = Column(
    #     "click_count",
    #     INTEGER,
    #     nullable=False,
    #     default=0,
    #     doc="The number of clicks on the link"
    # )
