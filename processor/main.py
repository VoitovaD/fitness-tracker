import logging
from fastapi import FastAPI, APIRouter
import uvicorn

from app.api.internal import router_healthcheck
from app.api.routes import api_router_v1
from config import settings





def app_factory() -> FastAPI:
    app = FastAPI(
        docs_url=f"{settings.API_PREFIX}/docs/",
        openapi_url=f"{settings.API_PREFIX}/openapi.json/",
    )
    logging.info("Start Processor app")
    app.include_router(api_router_v1)
    app.include_router(router_healthcheck)
    return app


app = app_factory()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
