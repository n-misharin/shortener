from shortener.endpoints.health_check import api_router as health_router

routes_list = [
    health_router,
]

__all__ = [
    'routes_list',
]
