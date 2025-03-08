from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session

from app.models.task_tracking import TaskTracking
from app.models.checklist import ChecklistItem
from app.models.work_assignment import WorkAssignment
from app.models.status import Status

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

    try:
        # Update task tracking entry
        task.status = updated_task_tracking.status
        session.add(task)
        
        # Update Checklist Item Status
        checklist_item = session.get(ChecklistItem, task.checklist_item_id)
        if checklist_item:
            checklist_item.status = updated_task_tracking.status
            session.add(checklist_item)

        session.commit()

        # Check if all mandatory checklist items are completed
        work_assignment = session.get(WorkAssignment, task.work_assignment_id)
        if work_assignment:
            mandatory_items = session.exec(
                select(ChecklistItem).where(
                    (ChecklistItem.work_assignment_id == work_assignment.id) & 
                    (ChecklistItem.is_mandatory == True) 
                )
            ).all()

            if all(item.status == Status.COMPLETED for item in mandatory_items):
                work_assignment.status = Status.COMPLETED
                session.add(work_assignment)
                session.commit()

        session.refresh(task)
        return task

    except Exception as e:
        session.rollback()  # Rollback in case of failure
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.delete("/{task_tracking_id}")
def delete_task_tracking(task_tracking_id: int, session: Session = Depends(get_session)):
    task = session.get(TaskTracking, task_tracking_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Tracking entry not found")
    
    session.delete(task)
    session.commit()
    return {"message": "Task Tracking entry deleted successfully"}


@router.delete("/{task_tracking_id}", response_model=TaskTracking)
def delete_task_tracking(task_tracking_id: int, session: Session = Depends(get_session)):
    task = session.get(TaskTracking, task_tracking_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Tracking entry not found")

    try:
        session.delete(task)
        session.commit()
        return task  

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

