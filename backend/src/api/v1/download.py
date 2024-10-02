import use_cases
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response

router = APIRouter()


@router.get("/download/{img_id}")
async def download_image(img_id: str) -> Response:
    """enables client to download the original image."""
    details = use_cases.get_image_by_id(img_id)
    if not details:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(details)
