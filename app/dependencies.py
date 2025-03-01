from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
import jwt

from app.models.user import Role

from app.auth import SECRET_KEY, ALGORITHM
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Security(oauth2_scheme)):
    """Extract and validate the user from the JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")  # Extract user email from token
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return "db[email]"  # Return user info
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def require_role(role: Role):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_dependency
