from fastapi import APIRouter, Depends
from models.subject import Subject, SubjectListResponse, SubjectResponse, SubjectUpdate
from db.db import database
from repositories.subject_repo import SubjectRepository
from services.subject_service import SubjectService

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

# Get Subject Details By Subject ID
@router.get("/get/{subject_id}", response_model=SubjectResponse)
async def get_subject(subject_id: str, service: SubjectService = Depends(get_subject_service)):
    return await service.get_by_id(subject_id)

# Get All Subjects
@router.get("/get-all", response_model=SubjectListResponse)
async def get_all_subjects(service: SubjectService = Depends(get_subject_service)):
    return await service.get_all()

# Create Subject
@router.post("/create", response_model=SubjectResponse)
async def create_subject(item: Subject, service: SubjectService = Depends(get_subject_service)):
    return await service.create(item)

# Update Subject
@router.put("/update/{subject_id}")
async def update_subject(subject_id: str, item: SubjectUpdate, service: SubjectService = Depends(get_subject_service)):
    return await service.update(subject_id, item)

# Delete Subject
@router.delete("/delete/{subject_id}")
async def delete_subject(subject_id: str, service: SubjectService = Depends(get_subject_service)):
    return await service.delete(subject_id)
