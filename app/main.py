from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

import os

from dotenv import load_dotenv

from app.routers import (
    project,
    work_type,
    space,
    work_assignment,
    expense,
    task_tracking,
    user,
    admin
)
from app.auth import auth_google

load_dotenv()

app = FastAPI()

print(os.environ.get("GOOGLE_REDIRECT_URL"))


# Include routers
app.include_router(project.router)
app.include_router(work_type.router)
app.include_router(space.router)
app.include_router(work_assignment.router)
app.include_router(expense.router)
app.include_router(task_tracking.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(auth_google.router)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "your_secret_key"))

@app.get("/")
def read_root():
    return {"message": "DeTaska Backend is Running!"}

