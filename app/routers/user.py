from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models.user import User
from app.dependencies import get_current_user
from app.database import get_session

router = APIRouter(prefix="/user", tags=["User Profile"])

@router.get("/me")
async def get_profile(user: User = Depends(get_current_user)):
    return {"email": user.email, "name": user.name, "profile_pic": user.profile_pic, "role": user.role}

@router.put("/me")
async def update_profile(
    name: str,
    profile_pic: str,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    user.name = name
    user.profile_pic = profile_pic
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Profile updated successfully"}
