import use_cases
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse, Response

router = APIRouter()


@router.post("/upload")
async def receive_image(file: UploadFile) -> Response:
    """enables client to upload an image."""
    file_format = file.filename.rsplit(".", maxsplit=1)[-1]
    file_id = use_cases.upload_image(file.file, file_format)
    return JSONResponse({"id": file_id})
