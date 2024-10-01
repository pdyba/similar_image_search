from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response


router = APIRouter()


@router.get("/health", tags=["health"])
def health() -> Response:
    # some async operation could happen here
    # example: `data = await get_all_datas()`
    return JSONResponse({"status": "ok"})
