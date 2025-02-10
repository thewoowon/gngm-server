from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from app.schemas.message import MessageResponse
from app.models.message import Message
from fastapi.responses import JSONResponse


async def create_message(request: Request, db: Session, chat_id: int, user_id: int):
    try:
        data = await request.json()
        db_message = Message(
            message=data.get("content"),
            sender_id=user_id,
            chat_id=chat_id
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return JSONResponse(content={"message": "Message created successfully", "message_id": db_message.id}, status_code=201)

    except Exception as e:
        print("Error:", e)
        print("Failed to verify token")
        raise HTTPException(status_code=400, detail="Invalid token")


async def update_message(request: Request, db: Session,  message_id: int):
    try:
        data = await request.json()
        db_message = db.query(Message).filter(Message.id == message_id).first()
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        db_message.message = data.get("message")
        db.commit()
        db.refresh(db_message)
        return JSONResponse(content={"message": "Message updated successfully"}, status_code=200)

    except Exception as e:
        print("Error:", e)
        print("Failed to verify token")
        raise HTTPException(status_code=400, detail="Invalid token")


async def delete_message(db: Session, message_id: int):
    try:
        db_message = db.query(Message).filter(Message.id == message_id).first()
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        db.delete(db_message)
        db.commit()
        return JSONResponse(content={"message": "Message deleted successfully"}, status_code=200)
    except Exception as e:
        print("Error:", e)
        print("Failed to verify token")
        raise HTTPException(status_code=400, detail="Invalid token")


def get_message_by_chat_id(db: Session, take: int, skip: int, chats_id: int):
    db_messages = db.query(Message).filter(Message.chat_id == chats_id).all()
    if not db_messages:
        return []
    return db_messages


def get_message_by_id(db: Session, message_id: int):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if not db_message:
        return HTTPException(status_code=404, detail="Message not found")
    return db_message
