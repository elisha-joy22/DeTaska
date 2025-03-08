from sqlmodel import Session
from app.models.notification import Notification


class NotificationService:
    @staticmethod
    def send_notification(session: Session, user_id: int, message: str, notif_type: str):
        """Creates and stores a notification in the database."""
        notification = Notification(
            user_id=user_id,
            message=message,
            type=notif_type
        )
        session.add(notification)
        session.commit()
