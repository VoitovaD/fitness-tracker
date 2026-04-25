from fastapi import APIRouter


router = APIRouter()

@router.get("/my_endpoint", summary="test", tags=["test"])
def ping() -> dict[str, str]:
    return {"message": "ok"}