from fastapi import APIRouter

"""
    1. Search Assignment
        GET assignment by Subject_ID (Show All Assignments for a user)
        GET assignment by assignment_id (Show Assignment Details)
    2. Send Document
        POST document to assignment
            response verify document
        submit document
"""

router = APIRouter(prefix="/documents", tags=["Documents"])

# Get All Assignments For a User
@router.get("/get-all/{subject_id}")
async def get_all_assignments(subject_id: str):
    pass

# Get Assignment Details
@router.get("/get/{assignment_id}")
async def get_assignment(assignment_id: str):
    pass

# Send Assignment Document
@router.post("/send-document/{assignment_id}")
async def send_document(assignment_id: str):
    pass

# Verify Assignment Document
@router.post("/verify-document/{assignment_id}")
async def verify_document(assignment_id: str):
    pass

# Submit Assignment Document
@router.post("/submit-document/{assignment_id}")
async def submit_document(assignment_id: str):
    pass

# Unsubmit Assignment Document
@router.delete("/unsubmit-document/{assignment_id}")
async def unsubmit_document(assignment_id: str):
    pass