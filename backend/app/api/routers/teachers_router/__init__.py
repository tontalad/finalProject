from fastapi import APIRouter
from .assignment_router import router as assignment_router
from .report_router import router as report_router

router = APIRouter(prefix="/teacher", tags=["Teachers"])

router.include_router(assignment_router)
router.include_router(report_router)