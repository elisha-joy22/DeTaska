from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.work_type import WorkType

router = APIRouter(prefix="/work_types", tags=["Work Types"])

@router.post("/", response_model= WorkType)
def create_work_type(work_type: WorkType, session: Session = Depends(get_session)):
    session.add(work_type)
    session.commit()
    session.refresh(work_type)
    return work_type


@router.get("/", response_model= list[WorkType])
def get_work_types(session: Session = Depends(get_session)):
    work_types = session.exec(select(WorkType)).all()
    return work_types


@router.get("/{work_type_id}", response_model=WorkType)
def get_work_type(work_type_id: int, updated_work_type: WorkType, session: Session = Depends(get_session)):
    work_type = session.get(WorkType, work_type_id)
    if not work_type:
        raise HTTPException(status_code=404, detail= "Work type not found")
    
    work_type.name = updated_work_type.name
    work_type.description = updated_work_type.description

    session.add(work_type)
    session.commit()
    session.refresh(work_type)
    return work_type


@router.delete("/{work_type_id}")
def delete_work_type(work_type_id: int, session:Session = Depends(get_session)):
    work_type = session.get(WorkType, work_type_id)
    if not work_type_id:
        raise HTTPException(status_code=404, detail= "Work type not found")
    
    session.delete(work_type)
    session.commit()

    return {"message": "Work Type deleted successfully"}
