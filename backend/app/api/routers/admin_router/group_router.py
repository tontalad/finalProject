from fastapi import APIRouter

"""
    1. Search Group
        GET group by user_id (Show All Groups for a user)
        GET group by group_id (Show Group Details)
        GET group by subject_id (Show All Groups in a Subject)
    2. Create Group
        POST group (subject_id)
    3. Update Group (Edit User in Group)
        ADD user to group
        Delete user from group
    4. Delete Group
        DELETE group
    5. Submit Group
        POST group_id to user_id 
"""

router = APIRouter(prefix="/groups", tags=["Groups"])

# Get All Groups In a Subject
@router.get("/get-all/{subject_id}")
async def get_all_groups_in_subject(subject_id: str):
    pass

# Get Group Details
@router.get("/get-group/{group_id}")
async def get_group(group_id: str):
    pass

# Update Group
@router.put("/update-group/{group_id}") 
async def update_group(group_id: str):
    pass

# Submit Group
@router.post("/submit-group/{group_id}")
async def submit_group(group_id: str):
    pass