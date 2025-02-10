from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.services.upload_service import upload_image
from app.dependencies import get_db
from app.core.security import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/profile")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return await upload_image(file=file, db=db, user_id=user_id)
