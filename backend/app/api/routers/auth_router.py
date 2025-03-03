from fastapi import APIRouter, Request, HTTPException, status, Depends
from datetime import timedelta
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport.requests import Request
import requests
from google_auth_oauthlib.flow import Flow
from settings import settings
from utils.jwt import create_access_token
from services.user_service import UserService
from db.db import database
from repositories.user_repo import UserRepository
from models.user import User, UserResponse
import os

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID  # From your Google Cloud Console
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET  # From your Google Cloud Console
REDIRECT_URI = settings.GOOGLE_REDIRECT_URI
ACCESS_TOKEN_EXPIRE_HOUR = settings.ACCESS_TOKEN_EXPIRE_HOUR

flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "redirect_uris": [REDIRECT_URI],
        }
    },
    scopes=[
            "openid", 
            "https://www.googleapis.com/auth/userinfo.profile", 
            "https://www.googleapis.com/auth/userinfo.email"
        ],
    redirect_uri=REDIRECT_URI,
)
flow.redirect_uri = REDIRECT_URI  # Ensure the redirect URI is set
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP for local development

def get_user_service():
    repo = UserRepository(database)
    return UserService(repo)


router = APIRouter()

# Step 1: Redirect user to Google Login Page
@router.get("/login/google")
async def google_login():
    authorization_url, state = flow.authorization_url(prompt="consent")
    return RedirectResponse(authorization_url)

# Step 2: Handle Google OAuth Callback
@router.get("/google/callback")
async def auth_google_callback(code: str, service: UserService = Depends(get_user_service)):
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials

        id_info = id_token.verify_oauth2_token(
            credentials.id_token, Request(), GOOGLE_CLIENT_ID
        )

        if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Invalid issuer")
        
        user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {credentials.token}"}
        response = requests.get(user_info_endpoint, headers=headers)
        user_data = response.json()
        
        user = await service.get_user_by_email(user_data["email"])
        if not user:
            user_data_create = {
                "UserName": user_data["given_name"],
                "UserLastName": user_data["family_name"],
                "Email": user_data["email"],
                "Type": "Student"  
            }

            user_create = User(**user_data_create)
            user_create.set_created_at()
            user = await service.create_user(user_create)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "type": user.type},
            expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRE_HOUR)
        )

        return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))