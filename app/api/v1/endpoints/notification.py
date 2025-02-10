from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas.notification import NotificationResponse
from app.services.notification_service import get_notification_by_user_id, get_notification_by_id, delete_notification, delete_all_notification
from app.dependencies import get_db

router = APIRouter()


@router.get("/one/{notification_id}", response_model=NotificationResponse)
def read_one(notification_id: int, db: Session = Depends(get_db)):
    return get_notification_by_id(db=db, notification_id=notification_id)


@router.get("/all", response_model=List[NotificationResponse])
def read_all(user_id: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    return get_notification_by_user_id(db=db, user_id=user_id)


@router.delete("/delete/{notification_id}")
def delete(notification_id: int, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_notification(db=db, notification_id=notification_id, user_id=user_id)


@router.delete("/delete/all")
def delete_all(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_all_notification(db=db, user_id=user_id)
