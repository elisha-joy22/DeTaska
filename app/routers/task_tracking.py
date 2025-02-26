from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.task_tracking import TaskTracking

router = APIRouter(prefix="/task-tracking", tags=["Task Tracking"])


@router.post("/", response_model=TaskTracking)
def create_task_tracking(task_tracking: TaskTracking, session: Session = Depends(get_session)):
    session.add(task_tracking)
    session.commit()
    session.refresh(task_tracking)
    return task_tracking


@router.get("/", response_model=list[TaskTracking])
def get_task_tracking(session: Session = Depends(get_session)):
    tasks = session.exec(select(TaskTracking)).all()
    return tasks


@router.get("/{task_tracking_id}", response_model=TaskTracking)
def get_task_tracking(task_tracking_id: int, session: Session = Depends(get_session)):
    task = session.get(TaskTracking, task_tracking_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Tracking entry not found")
    return task


@router.put("/{task_tracking_id}", response_model=TaskTracking)
def update_task_tracking(task_tracking_id: int, updated_task_tracking: TaskTracking, session: Session = Depends(get_session)):
    task = session.get(TaskTracking, task_tracking_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Tracking entry not found")

    task.work_assignment_id = updated_task_tracking.work_assignment_id
    task.checklist_item_id = updated_task_tracking.checklist_item_id
    task.status = updated_task_tracking.status
    task.assigned_person = updated_task_tracking.assigned_person
    task.notes = updated_task_tracking.notes

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_tracking_id}")
def delete_task_tracking(task_tracking_id: int, session: Session = Depends(get_session)):
    task = session.get(TaskTracking, task_tracking_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Tracking entry not found")
    
    session.delete(task)
    session.commit()
    return {"message": "Task Tracking entry deleted successfully"}
