from fastapi import APIRouter
from .assignment_router import router as assignment_router
from .group_router import router as group_router
from .subject_router import router as subject_router
from .user_router import router as user_router

router = APIRouter(prefix="/admin", tags=["Admin"])

router.include_router(assignment_router)
router.include_router(group_router)
router.include_router(subject_router)
router.include_router(user_router)