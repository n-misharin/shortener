import pytest
from url_normalize import url_normalize
from starlette import status

from shortener.utils import url_from_suffix
from shortener.utils.make_shorter import get_url_by_long


class TestMakeShorterEndpoint:
    @staticmethod
    def get_url():
        return "/api/v1/link/make_shorter"

    @staticmethod
    def get_work_site_url():
        return "https://fastapi.tiangolo.com/"

    async def test_add_url(self, client, database):
        url = TestMakeShorterEndpoint.get_work_site_url()

        db_url = await get_url_by_long(database, url)
        assert db_url is None

        response = await client.post(
            TestMakeShorterEndpoint.get_url(),
            json={"long_url": url}
        )

        db_url = await get_url_by_long(database, url)
        assert url_normalize(db_url.long_url) == url

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["short_url"] == url_from_suffix(db_url.short_url)
        assert response.json()["id"] == str(db_url.id)
        assert url_normalize(response.json()["long_url"]) == url

    async def test_add_vip_url(self, client, database):
        url = TestMakeShorterEndpoint.get_work_site_url()
        data = {
            "long_url": url,
            "suffix": "vip_suffix"
        }

        response = await client.post(TestMakeShorterEndpoint.get_url(), json=data)

        db_url = await get_url_by_long(database, url)
        assert url_normalize(db_url.long_url) == url

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["short_url"] == url_from_suffix(db_url.short_url)
        assert response.json()["id"] == str(db_url.id)
        assert url_normalize(response.json()["long_url"]) == url

    @pytest.mark.parametrize(
        "url",
        [
            "hello",
            "asdf/asd/fa/fsd"
        ]
    )
    async def test_invalid_url(self, client, database, url):
        response = await client.post(
            TestMakeShorterEndpoint.get_url(),
            json={"long_url": url}
        )

        db_url = await get_url_by_long(database, url)
        assert db_url is None

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "response_data",
        [
            {"key": "value"},
            {"long_uri": "http://ya.ru"},
        ]
    )
    async def test_invalid_schema(self, client, response_data):
        response = await client.post(
            TestMakeShorterEndpoint.get_url(),
            json=response_data
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
