from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse, Response
from use_cases import upload_image

router = APIRouter()


@router.post("/upload")
async def receive_image(file: UploadFile) -> Response:
    """enables client to upload an image."""
    file_format = file.filename.rsplit(".", maxsplit=1)[-1]
    file_id = upload_image(file.file, file_format)
    return JSONResponse({"id": file_id})
