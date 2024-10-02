from db import MilvusConnector
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

router = APIRouter()


@router.get("/health", tags=["health"])
def health() -> Response:
    stats = MilvusConnector().get_collection_stats()
    return JSONResponse({"status": "ok" if stats else "error"}, status_code=200 if stats else 500)
