from fastapi import APIRouter, Depends

from app.dependencies import require_role
from app.models.user import Role, User



router = APIRouter(prefix="/admin")

@router.get("/dashboard")
async def admin_dashboard(user: User = Depends(require_role(Role.ADMIN))):
    return {"message": f"Welcome Admin {user.email}!"}