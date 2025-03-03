from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from models.query_params import QueryParams
from models.subject import SubjectCreate, SubjectListResponse, SubjectResponse, SubjectUpdate
from models.user import User
from db.db import database
from repositories.subject_repo import SubjectRepository
from services.subject_service import SubjectService
from infrastructure.auth import get_subject_permission

"""
    1. Search Subject
        GET subject (Show All Subjects)
        GET subject by year (Show All Subjects in a Year)
        GET subject by subject_id (Show Subject Details)
    2. Create Subject
        POST subject
    3. Update Subject
        EDIT subject
    4. Delete Subject
        DELETE subject
    5. Add User to Subject
        POST user_id to subject_id
        POST list(user_id) to subject_id (Add multiple users to a subject)
    6. Remove User from Subject
        DELETE user_id from subject_id
"""

router = APIRouter(prefix="/subjects", tags=["Subjects"])

def get_subject_service():
    repo = SubjectRepository(database)
    return SubjectService(repo)

@router.get("/get-group")
async def get_group():
    pass

# Insert User to Subject by Subject ID, Type = Student, Teacher
@router.post("/insert-user/{subject_id}")
async def insert_user(subject_id: str, user_data: User, service: SubjectService = Depends(get_subject_service)):
    try:
        result = await service.insert_user(subject_id, user_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
# Insert Multiple Users From CSV to Subject by Subject ID, Type = Student
@router.post("/insert-multiple-users/{subject_id}")
async def upload_users(subject_id: str, file: UploadFile = File(...),
                       service: SubjectService = Depends(get_subject_service)):
    try:
        result = await service.insert_multiple_user(subject_id, file)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get Subject Details By Subject ID
@router.get("/get/{subject_id}", response_model = SubjectResponse, dependencies = [Depends(get_subject_permission())])
async def get_subject(subject_id: str, 
                      service: SubjectService = Depends(get_subject_service)
                    ):
    try:
        subject = await service.get_by_id(subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found"
            )
        return subject
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

# Get All Subjects
@router.post("/get-all", response_model = SubjectListResponse)
async def get_all_subjects(service: SubjectService = Depends(get_subject_service), query_params: QueryParams = Depends()):
    try:
        subjects = await service.get_all(query_params)
        if not subjects:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subjects not found"
            )
        return subjects
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

# Create Subject
@router.post("/create", response_model=SubjectResponse)
async def create_subject(item: SubjectCreate, service: SubjectService = Depends(get_subject_service)):
    try:
        subject = await service.create(item)
        if not subject:
            raise HTTPException(  
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject not created"
            )
        return subject
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

# Update Subject
@router.put("/update/{subject_id}")
async def update_subject(subject_id: str, item: SubjectUpdate, service: SubjectService = Depends(get_subject_service)):
    try:
        subject = await service.update(subject_id, item)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject not updated"
            )
        return subject
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))

# Delete Subject
@router.delete("/delete/{subject_id}")
async def delete_subject(subject_id: str, service: SubjectService = Depends(get_subject_service)):
    try:
        subject = await service.delete(subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject not deleted"
            )
        return subject
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
