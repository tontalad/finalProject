from pydantic import BaseModel, Field, GetJsonSchemaHandler
from typing import Optional, List, Any, Annotated
from bson import ObjectId
from datetime import datetime

    

class User(BaseModel):
    name: str = Field(None, alias="UserName")
    last_name: str = Field(None, alias="UserLastName")
    email: str = Field(None, alias="Email")
    type: str = Field(None, alias="Type")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    updated_at: Optional[datetime] = Field(None, alias="UpdatedAt")
    deleted_at: Optional[datetime] = Field(None, alias="DeletedAt")

    class Config:
        from_attriubte = True
        populate_by_name = True
        json_encoders = {ObjectId: str}

    def set_created_at(self):
        self.created_at = datetime.now().isoformat()

    def set_updated_at(self):
        self.updated_at = datetime.now().isoformat()

class UserResponse(BaseModel):
    id: Annotated[str, Field(None, alias="_id")]
    name: str = Field(None, alias="UserName")
    last_name: str = Field(None, alias="UserLastName")
    email: str = Field(None, alias="Email")
    type: str = Field(default_factory=str, alias="Type")
    track: str = Field(None, alias="Track")
    year: str = Field(None, alias="Year")
    created_at: Optional[datetime] = Field(None, alias="CreatedAt")
    updated_at: Optional[datetime] = Field(None, alias="UpdatedAt")
    deleted_at: Optional[datetime] = Field(None, alias="DeletedAt")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class UserListResponse(BaseModel):
    users: list[UserResponse]

class UserListResponseFromSubject(BaseModel):
    teacher: list[UserResponse]
    student: list[UserResponse]