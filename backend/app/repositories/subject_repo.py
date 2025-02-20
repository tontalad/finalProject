from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.subject import SubjectResponse, SubjectListResponse, SubjectUpdate
from bson import ObjectId

class SubjectRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["SubjectAvaliable"]

    async def get_by_id(self, subject_id: str) -> SubjectResponse | None:
        subject = await self.collection.find_one({"_id": ObjectId(subject_id)})
        return SubjectResponse(**{**subject, "_id": str(subject["_id"])}) if subject else None

    async def get_all(self) -> SubjectListResponse:
        subjects = await self.collection.find().to_list(None)
        subject_list = [
            SubjectResponse(**{**subject, "_id": str(subject["_id"])})
            for subject in subjects
        ]
        return SubjectListResponse(subjects=subject_list)

    async def create(self, subject: SubjectResponse) -> str:
        result = await self.collection.insert_one(subject.dict(by_alias=True))
        subject = await self.collection.find_one({"_id": ObjectId(result.inserted_id)})
        return SubjectResponse(**{**subject, "_id": str(subject["_id"])})

    async def update(self, subject_id: str, subject: SubjectUpdate) -> bool:
        if not ObjectId.is_valid(subject_id):
            raise HTTPException(status_code=400, detail="Invalid subject ID")
        update_data = subject.model_dump(by_alias=True, exclude_unset=True)
        result = await self.collection.update_one(
            {"_id": ObjectId(subject_id)}, {"$set": update_data}
        )
        return result.modified_count == 1

    async def delete(self, subject_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(subject_id)})
        return result.deleted_count == 1