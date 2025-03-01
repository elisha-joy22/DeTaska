from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2AuthorizationCodeBearer

from dotenv import load_dotenv

import httpx
from datetime import datetime, timedelta
import jwt
import os

load_dotenv()

GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_EXPIRATION_TIMEDELTA=timedelta(hours=1)

router = APIRouter(prefix="/auth-google", tags=["Authentication-google"])


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)


@router.get("/login")
def login():
    return {
        "login_url": f"https://accounts.google.com/o/oauth2/auth"
                     f"?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}"
                     f"&response_type=code&scope=email profile"
    }


@router.get("/auth")
async def auth(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        })
        tokens = response.json()
        access_token = tokens.get("access_token")


        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to obtain access token")

        user_info = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_info.json()
        email = user_data.get("email")
        name = user_data.get("name")

        if not email:
            raise HTTPException(status_code=400, detail="Unable to get email from Google")

        # Simulate checking the database
        #if email not in db:
        #    db_user[email] = {"name": name, "email": email}

        jwt_token = jwt.encode(
        {"sub": email, "exp": datetime.utcnow() + JWT_EXPIRATION_TIMEDELTA},
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
        )
        return {"access_token": jwt_token, "token_type": "bearer"}
    
        