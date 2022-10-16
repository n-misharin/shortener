from fastapi.testclient import TestClient

from shortener import __version__


def test_version():
    assert __version__ == '0.1.0'


def test_fastapi(client: TestClient):
    response = client.post(
        "api/v1/link/make_shorter",
        json={
            "long_url": "http://yandex.ru"
        }
    )
    assert response.status_code == 200
