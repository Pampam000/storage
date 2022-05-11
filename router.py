from fastapi import APIRouter
from storage.api.storage import router as storage_router
from storage.api.auth import router as auth_router

router = APIRouter()

router.include_router(storage_router)
router.include_router(auth_router)
