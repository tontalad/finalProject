from fastapi import APIRouter, Request, HTTPException, status, Depends
from db.db import get_collection, database
from models.user import UserListResponse, UserResponse
from repositories.student_repo import StudentRepository
from services.student_service import StudentService

router = APIRouter()

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