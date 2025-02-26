from fastapi import FastAPI
from app.routers import project, work_type


app = FastAPI()


# Include routers
app.include_router(project.router)
app.include_router(work_type.router)

@app.get("/")
def read_root():
    return {"message": "DeTaska Backend is Running!"}
