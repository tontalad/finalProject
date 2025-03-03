from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User, UserResponse, UserListResponse, UserListResponseFromSubject
from bson import ObjectId

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]
        self.subject = db["SubjectAvaliable"]

    async def get_users_by_subject_id(self, subject_id: str) -> UserListResponse:
        # ดึงข้อมูล Subject จาก MongoDB
        subject = await self.subject.find_one({"_id": ObjectId(subject_id)})
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )

        teacher_ids = subject["Teachers"]
        student_ids = subject["Students"]
  
        # ดึงข้อมูล Teacher และ Students จาก MongoDB
        teacher_data = await self.collection.find({"_id": {"$in": teacher_ids}}).to_list(None)
        students_data = await self.collection.find({"_id": {"$in": student_ids}}).to_list(None)

        teacher_list = [
            UserResponse(**{**teacher, "_id": str(teacher["_id"])})
            for teacher in teacher_data
        ]
        student_list = [
            UserResponse(**{**student, "_id": str(student["_id"])})
            for student in students_data
        ]

        return UserListResponseFromSubject(teacher=teacher_list, student=student_list)

    async def get_by_id(self, user_id: str) -> UserResponse | None:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return UserResponse(**{**user, "_id": str(user["_id"])}) if user else None

    async def create(self, user: User) -> UserResponse | None:
        result = await self.collection.insert_one(user.model_dump())
        return UserResponse(**{**user.model_dump(), "_id": str(result.inserted_id)}) if user else None
    
    async def get_by_email(self, email: str) -> UserResponse | None:
        user = await self.collection.find_one({"email": email})
        return UserResponse(**{**user, "_id": str(user["_id"])}) if user else None
    
