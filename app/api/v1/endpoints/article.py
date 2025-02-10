from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.article import ArticleResponse
from app.services.article_service import create_article, get_article_by_id, get_article_by_location, get_article_by_user_id, update_article, delete_article, get_article_on_my_request, get_article_with_messages_by_user_id, get_article_with_messages_by_id, get_article_with_messages_on_my_request
from app.dependencies import get_db
from app.core.security import get_current_user
from typing import List

router = APIRouter()


@router.get("/one/{article_id}", response_model=ArticleResponse)
def read_one(article_id: int, db: Session = Depends(get_db)):
    return get_article_by_id(db=db, article_id=article_id)


@router.get("/all", response_model=List[ArticleResponse])
def read_all(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_article_by_user_id(db=db, user_id=user_id)


@router.get("/one/with-messages/{article_id}", response_model=ArticleResponse)
def read_one_with_messages(article_id: int, db: Session = Depends(get_db)):
    return get_article_with_messages_by_id(db=db, article_id=article_id)


@router.get("/all/with-messages", response_model=List[ArticleResponse])
def read_all_with_messages(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_article_with_messages_by_user_id(db=db, user_id=user_id)


@router.get("/request", response_model=List[ArticleResponse])
def read_by_request(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_article_on_my_request(db=db, user_id=user_id)


@router.get("/request/with-messages", response_model=List[ArticleResponse])
def read_by_request(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_article_with_messages_on_my_request(db=db, user_id=user_id)


@router.get("/location", response_model=List[ArticleResponse])
def read_by_location(request: Request, db: Session = Depends(get_db)):
    return get_article_by_location(db=db, request=request)


@router.post("/create")
async def create(request: Request, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return await create_article(request=request, db=db,  user_id=user_id)


@router.put("/update/{article_id}")
async def update(request: Request, article_id: int, db: Session = Depends(get_db)):
    return await update_article(request=request, db=db, article_id=article_id)


@router.delete("/delete/{article_id}")
async def delete(request: Request, article_id: int, db: Session = Depends(get_db)):
    return await delete_article(db=db, article_id=article_id)
