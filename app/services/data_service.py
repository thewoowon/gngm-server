from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

CREATE_SELLER_ACCOUNT_SQL = """
        INSERT INTO user (id, name, nickname, email, phone_number, address, src, is_auto_login, accident_date, job, job_description, is_job_open, is_admin, is_deleted, user_type, status, is_seller, created_at, updated_at)
        VALUES
        (1, '김하늘' , '푸른바람' , 'haneulsky@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (2, '이도윤' , '코드마스터' , 'doyuncode@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (3, '박서연' , '미라클' , 'miraclepark@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (4, '정우진' , '데이터드리븐' , 'datawoojin@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (5, '최민준' , '알고리즘헌터' , 'algohunter@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (6, '강지윤' , '디자인캣' , 'designcat@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (7, '윤서준' , '감성코더' , 'emotionalcoder@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (8, '배수진' , '분석천재' , 'analysisqueen@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (9, '송지호' , '빛나는별' , 'shiningstar@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (10, '임나연' , '코드위자드' , 'codewizard@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00');
    """

CREATE_GENERAL_ACCOUNT_SQL = """
        INSERT INTO user (id, name, nickname, email, phone_number, address, src, is_auto_login, accident_date, job, job_description, is_job_open, is_admin, is_deleted, user_type, status, is_seller, created_at, updated_at)
        VALUES
        ( 11 , '김소연', '드림캐쳐1' , 'dreamcatcher1@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 12 , '이현우', '네오아트' , 'neoartworks@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 13 , '박민지', '피오니어' , 'pioneerpark@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 14 , '정석현', '아이디어뱅크' , 'ideabankjs@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 15 , '최다은', '아트코드' , 'artcodechoi@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 16 , '강지훈', '인스퍼레이션' , 'inspirationkj@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 17 , '윤하린', '크리에이터' , 'creatorhr@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 18 , '배준호', '메이커즈' , 'makersjoon@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 19 , '송다빈', '핸즈온' , 'handsonsong@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (20 , '임서하', '브레인박스' , 'brainboxsh@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (21 , '김재훈', '아이언핸드' , 'ironhand76@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (22 , '박은지', '크리에이티브' , 'creativepark@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (23 , '이성민', '핸즈메이커' , 'handsmaker@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (24 , '정민수', '아트마스터' , 'artmaster@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (25 , '조유진', '캔버스퀸' , 'canvasqueen@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (26 , '한지우', '드림캐쳐2' , 'dreamcatcher2@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (27 , '최다영', '블루오션' , 'blueocean@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (28 , '강현우', '메탈릭스' , 'metallics@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (29 , '윤서연', '스파클러' , 'sparkler@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        (30 , '장우성', '미니멀리스트' , 'minimalist@gmail.com','','','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/b474d0e1-13c9-4516-19a6-7b7f5a567900/public',0,'2025-01-01 00:00:00','','',0,0,0,0,0,0,'2025-01-01 00:00:00','2025-01-01 00:00:00');
"""

CREATE_SERVICE_CATEGORY_SQL = """
        INSERT INTO service_category (id, name, code, created_at, updated_at)
        VALUES
        ( 1 , '금속가공' , 'METAL' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 2 , '목재가공' , 'WOOD' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 3 , '3D프린팅' , '3DPRINT' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 4 , '아크릴가공' , 'ACRYLIC' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 5 , '인쇄' , 'PRINT' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 6 , '각인' , 'ENGRAVE' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 7 , '도색' , 'PAINT' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 8 , '플라스틱가공', 'PLASTIC' ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 9 , '그외' , 'ETC' ,'2025-01-01 00:00:00','2025-01-01 00:00:00');
"""

