from api.v1 import download, health, similar, upload
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(upload.router)
api_router.include_router(download.router)
api_router.include_router(similar.router)
