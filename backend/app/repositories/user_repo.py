from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import User
from bson import ObjectId

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def get_by_id(self, user_id: str) -> User | None:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return User(**user) if user else None

    async def create(self, user: User) -> str:
        result = await self.collection.insert_one(user.dict(by_alias=True))
        return str(result.inserted_id)