CREATE_STORE_SQL = """
        INSERT INTO store (id, name, address, store_type, business_hours, phone_number, representative_image, user_id, created_at, updated_at)
        VALUES
        ( 1 , '스카이메탈' , '서울시 종로구','OFFLINE' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',1,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 2 , '코드우드' , '서울시 강남구',1 ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',2,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 3 , '미라클프린트' , '부산시 해운대구','OFFLINE' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',3 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 4 , '우진레이저' , '서울시 성수동','OFFLINE' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',4 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 5 , '알고팩토리' , '인천시 남동구','OFFLINE' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',5 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 6 , '디자인랩' , '대구시 수성구','BOTH' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',6,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 7 , '감성아틀리에' , '서울시 마포구','BOTH' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',7 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 8 , '분석공방' , '광주시 서구','BOTH' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',8 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 9 , '스타프린팅' , '대전시 유성구','BOTH' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',9 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 10 , '위자드메이커스' , '서울시 강동구','BOTH' ,'09:00-18:00','010-1234-5678','https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/e2767db1-1bc8-4815-d55e-b2eaf0052000/public',10 ,'2025-01-01 00:00:00','2025-01-01 00:00:00');
"""

CREATE_SERVICE_SQL = """
        INSERT INTO service (id, name, description, unit, price, discount_rate, is_representative, representative_image, store_id, service_category_id, created_at, updated_at)
        VALUES
        ( 1 , '레이저 절단','레이저 절단' , 'cm', 1000 , 10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public', 1,1 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 2 , 'CNC 밀링','CNC 밀링' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 1,1 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 3 , '목재 절단','목재 절단' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 2,2 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 4 , 'CNC 조각','CNC 조각' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 2,2 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 5 , 'FDM 프린팅','FDM 프린팅' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 3,3 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 6 , 'SLA 프린팅','SLA 프린팅' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 3,3 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 7 , '아크릴 레이저 절단','아크릴 레이저 절단' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 4,8 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 8 , '아크릴 접착','아크릴 접착' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 4,8 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 9 , '디지털 인쇄','디지털 인쇄' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 5,4 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 10 , '오프셋 인쇄','오프셋 인쇄' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 5,4 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 11 , '가죽 공예','가죽 공예' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 6,5 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 12 , '유리 가공','유리 가공' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 6,5 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 13 , '사출 성형','사출 성형' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 7,2 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 14 , '진공 성형','진공 성형' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 7,2 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 15 , '레이저 각인','레이저 각인' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 8,3 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 16 , 'CNC 각인','CNC 각인' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 8,3 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 17 , '디지털 인쇄','디지털 인쇄' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 9,5 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 18 , '오프셋 인쇄','오프셋 인쇄' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 9,5 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 19 , '스프레이 도색','스프레이 도색' , 'cm', 1000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 10,7 ,'2025-01-01 00:00:00','2025-01-01 00:00:00'),
        ( 20 , '붓 도색','붓 도색' , 'g', 2000 ,10, 1,'https://imagedelivery.net/6qzLODAqs2g1LZbVYqtuQw/84886490-ddb1-417d-45a3-9f129e7c9b00/public' , 10,7 ,'2025-01-01 00:00:00','2025-01-01 00:00:00');
"""

SQL_STATEMENTS = [
    CREATE_SELLER_ACCOUNT_SQL,
    CREATE_GENERAL_ACCOUNT_SQL,
    CREATE_SERVICE_CATEGORY_SQL,
    CREATE_STORE_SQL,
    CREATE_SERVICE_SQL,
]


