from fastapi import FastAPI
from app.routers import project, work_type, space, work_assignment, expense, task_tracking


app = FastAPI()


# Include routers
app.include_router(project.router)
app.include_router(work_type.router)
app.include_router(space.router)
app.include_router(work_assignment.router)
app.include_router(expense.router)
app.include_router(task_tracking.router)

@app.get("/")
def read_root():
    return {"message": "DeTaska Backend is Running!"}
