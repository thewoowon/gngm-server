from fastapi import HTTPException, Request
from datetime import datetime
from app.models.chat_participant import ChatParticipant
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse
from app.models.delivery import Delivery
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


async def create_delivery(db: Session, user_id: int, request: Request):
    try:
        data = await request.json()
        now = datetime.now()

        # 날짜만 추출
        date_only = now.strftime("%Y-%m-%d")

        # 시간만 추출
        time_only = now.strftime("%H:%M:%S")
        db_delivery = Delivery(
            request_date=date_only,
            request_time=time_only,
            user_id=user_id,
            article_id=data.get('articleId'),
            order_id=data.get('orderId')
        )
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)

        # 전달 생성 후에 채팅은 생성하지 않고,
        # 채팅하기로 넘어가면 참여자 생성

        return JSONResponse(content={"message": "Delivery created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Delivery creation failed")

# 수정의 경우 참여자..?
# async def update_delivery(db: Session, request: Request):
#     data = await request.json()
#     db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
#     db_delivery.request_date = delivery.request_date if delivery.request_date else db_delivery.request_date
#     db_delivery.request_time = delivery.request_time if delivery.request_time else db_delivery.request_time
#     db.commit()
#     db.refresh(db_delivery)
#     return DeliveryResponse.model_validate(db_delivery)


async def delete_delivery(db: Session, delivery_id: int):
    db_delivery = db.query(Delivery).filter(
        Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(db_delivery)
    db.commit()
    return JSONResponse(content={"message": "Delivery deleted successfully"}, status_code=200)


def get_delivery_by_id(db: Session, delivery_id: int):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return DeliveryResponse.model_validate(delivery)


def get_delivery_by_user_id(db: Session, user_id: int):
    deliveries = db.query(Delivery).filter(Delivery.user_id == user_id).all()
    if not deliveries:
        return []
    return [DeliveryResponse.model_validate(delivery) for delivery in deliveries]
