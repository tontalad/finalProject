from fastapi import APIRouter

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
 
# Get All Users In a Subject
@router.get("/get-all/{subject_id}")
async def get_all_users_in_subject(subject_id: str):
    pass

# Get All Users In a Group
@router.get("/get-all-group/{group_id}")
async def get_all_users_in_group(group_id: str):
    pass

# Get User Details 
@router.get("/get-user/{user_id}")
async def get_user_details(user_id: str):
    pass

# Insert User to Subject by Subject ID
@router.post("/insert-user/{subject_id}")
async def insert_user():
    pass

# Insert Multiple Users From CSV to Subject by Subject ID
@router.post("/insert-users/{subject_id}")
async def insert_multiple_users():
    pass

# Update User
@router.put("/update-user/{user_id}")
async def update_user(user_id: str):
    pass

# Delete User
@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    pass