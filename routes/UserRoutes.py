from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from schema.UserClient import *
from utils.utility import UserUtility

user_router = APIRouter(
    prefix='/user',
    tags=['user']
)

user_util = UserUtility()


@user_router.post('/signup', response_class=JSONResponse)
async def signup(user: Register):
    try:
        # Check if user already exists
        user_data = user_util.get_user(user.username)
        if user_data:
            error_response = ErrorResponse(
                status=False,
                error="User already exists",
                detail=f"User {user.username} already exists"
            )
            return JSONResponse(
                status_code=409,
                content=error_response.model_dump()
            )

        # Save student details
        saved_id = user_util.save_user(user)
        if not saved_id:
            error_response = ErrorResponse(
                status=False,
                error="Failed to save student details",
                detail=f"Failed to save student details"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        
        return JSONResponse(
            status_code=200,
            content={"message": "User registered successfully"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post('/login', response_class=JSONResponse)
async def login(user: Login):
    try:
        # Check if user exists
        user_data = user_util.get_user(user.username)
        if not user_data:
            error_response = ErrorResponse(
                status=False,
                error="User not found",
                detail=f"User {user.username} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )

        # Check if password is correct
        if not user_util.validate_password(user.password, user_data['password']):
            error_response = ErrorResponse(
                status=False,
                error="Invalid password",
                detail=f"Invalid password for user {user.username}"
            )
            return JSONResponse(
                status_code=401,
                content=error_response.model_dump()
            )

        return JSONResponse(
            status_code=200,
            content={"message": "User logged in successfully"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_router.get('/{username}', response_class=JSONResponse)
async def get_user(username: str):
    try:
        user_data = user_util.get_user(username)
        if not user_data:
            error_response = ErrorResponse(
                status=False,
                error="User not found",
                detail=f"User {username} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        
        user_data: Register = user_util.filter_user_data(user_data)
        return JSONResponse(
            status_code=200,
            content=user_data.model_dump()
        )
        
    except Exception as e:
        print("Exception while getting data from MongoDB\nError Message from routes/UserRoutes.py get_user function")
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get('/profile/{username}', response_class=JSONResponse)
async def get_profile(username: str):
    try:
        user_data = user_util.get_user(username)
        if not user_data:
            error_response = ErrorResponse(
                status=False,
                error="User not found",
                detail=f"User {username} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        
        user_profile = user_util.get_profile(user_data['_id'])
        if not user_profile:
            error_response = ErrorResponse(
                status=False,
                error="Profile not found",
                detail=f"Profile for user {username} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        
        user_skills = user_util.get_skills(user_data["_id"])
        user_projects = user_util.get_projects(user_data["_id"])

        user_profile["skills"] = user_skills
        user_profile["projects"] = user_projects

        user_profile = UserProfile(**user_profile)        
        return JSONResponse(
            status_code=200,
            content=user_profile.model_dump()
        )
        
    except Exception as e:
        print("Exception while getting data from MongoDB\nError Message from routes/UserRoutes.py get_profile function")
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post('/save/profile/{username}', response_class=JSONResponse)
async def save_profile(username: str, profile_data: UserProfile):
    try:
        # Check if username exists in the database
        user_data = user_util.get_user(username)
        if not user_data:
            error_response = ErrorResponse(
                status=False,
                error="User not found",
                detail=f"User {username} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        
        result: bool = user_util.save_profile(user_data['_id'], profile_data)
        if not result:
            error_response = ErrorResponse(
                status=False,
                error="Failed to save profile",
                detail=f"Failed to save profile"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )


        return JSONResponse(
            status_code=200,
            content={"message": "Profile saved successfully"}
        )
        
    except Exception as e:
        print("Exception while saving data in MongoDB\nError Message from routes/UserRoutes.py save_profile function")
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    

@user_router.post('/update/profile/{username}', response_class=JSONResponse)
async def update_profile(username: str, profile_data: UserProfile):
    try:
        # Check if username exists in the database
        user_data = user_util.get_user(username)
        if not user_data:
            error_response = ErrorResponse(
                status=False,
                error="User not found",
                detail=f"User {username} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        
        result: bool = user_util.update_profile(user_data['_id'], profile_data)
        if not result:
            error_response = ErrorResponse(
                status=False,
                error="Failed to update profile",
                detail=f"Failed to update profile"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )


        return JSONResponse(
            status_code=200,
            content={"message": "Profile updated successfully"}
        )
        
    except Exception as e:        
        print("Exception while updating data in MongoDB\nError Message from routes/UserRoutes.py update_profile function")
        print(e)
        raise HTTPException(status_code=400, detail=str(e))