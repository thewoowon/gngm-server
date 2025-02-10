from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.chat import Chat
from app.models.chat_participant import ChatParticipant
from app.models.delivery import Delivery
from app.models.message import Message
from fastapi.responses import JSONResponse
from app.models.address import Address
from app.utils.math import haversine


async def create_article(request: Request, db: Session, user_id: str):
    try:
        data = await request.json()

        db_article = Article(
            title=data.get("title"),
            contents=data.get("contents"),
            article_type=data.get("articleType"),
            pick_up_location=data.get("pickUpLocation"),
            pick_up_date=data.get("pickUpDate"),
            pick_up_time=data.get("pickUpTime"),
            destination=data.get("destination"),
            departure_date=data.get("departureDate"),
            number_of_recruits=5,
            process_status=data.get("processStatus"),
            user_id=user_id
        )

        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        # 역기서 address를 생성하고 article에 연결
        # 여기서 다음 카카오 검색

        # 전달해주세요인 경우 추가로 address 생성
        if data.get("articleType") == 'passItOn':
            db_address_destination = Address(
                address_string=data.get("destination"),
                postal_code="12345",
                latitude=data.get("latitude1"),
                longitude=data.get("longitude1"),
                article_id=db_article.id
            )

            db.add(db_address_destination)
            db.commit()
            db.refresh(db_address_destination)

        db_address_location = Address(
            address_string=data.get("pickUpLocation"),
            postal_code="12345",
            latitude=data.get("latitude2"),
            longitude=data.get("longitude2"),
            article_id=db_article.id
        )

        db.add(db_address_location)
        db.commit()
        db.refresh(db_address_location)

        # 채팅방 생성
        db_new_chat = Chat(
            founder_id=user_id,
            article_id=db_article.id
        )

        db.add(db_new_chat)
        db.commit()
        db.refresh(db_new_chat)

        db_chat_participant = ChatParticipant(
            chat_id=db_new_chat.id,
            user_id=user_id,
            role="founder"
        )

        db.add(db_chat_participant)
        db.commit()
        db.refresh(db_new_chat)

        return JSONResponse(content={"message": "Article created successfully",
                                     "article_id": db_article.id
                                     }, status_code=201)
    except Exception as e:
        print("Error:", e)
        print("Failed to verify token")
        raise HTTPException(status_code=400, detail="Invalid token")


def update_article(request: Request, db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    db_article.title = request.title if request.title else db_article.title
    db_article.contents = request.contents if request.contents else db_article.contents
    db_article.article_type = request.article_type if request.article_type else db_article.article_type
    db_article.pick_up_location = request.pick_up_location if request.pick_up_location else db_article.pick_up_location
    db_article.pick_up_time = request.pick_up_time if request.pick_up_time else db_article.pick_up_time
    db_article.destination = request.destination if request.destination else db_article.destination
    db_article.departure_date = request.departure_date if request.departure_date else db_article.departure_date
    db_article.number_of_recruits = request.number_of_recruits if request.number_of_recruits else db_article.number_of_recruits
    db_article.process_status = request.process_status if request.process_status else db_article.process_status

    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return JSONResponse(content={"message": "Article deleted successfully"}, status_code=200)


def get_article_by_id(db: Session, article_id: int):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def get_article_with_messages_by_id(db: Session, article_id: int):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    chat = db.query(Chat).filter(Chat.article_id == article.id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # article에 top messages를 추가
    messages = db.query(Message).filter(
        Message.chat_id == chat.id).order_by(Message.id.desc()).limit(5).all()

    article.messages = messages
    return article


def get_article_by_user_id(db: Session, user_id: int):
    # 나의 article을 가져옴
    articles = db.query(Article).filter(Article.user_id == user_id).all()

    if not articles:
        return []

    return articles


def get_article_with_messages_by_user_id(db: Session, user_id: int):
    # 나의 article을 가져옴
    articles = db.query(Article).filter(Article.user_id == user_id).all()

    if not articles:
        return []

    for article in articles:
        chat = db.query(Chat).filter(Chat.article_id == article.id).first()
        if chat:
            messages = db.query(Message).filter(
                Message.chat_id == chat.id).order_by(Message.id.desc()).limit(5).all()
            article.messages = messages

    return articles

# 내가 요청한 아티클의 정보가 가져오기
def get_article_on_my_request(db: Session, user_id: int):
    # 나의 delivery를 가져옴
    deliveries = db.query(Delivery).filter(Delivery.user_id == user_id).all()
    # 나의 deliveries의 article_id를 가져옴
    article_ids = [delivery.article_id for delivery in deliveries]
    # article_ids를 이용해서 article을 가져옴
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()

    if not articles:
        return []

    results = []

    for article in articles:
        delivery = db.query(Delivery).filter(
            Delivery.user_id == user_id).first()
        # delivery의 user_id가 나인 경우
        if delivery:
            results.append(article)

    return results


def get_article_with_messages_on_my_request(db: Session, user_id: int):
    # 나의 delivery를 가져옴
    deliveries = db.query(Delivery).filter(Delivery.user_id == user_id).all()
    # 나의 deliveries의 article_id를 가져옴
    article_ids = [delivery.article_id for delivery in deliveries]
    # article_ids를 이용해서 article을 가져옴
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()

    if not articles:
        return []

    results = []

    for article in articles:
        delivery = db.query(Delivery).filter(
            Delivery.user_id == user_id).first()
        # delivery의 user_id가 나인 경우
        if delivery:
            chat = db.query(Chat).filter(Chat.article_id == article.id).first()
            if chat:
                messages = db.query(Message).filter(
                    Message.chat_id == chat.id).order_by(Message.id.desc()).limit(5).all()
                article.messages = messages
            results.append(article)

    return results


def get_article_by_location(db: Session, request: Request):

    # latitude: number;
    # longitude: number;
    # distance: number;

    data = request.query_params
    latitude = float(data.get("latitude"))
    longitude = float(data.get("longitude"))
    fix_distance = int(data.get("distance"))

    # 모든 article을 가져온 후 article의 address와 위도 경도를 비교해서 거리 계산
    # 거리가 distance보다 작은 article만 반환, distance는 km 단위로 계산
    # 거리 계산은 위도 경도를 이용해서 계산, 곡선 거리 계산법 사용

    articles = db.query(Article).all()
    results = []

    for article in articles:
        # article.address는 이미 연결되어 있음
        address = db.query(Address).filter(
            Address.article_id == article.id).first()

        if address:
            # 거리 계산
            # 곡선 거리 계산법 사용
            # 거리가 distance보다 작으면 반환
            distance = haversine(
                latitude, longitude, float(address.latitude), float(address.longitude))
            if distance < fix_distance:
                results.append(article)

    return results
