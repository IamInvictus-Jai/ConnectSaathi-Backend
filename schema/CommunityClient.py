from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class Community(BaseModel):
    creator_username:str
    name:str
    tech_stack:List[str]
    experience: Optional[str] = None

class SearchCommunityBySkills(BaseModel):
    limit:int
    skills:List[str]

# Search Community By Skills Response Model
class CommunityBySkillsResponse(BaseModel):
    tech_stack:List[str]
    name:str
    creator_username:str
    experience:Optional[str] = None
    registeration_date_time: datetime

class ErrorResponse(BaseModel):
    status: bool = False
    error: str
    detail: Optional[str] = None

class CommunityResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name:str
    experience:Optional[str] = None

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,  # Optional: lets you use "id" instead of "_id"
    }