from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from fastapi.responses import JSONResponse


async def create_order(request: Request, db: Session, user_id: str):
    try:
        data = await request.json()

        db_order = Order(
            description=data.get("description"),
            order_type=data.get("orderType"),
            store_id=data.get("storeId"),
            user_id=user_id,
            service_id=data.get("serviceId"),
        )

        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return JSONResponse(content={"message": "Order created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Order creation failed")


async def update_order(db: Session, order: OrderUpdate, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.description = order.description if order.description else db_order.description
    db_order.order_type = order.order_type if order.order_type else db_order.order_type
    db.commit()
    db.refresh(db_order)
    return OrderResponse.model_validate(db_order)


async def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return JSONResponse(content={"message": "Order deleted successfully"}, status_code=200)


def get_order_by_id(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


def get_order_by_store_id(db: Session, store_id: int):
    db_order = db.query(Order).filter(Order.store_id == store_id).all()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


def get_order_by_user_id(db: Session, user_id: int):
    db_orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not db_orders:
        return []
    return db_orders
