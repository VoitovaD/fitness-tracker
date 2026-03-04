from ninja import NinjaAPI

from internal.api import internal_router


api = NinjaAPI(
    title="API",
    version="1.0.0",
)

api.add_router("/internal", internal_router)