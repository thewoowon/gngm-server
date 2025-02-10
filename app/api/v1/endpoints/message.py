from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.schemas.message import MessageCreate, MessageUpdate, MessageResponse
from app.services.message_service import create_message, get_message_by_chat_id, get_message_by_id, update_message, delete_message
from app.dependencies import get_db
from typing import List

router = APIRouter()


@router.post("/create/{chat_id}")
async def create(request: Request, chat_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return await create_message(request=request, db=db, chat_id=chat_id, user_id=user_id)


@router.get("/chat/{chat_id}", response_model=List[MessageResponse])
def read_all(chat_id: int, take: int = Query(...), skip: int = Query(...), db: Session = Depends(get_db)):
    return get_message_by_chat_id(db=db, chat_id=chat_id, take=take, skip=skip)


@router.get("/one/{message_id}", response_model=MessageResponse)
def read_one(message_id: int, db: Session = Depends(get_db)):
    return get_message_by_id(db=db, message_id=message_id)


@router.put("/update/{message_id}", response_model=MessageResponse)
async def update(request: Request, message_id: int, db: Session = Depends(get_db)):
    return await update_message(request=request, db=db, message_id=message_id)


@router.delete("/delete/{message_id}")
async def delete(request: Request, message_id: int, db: Session = Depends(get_db)):
    return await delete_message(db=db, message_id=message_id)
