from pydantic import BaseModel, Field, BeforeValidator, model_validator
from typing import List, Dict, Optional, Annotated
from datetime import datetime
from bson import ObjectId, Timestamp
from . import convert_timestamp

PyObjectId = Annotated[str, BeforeValidator(str)]

def to_objectid(value):
    if isinstance(value, str) and ObjectId.is_valid(value):
        return ObjectId(value)
    return value

class SubjectGroup(BaseModel):
    BIT: Optional[str] = None
    WEB: Optional[str] = None
    Network: Optional[str] = None

class Subject(BaseModel):
    name: str = Field(alias="SubjectName")
    description: str = Field(None, alias="Description")
    teacher: List[str] = Field(default_factory=list, alias="Teachers")
    number_of_students: int = Field(alias="NumberOfStudent")
    section: str = Field(alias="Section")
    subject_semester: str = Field(alias="SubjectSemester")
    subject_year: str = Field(alias="SubjectYear")
    group: Optional[SubjectGroup] = Field(None, alias="Group")
    created_at: Optional[str] = Field(default_factory=datetime.now, alias="CreatedAt")
    updated_at: Optional[str] = Field(None, alias="UpdatedAt")
    deleted_at: Optional[str] = Field(None, alias="DeletedAt")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class SubjectUpdate(BaseModel):
    name: str = Field(None, alias="SubjectName")
    description: str = Field(None, alias="Description")
    teacher: Optional[List[PyObjectId]] = Field(default_factory=list, alias="Teachers")
    number_of_students: int = Field(None, alias="NumberOfStudent")
    section: str = Field(None, alias="Section")
    subject_semester: str = Field(None, alias="SubjectSemester")
    subject_year: str = Field(None, alias="SubjectYear")
    group: Optional[SubjectGroup] = Field(None, alias="Group")
    created_at: Optional[str] = Field(None, alias="CreatedAt")
    updated_at: Optional[str] = Field(default_factory=datetime.now, alias="CreatedAt")
    deleted_at: Optional[str] = Field(None, alias="DeletedAt")

    @model_validator(mode="before")
    def convert_teachers_to_objectid(cls, values):
        if "Teachers" in values:
            values["Teachers"] = [to_objectid(t) for t in values["Teachers"]]
        return values
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class SubjectResponse(BaseModel):
    id: Annotated[str, Field(None, alias="_id")]
    name: str = Field(alias="SubjectName")
    description: str | None = Field(None, alias="Description")
    teacher: Optional[List[str]] = Field(None, alias="Teachers")
    number_of_students: int = Field(alias="NumberOfStudent")
    section: str = Field(alias="Section")
    subject_semester: str = Field(alias="SubjectSemester")
    subject_year: str = Field(alias="SubjectYear")
    group: Optional[SubjectGroup] = Field(None, alias="Group")
    created_at: Annotated[Optional[datetime], BeforeValidator(convert_timestamp)] = Field(None, alias="CreatedAt")
    updated_at: Annotated[Optional[datetime], BeforeValidator(convert_timestamp)] = Field(None, alias="UpdatedAt")
    deleted_at: Annotated[Optional[datetime], BeforeValidator(convert_timestamp)] = Field(None, alias="DeletedAt")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

class SubjectListResponse(BaseModel):
    subjects: List[SubjectResponse]