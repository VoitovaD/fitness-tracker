from fastapi import APIRouter
from config import settings
from app.api.v1 import test

api_router_v1 = APIRouter(prefix=settings.API_PREFIX)
api_router_v1.include_router(
    test.router,
    prefix="/test"
)