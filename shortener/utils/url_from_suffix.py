from shortener.config import get_settings


def url_from_suffix(suffix: str) -> str:
    settings = get_settings()
    return f"{settings.APP_HOST}:{settings.APP_PORT}/{suffix}"
