from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from settings import settings
import os

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID  # From your Google Cloud Console
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET  # From your Google Cloud Console
REDIRECT_URI = settings.GOOGLE_REDIRECT_URI

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
    scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
    redirect_uri=REDIRECT_URI,
)
flow.redirect_uri = REDIRECT_URI  # Ensure the redirect URI is set
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP for local development


router = APIRouter()

# Step 1: Redirect user to Google Login Page
@router.get("/login/google")
async def google_login():
    authorization_url, state = flow.authorization_url()
    print(f"Authorization URL: {authorization_url}")
    print(f"Redirect URL: {REDIRECT_URI}")
    return RedirectResponse(authorization_url)

# Step 2: Handle Google OAuth Callback
@router.get("/google/callback")
async def auth_google_callback(code: str):
    try:
        # Exchange the authorization code for a token
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Verify the ID token
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, requests.Request(), GOOGLE_CLIENT_ID
        )

        # Check if the token is valid
        if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Invalid issuer")

        return {"user_info": id_info}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))