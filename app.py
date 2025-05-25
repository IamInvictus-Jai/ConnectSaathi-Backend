from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from os import environ
from dotenv import load_dotenv; load_dotenv()


# Routes
from routes.UserRoutes import user_router
from routes.CommunityRoutes import community_router


# FastAPI Setup
app = FastAPI(
    title="ConnectSaathi",
    description="FastAPI is a modern, fast (high performance), web framework for building APIs with Python 3.6+.",
    version="0.1.1"
)

# CORS
# origins = environ.get("ALLOWED_ORIGINS", "").split(",")
origins = ["*"]
allowed_methods = [
    "GET",
    "POST"
]
allowed_headers = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)


# FastAPI Routes
@app.get("/")
async def health_check():
    return {"message": "Server is live!"}


# User Routes
app.include_router(user_router)

# Community Routes
app.include_router(community_router)