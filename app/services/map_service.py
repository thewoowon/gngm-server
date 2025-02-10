import os
import requests
from fastapi import HTTPException  # noqa
from fastapi.responses import JSONResponse


async def search_places(search_string: str):
    try:
        # https://openapi.naver.com/v1/search/local.json?query=강남구+맛집

        # X-Naver-Client-Id
        # X-Naver-Client-Secret

        response = requests.get(
            f"https://openapi.naver.com/v1/search/local.json?query={search_string}&display=10",
            headers={
                "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
                "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET")
            }
        )

        # 여기서 다음 카카오 검색
        return JSONResponse(content=response.json().get('items'), status_code=200)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=400, detail="Invalid token")
