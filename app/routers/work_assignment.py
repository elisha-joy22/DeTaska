from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.work_assignment import WorkAssignment, WorkAssignmentDependency
from app.models.status import Status

import datetime

router = APIRouter(prefix="/work-assignments", tags=["Work Assignments"])


def calculate_priority(task: WorkAssignment, session: Session):
    """Calculate priority based on dependencies and deadline urgency."""
    dependency_count = session.exec(
        select(WorkAssignmentDependency).where(WorkAssignmentDependency.work_assignment_id == task.id)
    ).count()

    # Urgency factor: Closer the deadline, the higher the priority
    days_remaining = (task.expected_end_date - datetime.now()).days
    urgency_factor = max(1, 30 - days_remaining)  # More urgent if closer to today

    # Priority formula (Lower value = Higher priority)
    priority_score = dependency_count * 2 + urgency_factor

    return priority_score



@router.post("/", response_model=WorkAssignment)
def create_work_assignment(work_assignment: WorkAssignment, session: Session = Depends(get_session)):
    work_assignment.priority = calculate_priority(work_assignment, session)
    session.add(work_assignment)
    session.commit()
    session.refresh(work_assignment)
    return work_assignment


@router.get("/", response_model=list[WorkAssignment])
def get_work_assignments_sorted(session: Session = Depends(get_session)):
    tasks = session.exec(select(WorkAssignment).order_by(WorkAssignment.priority)).all()
    return tasks

# Get Work Assignment by ID
@router.get("/{work_assignment_id}", response_model=WorkAssignment)
def get_work_assignment(work_assignment_id: int, session: Session = Depends(get_session)):
    work_assignment = session.get(WorkAssignment, work_assignment_id)
    if not work_assignment:
        raise HTTPException(status_code=404, detail="Work Assignment not found")
    return work_assignment


@router.put("/{work_assignment_id}", response_model=WorkAssignment)
def update_work_assignment(work_assignment_id: int, updated_work_assignment: WorkAssignment, session: Session = Depends(get_session)):
    work_assignment = session.get(WorkAssignment, work_assignment_id)
    if not work_assignment:
        raise HTTPException(status_code=404, detail="Work Assignment not found")

    work_assignment.project_id = updated_work_assignment.project_id
    work_assignment.work_type_id = updated_work_assignment.work_type_id
    work_assignment.space_id = updated_work_assignment.space_id
    work_assignment.order = updated_work_assignment.order
    work_assignment.expected_start_date = updated_work_assignment.expected_start_date
    work_assignment.expected_end_date = updated_work_assignment.expected_end_date
    work_assignment.actual_start_date = updated_work_assignment.actual_start_date
    work_assignment.actual_end_date = updated_work_assignment.actual_end_date
    work_assignment.expected_cost = updated_work_assignment.expected_cost
    work_assignment.actual_cost = updated_work_assignment.actual_cost

    session.add(work_assignment)
    session.commit()
    session.refresh(work_assignment)
    return work_assignment


@router.delete("/{work_assignment_id}")
def delete_work_assignment(work_assignment_id: int, session: Session = Depends(get_session)):
    work_assignment = session.get(WorkAssignment, work_assignment_id)
    if not work_assignment:
        raise HTTPException(status_code=404, detail="Work Assignment not found")
    
    session.delete(work_assignment)
    session.commit()
    return {"message": "Work Assignment deleted successfully"}

@router.get("/{work_assignment_id}/dependencies")
def get_dependencies(work_assignment_id: int, session: Session = Depends(get_session)):
    """Retrieve dependencies for a task."""
    dependencies = session.exec(
        select(WorkAssignmentDependency.depends_on_id).where(WorkAssignmentDependency.work_assignment_id == work_assignment_id)
    ).all()
    return {"dependencies": dependencies}


@router.post("/{work_assignment_id}/dependencies/{depends_on_id}")
def add_dependency(work_assignment_id: int, depends_on_id: int, session: Session = Depends(get_session)):
    """Add a dependency between two tasks."""
    if work_assignment_id == depends_on_id:
        raise HTTPException(status_code=400, detail="A task cannot depend on itself.")

    existing_dependency = session.exec(
        select(WorkAssignmentDependency).where(
            (WorkAssignmentDependency.work_assignment_id == work_assignment_id) &
            (WorkAssignmentDependency.depends_on_id == depends_on_id)
        )
    ).first()

    if existing_dependency:
        raise HTTPException(status_code=400, detail="Dependency already exists.")

    dependency = WorkAssignmentDependency(
        work_assignment_id=work_assignment_id,
        depends_on_id=depends_on_id
    )
    session.add(dependency)
    session.commit()
    return {"message": "Dependency added successfully"}


@router.put("/{work_assignment_id}/start")
def start_work_assignment(work_assignment_id: int, session: Session = Depends(get_session)):
    """Start a task only if all dependencies are completed."""
    work_assignment = session.get(WorkAssignment, work_assignment_id)
    if not work_assignment:
        raise HTTPException(status_code=404, detail="Work Assignment not found.")

    dependencies = session.exec(
        select(WorkAssignmentDependency.depends_on_id).where(WorkAssignmentDependency.work_assignment_id == work_assignment_id)
    ).all()

    # Ensure all dependencies are completed
    for dep_id in dependencies:
        dependent_task = session.get(WorkAssignment, dep_id)
        if dependent_task and dependent_task.status != Status.COMPLETED:
            raise HTTPException(status_code=400, detail=f"Cannot start task. Dependency {dep_id} is not completed.")

    work_assignment.status = Status.IN_PROGRESS
    session.add(work_assignment)
    session.commit()
    return {"message": "Task started successfully"}


@router.delete("/{work_assignment_id}/dependencies/{depends_on_id}")
def remove_dependency(work_assignment_id: int, depends_on_id: int, session: Session = Depends(get_session)):
    """Remove a dependency."""
    dependency = session.exec(
        select(WorkAssignmentDependency).where(
            (WorkAssignmentDependency.work_assignment_id == work_assignment_id) &
            (WorkAssignmentDependency.depends_on_id == depends_on_id)
        )
    ).first()

    if not dependency:
        raise HTTPException(status_code=404, detail="Dependency not found.")

    session.delete(dependency)
    session.commit()
    return {"message": "Dependency removed successfully"}