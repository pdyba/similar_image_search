import logging

import use_cases
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response

router = APIRouter()


logger = logging.getLogger(__name__)


@router.get("/similar/{img_id}")
async def similar_images(img_id: str, limit: int = 10, precision: float = 0.99) -> Response:
    """enables client to find similar images to the one for which ID was provided"""
    data = use_cases.find_similar_images_using_id(img_id, limit, precision)
    if data is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return JSONResponse(
        {
            "id": img_id,
            "similar_images": data,
        }
    )