def init_data(db: Session):
    try:
        for sql in SQL_STATEMENTS:
            db.execute(text(sql))  # SQL 순차 실행
        db.commit()  # 성공 시 커밋

        # 10개 없체에 대해서 리뷰 생성 필요

        for i in range(1, 11):
            db.execute(text(f"""
                INSERT INTO review (id, title, contents, score, user_id, store_id, created_at, updated_at)
                VALUES
                ({1 + ((i-1) * 20)} , '퀄리티가 뛰어난 금속 가공!' , '정밀한 CNC 밀링 가공을 맡겼는데, 결과물이 너무 만족스럽습니다. 정말 정교하게 작업해주셨네요!' , 5 ,11,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({2 + ((i-1) * 20)} , '목재 조각이 섬세해요' , '나무 간판을 주문했는데, 조각이 정말 깔끔하게 잘 나왔어요. 만족스럽습니다!' , 5 ,12,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({3 + ((i-1) * 20)} , '3D 프린팅 속도가 아쉬워요' , '출력 품질은 좋지만 예상보다 시간이 오래 걸렸네요. 급한 작업엔 추천하기 어려울 듯!' , 3.5 ,13,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({4 + ((i-1) * 20)} , '아크릴 가공 너무 좋아요!' , '아크릴 절단도 깔끔하고, 접착 후 마감도 완벽합니다. 다음에도 이용할게요!' , 5 ,14,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({5 + ((i-1) * 20)} , '인쇄 품질이 뛰어납니다.' , '실크스크린 인쇄를 맡겼는데, 색상이 너무 예쁘고 선명하게 나왔어요!' , 3 ,15,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({6 + ((i-1) * 20)} , '레이저 각인 퀄리티 최고' , '가죽 지갑에 각인을 했는데, 너무 고급스럽고 예쁘게 나왔습니다!' , 4 ,16,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({7 + ((i-1) * 20)} , '도색 마감이 아쉬워요' , '붓칠 도색을 맡겼는데 마감이 조금 덜 깔끔해서 아쉽습니다. 그래도 색상은 만족스러워요!' , 3 ,17,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({8 + ((i-1) * 20)} , '플라스틱 가공 퀄리티 좋아요' , '진공 성형 작업이 필요했는데 정밀하게 작업해주셨습니다. 가공 시간도 빨라요!' , 5 ,18,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({9 + ((i-1) * 20)} , '가죽 공예 커스텀 너무 좋아요!' , '핸드메이드 가죽 지갑을 제작했는데, 퀄리티가 상상 이상이네요!' , 5 ,19,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({10 + ((i-1) * 20)} , '도색이 생각보다 별로네요' , '스프레이 도색을 맡겼는데 색상이 균일하지 않아요. 보완이 필요할 듯!' , 2.5 ,20,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({11 + ((i-1) * 20)} , 'CNC 가공 최고입니다!' , '금속 가공 맡겼는데 너무 깔끔하고 정밀하게 잘 나왔어요. 기술력이 뛰어나네요!' , 5 ,21,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({12 + ((i-1) * 20)} , '목재 조립이 완벽해요' , 'DIY 가구용 목재 커팅을 맡겼는데, 치수도 정확하고 맞춤 제작이 완벽했습니다!' , 5 ,22,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({13 + ((i-1) * 20)} , '3D 프린팅 마감이 너무 좋아요!' , '표면 후처리까지 맡겼는데 정말 부드럽고 매끈하게 잘 나왔어요.' , 5 ,23,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({14 + ((i-1) * 20)} , '아크릴 가공 마감이 아쉬워요' , '절단면이 살짝 거칠어서 손질이 좀 필요했습니다. 그래도 빠른 작업은 만족스러워요.' , 3 ,24,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({15 + ((i-1) * 20)} , '인쇄 색상이 정확해요' , '컬러 프린트 맡겼는데 색이 정말 정확하고 선명해요! 대만족입니다.' , 5 ,25,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({16 + ((i-1) * 20)} , '각인 글씨체 선택이 많아서 좋아요' , '각인 작업을 했는데 원하는 폰트가 다양해서 만족스러웠어요.' , 5 ,26,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({17 + ((i-1) * 20)} , '플라스틱 사출 성형이 정밀해요!' , '플라스틱 가공을 맡겼는데 치수가 완벽하게 맞아서 너무 만족스럽습니다!' , 4 ,27,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({18 + ((i-1) * 20)} , '도색 후처리가 살짝 부족했어요' , '스프레이 도색은 괜찮았는데 후처리가 조금 미흡했네요. 그래도 색상은 예쁩니다!' , 3 ,28,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({19 + ((i-1) * 20)} , '유리 가공이 정교해요!' , '세라믹 컵에 맞춰 유리를 잘라줬는데 사이즈도 정확하고 너무 깔끔해요!' , 5 ,29,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00'),
                ({20 + ((i-1) * 20)} , '레이저 각인 너무 세밀해요!' , '금속 펜에 각인을 했는데 글씨 크기가 작아도 선명하게 잘 보입니다. 대만족!' , 3.5 ,30,{i},'2025-01-01 00:00:00','2025-01-01 00:00:00');
        """))
        db.commit()  # 성공 시 커밋

        return JSONResponse(content={"message": "Data initialized successfully"}, status_code=201)
    except Exception as e:
        db.rollback()  # 실패 시 롤백
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()  # 세션 종료
