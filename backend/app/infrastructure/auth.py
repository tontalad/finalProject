from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models.user import UserResponse
from models.subject import SubjectResponse
from utils.jwt import decode_access_token
from services.subject_service import SubjectService
from repositories.subject_repo import SubjectRepository
from db.db import database
from settings import settings

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID  # From your Google Cloud Console
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET  # From your Google Cloud Console
REDIRECT_URI = settings.GOOGLE_REDIRECT_URI

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/google/callback")

def get_subject_service():
    repo = SubjectRepository(database)
    return SubjectService(repo)

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse(id=payload["sub"], email=payload["email"], type=payload["type"])


def get_permission(required_role: str):
    async def permission_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.type != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user
    return permission_checker

def get_subject_permission():
    async def permission_checker(
        subject_id: str,  # ดึง subject_id จาก request path
        service: SubjectService = Depends(get_subject_service),
        current_user: UserResponse = Depends(get_current_user)
    ):
        subject = await service.get_by_id(subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        if current_user.id not in subject.students:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user
    return permission_checker