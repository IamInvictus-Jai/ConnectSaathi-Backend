from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Optional
from enum import Enum
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

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

    def __str__(self):
        return self.value

class UserData(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str
    role: UserRole
    registeration_date_time: str

    class Config:
        use_enum_values = True

class UserProfileData(BaseModel):
    user_id: PyObjectId = Field(default_factory=PyObjectId)
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    years_exp: int

    class Config:
        json_encoders = {ObjectId: str}

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

    def __str__(self):
        return self.value

class UserSkills(BaseModel):
    user_id: PyObjectId = Field(default_factory=PyObjectId)
    skill: str
    # level: SkillLevel

    class Config:
        use_enum_values = True
        json_encoders = {ObjectId: str}

class UserProjects(BaseModel):
    user_id: PyObjectId = Field(default_factory=PyObjectId)
    title: str
    # description: str
    link: str

    class Config:
        json_encoders = {ObjectId: str}