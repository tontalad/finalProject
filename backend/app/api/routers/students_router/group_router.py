from fastapi import APIRouter, Request, HTTPException, status, Depends
from db.db import get_collection, database
from models.user import UserListResponse, UserResponse
from repositories.student_repo import StudentRepository
from services.student_service import StudentService
from bson import ObjectId

"""
    1. Search Group
        GET group by subject_id (Show All Groups for a subject)
            filter by track_name
    2. Join Group
        POST user_id to group
    3. Leave Group
        POST user_id to group
"""

router = APIRouter(prefix="/groups", tags=["Groups"])

def get_student_service():
    repo = StudentRepository(database)
    return StudentService(repo)

@router.get("/get-students", response_model=UserListResponse)
async def get_students(service: StudentService = Depends(get_student_service)):
    return await service.get_students()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, service: StudentService = Depends(get_student_service)):
    user = await service.get_student_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

 