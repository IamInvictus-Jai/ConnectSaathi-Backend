from typing import Optional, Union, Dict
import pytz
from datetime import datetime
from bson import ObjectId

from utils.dbHandler import MongoDB
from schema.UserClient import *
from schema.UserDb import *
from schema.CommunityClient import *
from schema.CommunityDb import *

mongoDBHandler = MongoDB()


try:
    if not mongoDBHandler.connect():
        raise Exception("MongoDB connection failed")
except Exception as e:
    print(e)

# Create Indexes on MongoDB fields for faster lookups
mongoDBHandler.create_index("community_skills", "skill")
mongoDBHandler.create_index("community", "registeration_date_time")

class Utilities:
    def __init__(self):
        self.tz = pytz.timezone('Asia/Kolkata')

    def get_date_time(self):
        # Get the current time in IST
        ist_timezone = pytz.timezone("Asia/Kolkata")
        now = datetime.now(ist_timezone)

        # Format the date and time
        formatted_date = now.strftime("%d %B %Y")  # Example: "4 April 2025"
        formatted_time = now.strftime("%I:%M %p") + " IST"  # Example: "12:03 AM IST"

        return formatted_date, formatted_time
    
    def format_datetime(self, dt: datetime) -> str:
        ist = dt.astimezone(pytz.timezone('Asia/Kolkata'))
        return ist.strftime("%d %B %Y %I:%M %p IST")


class UserUtility:
    def __init__(self):
        self.utility = Utilities()

    def save_user(self, user: Register) -> Optional[ObjectId]|None:
        """
        Save user details to MongoDB

        Args:
            user (Register): user details

        Returns:
            Optional[ObjectId]|None: user id
        """
        try:
            formatted_date, formatted_time = self.utility.get_date_time()
            user_data = user.model_dump()
            user_data["role"] = "user"
            user_data["registeration_date_time"] = f"{formatted_date} {formatted_time}"
            user_data = UserData(**user_data)

            # Save data to MongoDB
            student_inquiry_id:ObjectId = mongoDBHandler.insert("user", user_data)
            return student_inquiry_id
        
        except Exception as e:
            print("Exception while saving data in MongoDB\nError Message from utils/utility.py save_user function")
            print(e)
            return None
    
    def get_user(self, username: str) -> Union[Dict, None]:
        """
        Get user details from MongoDB

        Args:
            username (str): username of the user

        Returns:
            Union[Dict, None]: user details
        """
        try:
            return mongoDBHandler.find_one("user", {"username": username})
        except Exception as e:
            print("Exception while getting data from MongoDB\nError Message from utils/utility.py get_user function")
            print(e)
            return None
    
    def validate_password(self, given_password, original_password):
        return given_password == original_password
    
    def filter_user_data(self, user) -> Register:
        filtered_user = {
            "username": user["username"],
            "name": user["name"],
            "email": user["email"],
            "password": user["password"]
        }
        
        return Register(**filtered_user)
    
    def filter_user_profile_data(self, user) -> UserProfile:
        filtered_user = {
            "name": user["name"],
            "email": user["email"],
            "skills": user["skills"],
            "projects": user["projects"]
        }
        
        return UserProfile(**filtered_user)

    def save_profile(self, user_id: ObjectId, profile_data: UserProfile) -> bool:
        try:
            # Save User Casual Data
            profile_dict = profile_data.model_dump(exclude={'skills', 'projects'})
            profile_dict['user_id'] = user_id            
            profile = UserProfileData(**profile_dict)
            
            # Save to MongoDB
            mongoDBHandler.insert("user_profiles", profile)

            # Save Skills
            if profile_data.skills:
                for skill in profile_data.skills:
                    skill_doc = UserSkills(
                        user_id=user_id,
                        skill=skill,
                        # level=skill.level
                    )
                    mongoDBHandler.insert("user_skills", skill_doc)

            # Save Projects
            if profile_data.projects:
                for project in profile_data.projects:
                    project_doc = UserProjects(
                        user_id=user_id,
                        title=project.title,
                        # description=project.description,
                        link=project.link
                    )
                    mongoDBHandler.insert("user_projects", project_doc)
            
            return True
        
        except Exception as e:
            print("Exception while saving data in MongoDB\nError Message from utils/utility.py save_profile function")
            print(e)
            return 
    
    def get_profile(self, user_id: ObjectId) -> Union[Dict, None]:
        try:
            return mongoDBHandler.find_one("user_profiles", {"user_id": user_id})
        except Exception as e:
            print("Exception while getting data from MongoDB\nError Message from utils/utility.py get_profile function")
            print(e)
            return None

    def get_skills(self, user_id: ObjectId) -> Dict[str, str] | None:
        try:
            skills = mongoDBHandler.find("user_skills", {"user_id": user_id})
            skills = [
                skill["skill"]
                for skill in skills
            ]
            return skills
        
        except Exception as e:
            print("Exception while getting data from MongoDB\nError Message from utils/utility.py get_skills function")
            print(e)
            return None
    
    def get_projects(self, user_id: ObjectId) -> Union[List[Dict], None]:
        try:
            projects = mongoDBHandler.find("user_projects", {"user_id": user_id})
            projects = [
                {
                    "title": project["title"],
                    # "description": project["description"],
                    "link": project["link"]
                }
                for project in projects
            ]
            return projects
        except Exception as e:
            print("Exception while getting data from MongoDB\nError Message from utils/utility.py get_projects function")
            print(e)
            return None

    def update_profile(self, user_id: ObjectId, profile_data: UserProfile) -> bool:
        try:
            # Save User Casual Data
            profile_dict = profile_data.model_dump(exclude={'skills', 'projects'})
            profile_dict['user_id'] = user_id            
            profile = UserProfileData(**profile_dict)
            
            # Save to MongoDB
            mongoDBHandler.update("user_profiles", {"user_id": user_id}, profile)

            # Save Skills
            if profile_data.skills:
                mongoDBHandler.delete_many("user_skills", {"user_id": user_id})
                for skill in profile_data.skills:
                    skill_doc = UserSkills(
                        user_id=user_id,
                        skill=skill.skill,
                        # level=skill.level
                    )
                    mongoDBHandler.insert("user_skills", skill_doc)

            # Save Projects
            if profile_data.projects:
                mongoDBHandler.delete_many("user_projects", {"user_id": user_id})
                for project in profile_data.projects:
                    project_doc = UserProjects(
                        user_id=user_id,
                        title=project.title,
                        # description=project.description,
                        link=project.link
                    )
                    mongoDBHandler.insert("user_projects", project_doc)
            
            return True
        
        except Exception as e:
            print("Exception while saving data in MongoDB\nError Message from utils/utility.py update_profile function")
            print(e)
            return
        
