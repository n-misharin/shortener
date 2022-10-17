import pytest
from sqlalchemy import select
from url_normalize import url_normalize

from shortener.db.models import URLStorage
from shortener.utils.make_shorter import get_url_by_long


class TestMakeShorterEndpoint:
    @staticmethod
    def get_url():
        return "/api/v1/link/make_shorter"

    @pytest.mark.parametrize(
        "url",
        [
            "https://fastapi.tiangolo.com/",
            "https://vk.com/",
            "https://fastapi.tiangolo.com/deployment/concepts/#example-tools-to-restart-automatically",
        ]
    )
    async def test_add_new_url(self, client, database, url):
        res = await get_url_by_long(database, url)
        assert res is None
        response = await client.post(
            TestMakeShorterEndpoint.get_url(),
            json={"long_url": url}
        )
        assert response.status_code == 200
        assert "short_url" in response.json().keys()
        assert "id" in response.json().keys()
        assert url_normalize(response.json()["long_url"]) == url

    @pytest.mark.parametrize(
        "url",
        [
            "hello",
            "asdf/asd/fa/fsd"
        ]
    )
    async def test_invalid_url(self, client, url):
        response = await client.post(
            "/api/v1/link/make_shorter",
            json={"long_url": url}
        )
        assert response.status_code == 422
