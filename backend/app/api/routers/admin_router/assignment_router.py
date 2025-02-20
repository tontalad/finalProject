from fastapi import APIRouter

"""
    1. Search Assignment
        GET assignment by subject_id (Show All Assignments In a Subject)
            filter by sent, verified, submitted
        GET assignment by assignment_id (Show Assignment Details)
        GET assignment by group_id (Show Assignments for a group)
    2. Create Assignment   
        POST assignment (subject_id, due_date, assignment_name, description, document)
    3. Update Assignment
        EDIT assignment (assignment_neme, due_date, description, document)
    4. Delete Assignment
        DELETE assignment
    5. Verify Assignment
        POST assignment_id to user_id
"""

router = APIRouter(prefix="/assignments", tags=["Assignments"])


# Get All Assignments In a Subject
@router.get("/get-all/{subject_id}")
async def get_all_assignments(subject_id: str):
    pass


# Get Assignment Details
@router.get("/get-assignment/{assignment_id}")
async def get_assignment(assignment_id: str):
    pass


# Create Assignment by Subject_id
@router.post("/create-assignment/{subject_id}")
async def create_assignment(subject_id: str):
    pass

# Update Assignment
@router.put("/update-assignment/{assignment_id}")
async def update_assignment(assignment_id: str):
    pass

# Verify Assignment Document
@router.post("/verify-assignment/{assignment_id}")
async def verify_assignment(assignment_sent_id: str):
    pass

# Delete Assignment
@router.delete("/delete-assignment/{assignment_id}")
async def delete_assignment(assignment_id: str):
    pass