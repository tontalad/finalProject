from fastapi import APIRouter, Depends, HTTPException, status
from models.user import UserResponse, UserListResponseFromSubject
from infrastructure.auth import get_current_user, get_permission
from repositories.user_repo import UserRepository
from services.user_service import UserService
from db.db import database

"""
    1. Search User
        GET user by user_id (Show User Details)
        GET user by subject_id (Show All Users in a Subject)
    2. Create User
        POST user (Create a user)
        POST users (Create multiple users by uploading a csv file)
    3. Update User
        EDIT user (user_id, subject_id)
    4. Delete User
        DELETE user
"""

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service():
    repo = UserRepository(database)
    return UserService(repo)


@router.get("/me", dependencies= [Depends(get_permission("Student"))])
async def read_users_me(current_user: UserResponse = Depends(get_current_user),):
    return current_user
 
# Get All Users In a Subject
@router.get("/get-all-subject/{subject_id}", response_model=UserListResponseFromSubject)
async def get_all_users_in_subject(subject_id: str, service: UserService = Depends(get_user_service)):
    try:
        user = await service.get_user_by_subject(subject_id) 
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subjects not found"
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))


# Get All Users In a Group
@router.get("/get-all-group/{group_id}")
async def get_all_users_in_group(group_id: str):
    pass

# Get User Details 
@router.get("/get-user/{user_id}", response_model=UserResponse)
async def get_user_details(user_id: str, service: UserService = Depends(get_user_service)):
    try:
        user = await service.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subjects not found"
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))


# Update User
@router.put("/update-user/{user_id}")
async def update_user(user_id: str):
    pass

# Delete User
@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    pass