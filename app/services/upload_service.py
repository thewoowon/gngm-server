from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import httpx
from app.models.user import User
import os

# Cloudflare API 정보
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLIENT_ID = os.getenv("CLOUDFLARE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CLOUDFLARE_CLIENT_SECRET")
# API_TOKEN = CLOUDFLARE_API_TOKEN
# CLIENT_ID = CLOUDFLARE_CLIENT_ID
# CLIENT_SECRET = CLOUDFLARE_CLIENT_SECRET
UPLOAD_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLIENT_ID}/images/v1"


async def upload_image(file: UploadFile, db: Session, user_id: int):

    try:
        # 파일 내용 읽기
        file_content = await file.read()

        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
        }

        # 다른 서버로 POST 요청
        async with httpx.AsyncClient() as client:
            response = await client.post(
                UPLOAD_URL,
                files={"file": (file.filename, file_content,
                                file.content_type)},
                headers=headers,
            )

        # 결과 확인
        if response.status_code == 200:
            result = response.json().get("result")

            url = f"https://imagedelivery.net/{CLIENT_SECRET}/{result['id']}/public"
            # 이제 DB에 이미지 정보 저장
            user = db.query(User).filter(User.id == user_id).first()
            user.src = url
            db.commit()
            return JSONResponse(content={"message": "Image uploaded successfully", "url": url}, status_code=200)
        else:
            print("Upload Failed:", response.status_code, response.text)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
