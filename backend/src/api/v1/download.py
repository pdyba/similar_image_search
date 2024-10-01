from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from use_cases import get_image_by_id


router = APIRouter()


@router.get("/download/{img_id}")
async def download_image(img_id: str):
    """enables client to download the original image."""
    details = get_image_by_id(img_id)
    if not details:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(details)
