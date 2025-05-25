from pydantic import BaseModel, Field
from typing import Dict, Optional
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class CommunityData(BaseModel):
    creator_username:str
    name: str
    experience:Optional[str] = None
    registeration_date_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class CommunitySkill(BaseModel):
    community_id: PyObjectId = Field(default_factory=PyObjectId)
    skill: str

    model_config = {
        "json_encoders": {ObjectId: str}
    }