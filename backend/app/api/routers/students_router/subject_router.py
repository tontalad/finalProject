from fastapi import APIRouter

router = APIRouter(prefix="/subjects", tags=["Subjects"])

"""
    1. Search Subject
        GET subject by user_id (Show Subject Details)
"""

# Get All Subject for a User by User ID
@router.get("/get-all/{user_id}")
async def get_all_subjects(user_id: str):
    pass

# Get Subject Details
@router.get("/get/{subject_id}")
async def get_subject(subject_id: str):
    pass

