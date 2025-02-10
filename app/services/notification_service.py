from sqlalchemy.orm import Session
from app.schemas.notification import NotificationUpdate, NotificationResponse, NotificationCreate
from app.models.notification import Notification
from typing import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def delete_notification(db: Session, notification_id: int, user_id: int):
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notification)
    db.commit()
    return JSONResponse(content={"message": "Notification deleted successfully"}, status_code=200)


def delete_all_notification(db: Session, user_id: int):
    db_notifications = db.query(Notification).filter(
        Notification.user_id == user_id).all()
    # 없는 경우 그냥 리턴, 이미 없기 때문에 성공
    if not db_notifications:
        return JSONResponse(content={"message": "Notification not found"}, status_code=200)
    for db_notification in db_notifications:
        db.delete(db_notification)
    db.commit()
    return JSONResponse(content={"message": "All Notification deleted successfully"}, status_code=200)


def get_notification_by_id(db: Session, notification_id: int):
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationResponse.model_validate(db_notification)


def get_notification_by_user_id(db: Session, user_id: int):
    db_notifications = db.query(Notification).filter(
        Notification.user_id == user_id).all()
    if not db_notifications:
        return []
    return [NotificationResponse.model_validate(notification) for notification in db_notifications]
