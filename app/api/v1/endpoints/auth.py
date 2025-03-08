
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.core.security import get_current_user
from app.services.auth_service import google_auth, naver_auth, kakao_auth, refresh_token_func, google_auth_web, apple_notification, guest_login, apple_auth
from app.dependencies import get_db
from sqlalchemy.orm import Session
# from fastapi import FastAPI, Header

router = APIRouter()


@router.post("/web/google")
async def google_web(request: Request, db: Session = Depends(get_db)):
    """
    Google web login
    """
    return await google_auth_web(request=request, db=db)


@router.post("/google")
async def google(request: Request, db: Session = Depends(get_db)):
    return await google_auth(request, db)


@router.post("/naver")
def naver(access_token: str):
    return naver_auth(access_token)


@router.post("/kakao")
def kakao(access_token: str):
    return kakao_auth(access_token)


@router.post("/apple")
def apple(request: Request, db: Session = Depends(get_db)):
    return apple_auth(request, db)


@router.post("/guest")
def guest(db: Session = Depends(get_db)):
    return guest_login(db)


# /auth/validate-token -> 토큰 유효성 검사
# /auth/refresh-token -> 토큰 갱신
# /auth/logout -> 로그아웃

@router.get("/validate-token")
def validate_token(user_id: int = Depends(get_current_user)):
    return JSONResponse(content={"message": "Token is valid", "user_id": user_id}, status_code=200)


@router.post("/refresh-token")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    return refresh_token_func(request, db)


@router.post("/logout")
def logout():
    pass
