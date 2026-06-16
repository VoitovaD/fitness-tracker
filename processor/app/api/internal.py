from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse, Response
import asyncpg

from config import settings



router_healthcheck = APIRouter()


@router_healthcheck.get(
    "/",
    tags=["healthcheck"],
    response_class=Response,
)
async def get_healthcheck() -> Response:
    return Response(content="OK", status_code=status.HTTP_200_OK)


@router_healthcheck.get("/db", tags=["healthcheck"], response_class=Response)
async def readiness() -> Response:
    try:
        conn = await asyncpg.connect(
            host=settings.POSTGRES_HOST,
            port=int(settings.PGPORT),
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            timeout=5.0,
        )
        try:
            await conn.execute("SELECT 1")
        finally:
            await conn.close()
    except Exception:
        return Response(content="DB unavailable", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(content="OK", status_code=status.HTTP_200_OK)
