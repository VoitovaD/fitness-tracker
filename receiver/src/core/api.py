from ninja import NinjaAPI

from internal.api import internal_router
from workout.api import test_router


api = NinjaAPI(
    title="API",
    version="1.0.0",
)

# api.add_router("/internal", internal_router)
api.add_router("", internal_router)
api.add_router("", test_router)


# health_api = NinjaAPI()
# health_api.add_router("", internal_router)

# main_api = NinjaAPI()
# main_api.add_router("/api/v1", main_router)

# urlpatterns = [
#     path("", health_api.urls),
#     path("api/v1/", main_api.urls),
# ]
# main_api.add_router("/api/v1", test_router)