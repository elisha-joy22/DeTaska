from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.work_assignment import WorkAssignment

router = APIRouter(prefix="/work-assignments", tags=["Work Assignments"])


@router.post("/", response_model=WorkAssignment)
def create_work_assignment(work_assignment: WorkAssignment, session: Session = Depends(get_session)):
    session.add(work_assignment)
    session.commit()
    session.refresh(work_assignment)
    return work_assignment


@router.get("/", response_model=list[WorkAssignment])
def get_work_assignments(session: Session = Depends(get_session)):
    work_assignments = session.exec(select(WorkAssignment)).all()
    return work_assignments

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
