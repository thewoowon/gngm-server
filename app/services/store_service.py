from sqlalchemy.orm import Session, joinedload
from app.schemas.store import StoreCreate, StoreUpdate
from app.models.store import Store
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def create_store(db: Session, store: StoreCreate):
    db_store = Store(
        name=store.name,
        address=store.address,
        store_type=store.store_type,
        business_hours=store.business_hours,
        phone_number=store.phone_number
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def update_store(db: Session, store_id: int, store: StoreUpdate):
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    db_store.name = store.name if store.name else db_store.name
    db_store.address = store.address if store.address else db_store.address
    db_store.store_type = store.store_type if store.store_type else db_store.store_type
    db_store.business_hours = store.business_hours if store.business_hours else db_store.business_hours
    db_store.phone_number = store.phone_number if store.phone_number else db_store.phone_number
    db.commit()
    db.refresh(db_store)
    return db_store


def delete_store(db: Session, store_id: int):
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(db_store)
    db.commit()
    return JSONResponse(content={"message": "Store deleted successfully"}, status_code=200)


def get_store_by_id(db: Session, store_id: int):
    db_store = db.query(Store).filter(Store.id == store_id).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


def get_store_by_name(db: Session, search_query: str):
    # like 검색, 최대 30개까지만 반환, services 관계도 함께 로드
    db_store = db.query(Store).options(joinedload(Store.services)).filter(
        Store.name.like(f"%{search_query}%")).limit(30).all()

    if not db_store:
        return []

    # db_store object를 json으로 변환
    for store in db_store:
        print(store.services)

    return db_store


def get_store_by_category(db: Session, category: str):
    # store의 services를 로드
    # services는 오브젝트 리스트이므로, 각각의 service의 service_category를 비교하여 일치하는 store를 반환
    db_store = db.query(Store).options(joinedload(Store.services)).all()

    if not db_store:
        return []

    result = []
    for store in db_store:
        for service in store.services:
            if service.service_category.code == category:
                result.append(store)
                break
    return result
