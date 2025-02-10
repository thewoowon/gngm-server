from pydantic import BaseModel


class PlaceBase(BaseModel):
    title: str
    link: str
    category: str
    description: str
    telephone: str
    address: str
    roadAddress: str
    mapx: str
    mapy: str


class PlaceResponse(BaseModel):

    class Config:
        from_attributes = True
