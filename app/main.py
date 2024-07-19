import sys
import os
from fastapi import FastAPI
from sqlalchemy.orm import Session

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.controller import app
from database.database import initialize_tables, SessionLocal
from database.crud.ice_cream import create_ice_cream
from database.crud.topping import create_topping
from database.crud.consumable import create_consumable

# 테이블 및 데이터베이스 설정
initialize_tables()

# 데이터베이스 세션
db = SessionLocal()


# 테스트용 데이터 추가
def add_test_data(db: Session):
    # 아이스크림 생성
    create_ice_cream(db, "mint", 2500, 100)
    create_ice_cream(db, "choco", 2500, 0)
    create_ice_cream(db, "strawberry", 2500, 100)

    # 토핑 생성
    create_topping(db, "chocoball", 500, 0)
    create_topping(db, "cereal", 700, 100)
    create_topping(db, "oreo", 700, 100)

    # 소모품 생성
    create_consumable(db, "cup", 0, 100)


# 테스트 데이터 추가
add_test_data(db)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
