from fastapi import APIRouter

"""
    1. Search Assignment
        GET assignment by user_id (Show All Assignments for a user)
        GET assignment by assignment_id (Show Assignment Details)
        GET user by assignment_id (Show All User in an Assignment)
"""

router = APIRouter(prefix="/assignments", tags=["Assignments"])

# Get All Assignments For a User by Subject ID
@router.get("/get-all/{subject_id}")
async def get_all_assignments(subject_id: str):
    pass

# Get Assignment Details
@router.get("/get/{assignment_id}")
async def get_assignment(assignment_id: str):
    pass
