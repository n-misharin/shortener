import pytest
from starlette import status

from shortener.utils.make_shorter import make_short


class TestRedirectLong:
    @staticmethod
    def get_url(suffix: str):
        return f"/{suffix}"

    @pytest.mark.parametrize(
        "url",
        [
            "https://vk.com",
            "https://fastapi.tiangolo.com/deployment/concepts/#example-tools-to-restart-automatically"
        ]
    )
    async def test_valid_url_redirect(self, database, client, url):
        db_url = await make_short(database, url)
        response = await client.get(TestRedirectLong.get_url(db_url.short_url))
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
