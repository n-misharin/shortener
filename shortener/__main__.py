from fastapi import FastAPI

from shortener.config import get_settings
from shortener.config.default import DefaultSettings
from shortener.endpoints import routes_list


def bind_routes(application: FastAPI, settings: DefaultSettings) -> None:
    for route in routes_list:
        if "api" in route.tags:
            application.include_router(route, prefix=settings.PATH_PREFIX)
        else:
            application.include_router(route)


def create_app() -> FastAPI:
    application = FastAPI(
        title="shortener",
        description="Укорачиватель ссылок",
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
    )

    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings

    return application
