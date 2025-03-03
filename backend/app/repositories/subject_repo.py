from fastapi import HTTPException, status, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.subject import SubjectResponse, SubjectListResponse, SubjectUpdate
from models.user import User, UserListResponse
from bson import ObjectId
from services.query_params import QueryParamsService
from models.query_params import QueryParams
import pandas as pd
import numpy as np

class SubjectRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["SubjectAvaliable"]
        self.user_collection = db["users"]
        self.query_params = QueryParamsService(self.collection)

    async def insert_user_to_subject(self, subject_id: str, user_data: User):
        # ตรวจสอบว่า Subject มีอยู่หรือไม่
        subject = await self.collection.find_one({"_id": ObjectId(subject_id)})
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )

        user = await self.user_collection.find_one({"email": user_data.Email})

        if not user:
            user_data.set_created_at()
            user_dict = user_data.model_dump()
            user_dict["_id"] = ObjectId()  # สร้าง ObjectId ใหม่
            await self.user_collection.insert_one(user_dict)
            user = user_dict  # ใช้ user_dict ต่อไป

        if user["Type"] == "Teacher":
            await self.collection.update_one(
                {"_id": ObjectId(subject_id)},
                {"$addToSet": {"Teachers": user["_id"]}}
            )
        elif user["Type"] == "Student":
            await self.collection.update_one(
                {"_id": ObjectId(subject_id)},
                {"$addToSet": {"Students": user["_id"]}}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user role",
            )

        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="User added to subject successfully",
        )
    
    async def insert_multiple_user_to_subject(self, subject_id: str, file: UploadFile = File(...)):
        subject = await self.collection.find_one({"_id": ObjectId(subject_id)})
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        
        df = pd.read_excel(file.file, skiprows=5)
        df = df.applymap(lambda x: np.nan if str(x).strip() == "" else x)
        df.dropna(axis=1, how='all', inplace=True)  
        print(df.columns[df.isna().all()].tolist())
        
        required_columns = {"ชื่อ", "kkumail"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {required_columns - set(df.columns)}",
            )
        
        

        inserted_users = []
        for _, row in df.iterrows():
            full_name = str(row.get("ชื่อ", "")).strip() 
            name, last_name = (full_name.split(" ", 1) + [""])[:2]  
            user_data = User(
                UserName=name,
                UserLastName=last_name,
                Email=row["kkumail"],
                Type="Student"
            )

            user = await self.user_collection.find_one({"email": user_data.email})
            if not user:
                user_data.set_created_at()
                user_dict = user_data.model_dump()
                user_dict["_id"] = ObjectId()
                await self.user_collection.insert_one(user_dict)
                user = user_dict  # ใช้ user_dict ต่อไป

            await self.collection.update_one(
                {"_id": ObjectId(subject_id)},
                {"$addToSet": {"Students": user["_id"]}}
            )


            inserted_users.append(user_data.email)

        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Create multiple users to subject successfully",
        )

    async def get_by_id(self, subject_id: str) -> SubjectResponse | None:
        subject = await self.collection.find_one({"_id": ObjectId(subject_id)})
        return SubjectResponse(**{**subject, "_id": str(subject["_id"])}) if subject else None

    async def get_all(self, query_params: QueryParams) -> SubjectListResponse:
        subjects = await self.query_params.build_and_execute_query(query_params)
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