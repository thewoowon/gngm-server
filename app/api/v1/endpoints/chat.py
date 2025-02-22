from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.chat import ChatCreate, ChatResponse, ChatMainResponse
from app.services.chat_service import create_chat, get_chat_by_id, get_chat_by_user_id, delete_chat
from app.dependencies import get_db
from app.core.security import get_current_user
from typing import List

router = APIRouter()


@router.post("/create")
def create(attendant_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return create_chat(db=db, attendant_id=attendant_id, user_id=user_id)


@router.get("/all", response_model=List[ChatResponse])
def read_all(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_chat_by_user_id(db=db, user_id=user_id)


@router.get("/one/{chat_id}", response_model=ChatMainResponse)
def read_one(chat_id: int, take: int = Query(...), skip: int = Query(...), db: Session = Depends(get_db)):
    return get_chat_by_id(db=db, chat_id=chat_id, take=take, skip=skip)


@router.delete("/delete/{chat_id}")
def delete(chat_id: int, db: Session = Depends(get_db)):
    return delete_chat(db=db, chat_id=chat_id)
