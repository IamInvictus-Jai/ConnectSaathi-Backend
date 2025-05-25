from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Optional, List
from enum import Enum
from schema.UserDb import SkillLevel
# from bson import ObjectId

# Schema for User Login
class Login(BaseModel):
    username: str
    password: str

# Schema for User Signup
class Register(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str

# class SkillLevel(Enum):
#     BEGINNER = "beginner"
#     INTERMEDIATE = "intermediate"
#     ADVANCED = "advanced"

class Skill(BaseModel):
    skill: str
    level: SkillLevel

class Project(BaseModel):
    title: str
    # description: str
    link: str

class UserProfile(BaseModel):
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    years_exp: int
    skills: Optional[List[str]] = None
    projects: Optional[List[Project]] = None

    class Config:
        use_enum_values = True


class ErrorResponse(BaseModel):
    status: bool = False
    error: str
    detail: Optional[str] = None