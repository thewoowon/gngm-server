from fastapi import APIRouter
from app.services.map_service import search_places

router = APIRouter()

@router.get("/places/{search_string}")
async def read_places(search_string: str):
    return await search_places(search_string)
