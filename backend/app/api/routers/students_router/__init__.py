from fastapi import APIRouter
from .document_router import router as document_router
from .group_router import router as group_router

router = APIRouter(prefix="/student", tags=["Students"])

router.include_router(document_router)
router.include_router(group_router)