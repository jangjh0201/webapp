import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.user_controller import router as user_router
from controller.manager_controller import router as manager_router
from controller.auth_controller import router as auth_router  # 새로 추가된 라우터
from database.database import initialize_tables, SessionLocal
from database.crud.ice_cream import create_ice_cream
from database.crud.topping import create_topping
from database.crud.consumable import create_consumable

app = FastAPI()

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="app/resource/static"), name="static")

# 유저, 매니저 및 인증 라우터 등록
app.include_router(user_router)
app.include_router(
    manager_router
)  # 매니저 라우터 prefix="/manager"로 변경 시 다른 컨트롤러 수정 필요
app.include_router(auth_router)  # 새로 추가된 라우터

# 테이블 및 데이터베이스 설정
initialize_tables()

# 데이터베이스 세션
db = SessionLocal()


# 테스트용 데이터 추가
def add_test_data(db: Session):
    create_ice_cream(db, "mint", 2500, 100)
    create_ice_cream(db, "choco", 2500, 100)
    create_ice_cream(db, "strawberry", 2500, 100)
    create_topping(db, "chocoball", 500, 100)
    create_topping(db, "cereal", 700, 100)
    create_topping(db, "oreo", 700, 100)
    create_consumable(db, "cup", 0, 200)


# 테스트 데이터 추가
add_test_data(db)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
