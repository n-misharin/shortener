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
        doc="",
    )

    long_url = Column(
        "long_url",
        TEXT,
        nullable=False,
        index=True,
        unique=True,
        doc="",
    )

    short_url = Column(
        "short_url",
        TEXT,
        nullable=False,
        index=True,
        unique=True,
        doc="",
    )
