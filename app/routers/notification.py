from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/", response_model=Notification)
def create_notification(notification: Notification, session: Session = Depends(get_session)):
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


@router.get("/", response_model=list[Notification])
def get_notifications(user_id: int, session: Session = Depends(get_session)):
    notifications = session.exec(select(Notification).where(Notification.user_id == user_id)).all()
    return notifications


@router.put("/{notification_id}/read")
def mark_as_read(notification_id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    session.add(notification)
    session.commit()
    return {"message": "Notification marked as read"}
