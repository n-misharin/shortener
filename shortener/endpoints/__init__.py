from shortener.endpoints.health_check import api_router as health_router
from shortener.endpoints.make_shorter import api_router as shorter_router

routes_list = [
    health_router,
    shorter_router,
]

__all__ = [
    'routes_list',
]
