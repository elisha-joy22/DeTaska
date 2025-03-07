from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.work_assignment import TaskCategory

router = APIRouter(prefix="/task-categories", tags=["Task Categories"])


@router.post("/", response_model=TaskCategory)
def create_task_category(task_category: TaskCategory, session: Session = Depends(get_session)):
    """Create a new task category."""
    session.add(task_category)
    session.commit()
    session.refresh(task_category)
    return task_category


@router.get("/", response_model=list[TaskCategory])
def get_task_categories(session: Session = Depends(get_session)):
    """Retrieve all task categories."""
    categories = session.exec(select(TaskCategory)).all()
    return categories


@router.get("/{category_id}", response_model=TaskCategory)
def get_task_category(category_id: int, session: Session = Depends(get_session)):
    """Retrieve a specific task category by ID."""
    category = session.get(TaskCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Task Category not found")
    return category


@router.put("/{category_id}", response_model=TaskCategory)
def update_task_category(category_id: int, updated_category: TaskCategory, session: Session = Depends(get_session)):
    """Update an existing task category."""
    category = session.get(TaskCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Task Category not found")

    category.name = updated_category.name
    category.description = updated_category.description

    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_task_category(category_id: int, session: Session = Depends(get_session)):
    """Delete a task category."""
    category = session.get(TaskCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Task Category not found")

    session.delete(category)
    session.commit()
    return {"message": "Task Category deleted successfully"}
