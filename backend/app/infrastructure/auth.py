from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from settings import settings

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
)