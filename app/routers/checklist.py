from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.checklist import ChecklistItem

router = APIRouter(prefix="/checklist", tags=["Cehcklists"])

@router.post("/", response_model=ChecklistItem)
def create_checklist_item(item: ChecklistItem,session: Session=Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/{work_assignment_id}", response_model=list[ChecklistItem])
def get_checklist_items(work_assignment_id: int,session: Session=Depends(get_session)):
    items = session.exec(
        select(ChecklistItem)
        .where(ChecklistItem.work_assignment_id==work_assignment_id)
    ).all()
    return items


@router.put("/{item_id}", response_model=ChecklistItem)
def update_checklist_item(item_id: int, updated_item: ChecklistItem, session: Session = Depends(get_session)):
    item = session.get(ChecklistItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    item.description = updated_item.description
    item.is_mandatory = updated_item.is_mandatory
    item.status = updated_item.status

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_checklist_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(ChecklistItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    session.delete(item)
    session.commit()
    return {"message": "Checklist item deleted successfully"}
