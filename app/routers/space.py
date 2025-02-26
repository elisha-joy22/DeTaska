from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

from app.models.space import Space
from app.database import get_session

router = APIRouter(prefix="/spaces", tags=["Spaces"])


@router.post("/", response_model=Space)
def create_space(space: Space ,session: Session = Depends(get_session)):
    session.add(space)
    session.commit()
    session.refresh(space)
    return space


@router.get("/", response_model=list[Space])
def get_spaces(space: Space ,session: Session = Depends(get_session)):
    spaces = session.exec(select(Space)).all()
    return spaces


@router.get("/{space_id}", response_model=Space)
def get_space(space_id: int, session: Session = Depends(get_session)):
    space = session.get(Space, space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    return space


@router.put("/{space_id}", response_model=Space)
def update_space(space_id: int, updated_space: Space, session: Session = Depends(get_session)):
    space = session.get(Space, space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    space.name = updated_space.name
    space.parent_space = updated_space.parent_space   #might turn into a bug--do research
    space.type = updated_space.type
    space.status = updated_space.status

    session.add(space)
    session.commit()
    session.refresh(space)
    return space


@router.delete("/{space_id}")
def delete_space(space_id: int, session: Session = Depends(get_session)):
    space = session.get(Space, space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    
    session.delete(space)
    session.commit()
    return {"message": "Space deleted successfully"}

