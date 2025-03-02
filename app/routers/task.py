from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.models.task import Task, TaskStatus
from app.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create a Task
@router.post("/")
async def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Get All Tasks
@router.get("/")
async def get_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()

# Get Task by ID
@router.get("/{task_id}")
async def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update Task Status
@router.patch("/{task_id}/status")
async def update_task_status(task_id: int, status: TaskStatus, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = status
    if status == TaskStatus.IN_PROGRESS:
        task.actual_start = datetime.utcnow()
    elif status == TaskStatus.COMPLETED:
        task.actual_end = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"message": f"Task status updated to {status.value}"}

# Assign Task to a User
@router.patch("/{task_id}/assign")
async def assign_task(task_id: int, user_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.assigned_to = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"message": f"Task assigned to user {user_id}"}
