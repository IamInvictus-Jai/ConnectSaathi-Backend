from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from schema.CommunityClient import *
from utils.utility import CommunityUtility

community_router = APIRouter(
    prefix='/community',
    tags=['community']
)

community_util = CommunityUtility()


@community_router.post('/create', response_class=JSONResponse)
async def create_community(community: Community):

    try:
        community_id = community_util.save_community(community)
        if not community_id:
            error_response = ErrorResponse(
                status=False,
                error="Failed to save community details",
                detail=f"Failed to save community details"
            )
            return JSONResponse(
                status_code=409,
                content=error_response.model_dump()
            )
        return JSONResponse(content={"message": "Community created successfully", "community_id": str(community_id)})    
    except Exception as e:
        print("Exception while getting data from MongoDB\nError Message from routes/CommunityRoutes.py create_community function")
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@community_router.get('/id/{community_id}', response_class=JSONResponse)
async def get_community(community_id: str):
    try:
        community_data: Community = community_util.get_community(community_id)
        if not community_data:
            error_response = ErrorResponse(
                status=False,
                error="Community not found",
                detail=f"Community {community_id} not found"
            )
            return JSONResponse(
                status_code=404,
                content=error_response.model_dump()
            )
        return JSONResponse(content=community_data.model_dump(), status_code=200)
    except Exception as e:
        print("Exception while getting data from MongoDB\nError Message from routes/CommunityRoutes.py get_community function")
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@community_router.get('/user/{username}', response_class=JSONResponse)
async def get_user_communities(username: str):
    try:
        communities = community_util.get_user_communities(username)
        if not communities:
            return JSONResponse(
                content={"message": "No communities found", "communities": []},
                status_code=200
            )
        
        return JSONResponse(
            content={"message": "Communities fetched successfully", 
                    "communities": [comm.model_dump(mode='json') for comm in communities]},
            status_code=200
        )
    except Exception as e:
        print("Exception while fetching latest communities:", e)
        raise HTTPException(status_code=400, detail=str(e))

@community_router.get('/latest/', response_class=JSONResponse)
async def get_latest_communities(limit: int = 10, page:int = 1):
    try:
        communities = community_util.get_latest_communities(limit)
        if not communities:
            return JSONResponse(
                content={"message": "No communities found", "communities": []},
                status_code=200
            )
        
        return JSONResponse(
            content={"message": "Communities fetched successfully", 
                    "communities": [comm.model_dump() for comm in communities]},
            status_code=200
        )
    except Exception as e:
        print("Exception while fetching latest communities:", e)
        raise HTTPException(status_code=400, detail=str(e))
    
@community_router.post('/search/skills', response_class=JSONResponse)
async def search_communities_by_skills(search: SearchCommunityBySkills):
    try:
        communities = community_util.search_community_by_skills(skills=search.skills, limit=search.limit)
        if not communities:
            return JSONResponse(
                content={"message": "No communities found", "communities": []},
                status_code=200
            )
        
        return JSONResponse(
            content={"message": "Communities fetched successfully", 
                    "communities": [comm.model_dump() for comm in communities]},
            status_code=200
        )
    except Exception as e:
        print("Exception while fetching latest communities:", e)
        raise HTTPException(status_code=400, detail=str(e))
    
