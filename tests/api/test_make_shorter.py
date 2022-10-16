import pytest
from url_normalize import url_normalize


class TestMakeShorterEndpoint:
    def test_add_new_url(self, client):
        data = {
            "long_url": "https://fastapi.tiangolo.com/"
        }
        response = client.post(
            "/api/v1/link/make_shorter",
            json=data
        )
        assert response.status_code == 200
        assert "short_url" in response.json().keys()
        assert "id" in response.json().keys()
        assert url_normalize(response.json()["long_url"]) == data["long_url"]

    def test_invalid_url(self, client):
        data = {
            "long_url": "Hello"
        }
        response = client.post(
            "/api/v1/link/make_shorter",
            json=data
        )
        assert response.status_code == 422



