from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import UserResponse, UserListResponse
from bson import ObjectId

class StudentRepository():
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["User"]

    async def get_students(self) -> UserListResponse | None:
        students = await self.collection.find().to_list(length=None)
        user_list = [
            UserResponse(**{**user, "_id": str(user["_id"])})
            for user in students
        ]
        return UserListResponse(users=user_list)
        
    async def get_student_by_id(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return UserResponse(**{**user, "_id": str(user["_id"])})
        return None