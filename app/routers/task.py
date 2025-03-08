from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.database import get_session
from app.models.task import Task, TaskStatus
from app.models.work_assignment import WorkAssignment
from app.dependencies import get_current_user
from app.services.task_service import adjust_task_priority
from app.models.status import Status

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create a Task
@router.post("/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Get All Tasks
@router.get("/", response_model=list[Task])
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks


# Get Task by ID
@router.get("/{task_id}")
async def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update Task Status
@router.put("/{task_id}/status")
def update_task_status(task_id: int, status: Status, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status

    # Ensure we don't override existing start or end timestamps
    if status == Status.IN_PROGRESS and not task.actual_start:
        task.actual_start = datetime.utcnow()  # Only set if it's not already recorded

    elif status == Status.COMPLETED and not task.actual_end:
        task.actual_end = datetime.utcnow()  # Only set if it's not already recorded

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


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



@router.put("/{task_id}/update", response_model=WorkAssignment)
def update_task(task_id: int, updated_task: WorkAssignment, session: Session = Depends(get_session)):
    task = session.get(WorkAssignment, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the task fields
    task.expected_start_date = updated_task.expected_start_date
    task.expected_end_date = updated_task.expected_end_date
    task.actual_start_date = updated_task.actual_start_date
    task.actual_end_date = updated_task.actual_end_date
    task.expected_cost = updated_task.expected_cost
    task.actual_cost = updated_task.actual_cost

    session.add(task)
    session.commit()
    session.refresh(task)

    # Call the priority adjustment function
    adjust_task_priority(session, task_id)

    return task
