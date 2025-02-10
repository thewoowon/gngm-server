from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.delivery import DeliveryResponse
from app.services.delivery_service import create_delivery, get_delivery_by_id, get_delivery_by_user_id, delete_delivery
from app.dependencies import get_db
from app.core.security import get_current_user
from typing import List


router = APIRouter()


@router.get("/all", response_model=List[DeliveryResponse])
def read_all(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_delivery_by_user_id(db=db, user_id=user_id)


@router.get("/one/{delivery_id}", response_model=DeliveryResponse)
def read_one(delivery_id: int, db: Session = Depends(get_db)):
    return get_delivery_by_id(db=db, delivery_id=delivery_id)


@router.post("/create", response_model=DeliveryResponse)
async def create(request: Request, db: Session = Depends(get_db), user_id: str = Depends(get_current_user),):
    return await create_delivery(db=db, request=request, user_id=user_id)


# @router.put("/update", response_model=DeliveryResponse)
# def update(request: Request, db: Session = Depends(get_db)):
#     return update_delivery(db=db, request=request)


@router.delete("/delete/{delivery_id}")
async def delete(delivery_id: int, db: Session = Depends(get_db)):
    return await delete_delivery(db=db, delivery_id=delivery_id)