class CommunityUtility:
    def __init__(self):
        self.utility = Utilities()

    def save_community(self, community: Community) -> Optional[ObjectId]|None:
        """
        Save community details to MongoDB

        Args:
            community (Community): community details

        Returns:
            Optional[ObjectId]|None: community id
        """
        try:
            now = datetime.now(pytz.UTC)
            community_data = community.model_dump()
            community_data["registeration_date_time"] = now
            community_data = CommunityData(**community_data)

            # Save data to MongoDB
            community_id:ObjectId = mongoDBHandler.insert("community", community_data)

            # Save Tech Stack
            for tech_stack in community.tech_stack:
                tech_stack_doc = CommunitySkill(
                    community_id=community_id,
                    skill=tech_stack
                )
                mongoDBHandler.insert("community_skills", tech_stack_doc)

            return community_id
        
        except Exception as e:
            print("Exception while saving data in MongoDB\nError Message from utils/utility.py save_community function")
            print(e)
            return None
        
    def get_community(self, community_id: str) -> Community|None:
        try:
            community_data = mongoDBHandler.find_one("community", {"_id": ObjectId(community_id)})
            required_tech_stacks = mongoDBHandler.find("community_skills", {"community_id": ObjectId(community_id)})

            if not community_data:
                return None
            
            community_data["tech_stack"] = [tech_stack["skill"] for tech_stack in required_tech_stacks]
            community_data = Community(**community_data)  
            return community_data
        
        except Exception as e:
            print("Exception while getting data from MongoDB\nError Message from utils/utility.py get_community function")
            print(e)
            return None
        
    def get_latest_communities(self, limit: int = 10, page:int = 1) -> List[Community]:
        try:
            skip = (page - 1) * limit
            communities = mongoDBHandler.find_with_sort(
                collection_name="community",
                sort_field="registeration_date_time",
                skip=skip,
                limit=limit
            )
            if not communities:
                return []
            
            community_ids = [comm["_id"] for comm in communities]

            required_tech_stacks = mongoDBHandler.find("community_skills", {"community_id": {"$in": community_ids}})
            for comm in communities:
                comm["tech_stack"] = [tech_stack["skill"] for tech_stack in required_tech_stacks if tech_stack["community_id"] == comm["_id"]]
            
            return [Community(**comm) for comm in communities]
        except Exception as e:
            print("Error fetching latest communities:", e)
            return []

    def search_community_by_skills(self, skills: List[str], limit: int = 10) -> List[Community] | None:
        try:
            pipeline = [
                {
                    "$match": {
                        "skill": {"$in": skills}
                    }
                },
                {
                    "$group": {
                        "_id": "$community_id",
                        "tech_stack": {"$addToSet": "$skill"}
                    }
                },
                {
                    "$lookup": {
                        "from": "community",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "community_details"
                    }
                },
                {
                    "$unwind": "$community_details"
                },
                {
                    "$limit": limit
                },
                {
                    "$sort": {
                        "community_details.registeration_date_time": -1
                    }
                },
                {
                    "$project": {
                        "name": "$community_details.name",
                        "creator_username": "$community_details.creator_username",
                        "exp_level": "$community_details.exp_level",
                        "registeration_date_time": "$community_details.registeration_date_time",
                        "tech_stack": 1,
                        "_id": 0
                    }
                }
            ]
            results = mongoDBHandler.aggregate("community_skills", pipeline)
            if not results:
                return None
            return [Community(**comm) for comm in results]
            
        except Exception as e:
            print("Error message from utils/utility.py search_community_by_skills function")
            print("Error searching communities by tech stack:", e)
            return None
        
    def get_user_communities(self, username: str) -> List[Community] | None:
        try:
            communities = mongoDBHandler.find("community", {"creator_username": username})
            communities = [CommunityResponse(**comm) for comm in communities]
            return communities
        except Exception as e:
            print("Error message from utils/utility.py get_user_communities function")
            print("Error getting user communities:", e)
            return None

        
