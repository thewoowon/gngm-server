from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.models.chat_participant import ChatParticipant
from app.models.user import User
from app.schemas.chat import ChatResponse
from fastapi.responses import JSONResponse


def create_chat(db: Session, attendant_id: int, user_id: int):
    db_chat = Chat(attendant_id=attendant_id, founder_id=user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return JSONResponse(content={"message": "Chat created successfully"}, status_code=201)


def delete_chat(db: Session, chat_id: int):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(db_chat)
    db.commit()
    return JSONResponse(content={"message": "Chat deleted successfully"}, status_code=200)


def get_chat_by_id(db: Session, chat_id: int, take: int, skip: int):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db_chat.founder = db.query(User).filter(
        User.id == db_chat.founder_id).first()
    db_chat.participants = db.query(ChatParticipant).filter(
        ChatParticipant.chat_id == db_chat.id).all()
    return db_chat


def get_chat_by_user_id(db: Session, user_id: int):
    db_chats = db.query(Chat).filter(Chat.founder_id == user_id).all()
    if not db_chats:
        return []
    return db_chats
