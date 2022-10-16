import asyncio
import os
from types import SimpleNamespace
from uuid import uuid4
from httpx import AsyncClient

import pytest
from alembic.command import upgrade
from alembic.config import Config

from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from shortener.__main__ import create_app
from shortener.config import get_settings
from shortener.db.connection.session import SessionManager

from tests.utils import make_alembic_config


# @pytest.fixture(scope="session")
# def event_loop():
#     """
#     Creates event loop for tests.
#     """
#     policy = asyncio.get_event_loop_policy()
#     loop = policy.new_event_loop()
#
#     yield loop
#     loop.close()


@pytest.fixture
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = ".".join([uuid4().hex, "pytest"])
    settings.POSTGRES_DB = tmp_name
    os.environ["POSTGRES_DB"] = tmp_name

    tmp_url = settings.database_uri_sync

    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config="shortener/db/",
        name="alembic",
        pg_url=postgres,
        raiseerr=False,
        x=None
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


@pytest.fixture
async def database(
        postgres,
        migrated_postgres,
        manager: SessionManager = SessionManager()
) -> Session:
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh()
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


@pytest.fixture
def client(migrated_postgres, manager: SessionManager = SessionManager()) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    with TestClient(create_app()) as client:
        yield client
