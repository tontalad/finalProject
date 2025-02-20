from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["Reports"])

"""
        1. view Report
            GET report by assignment_id
            GET report by group_id
"""

# Get Report by Assignment ID
@router.get("/get-by-assignment/{assignment_id}")
async def get_report_by_assignment(assignment_id: str):
    pass

# Get Report by Group ID
@router.get("/get-by-group/{group_id}")
async def get_report_by_group(group_id: str):
    pass