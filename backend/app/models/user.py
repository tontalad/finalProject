from pydantic import BaseModel, Field, GetJsonSchemaHandler
from typing import Optional, List, Any, Annotated
from bson import ObjectId

    

class User(BaseModel):
    id: Annotated[str, Field(alias="_id")]
    UserName: str
    UserLastName: str
    Email: str

    class Config:
        from_attriubte = True
        populate_by_name = True
        json_encoders = {ObjectId: str}

class UserResponse(BaseModel):
    id: Annotated[str, Field(alias="_id")]
    user_name: str = Field(None, alias="UserName")
    user_last_name: str = Field(None, alias="UserLastName")
    email: str = Field(None, alias="Email")
    type: List[str] = Field(default_factory=list, alias="Type")
    track: str = Field(None, alias="Track")
    year: str = Field(None, alias="Year")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class UserListResponse(BaseModel):
    users: list[UserResponse]
