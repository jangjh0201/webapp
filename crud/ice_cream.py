from sqlalchemy.orm import Session
from models.models import IceCream


# 이름을 받아 기타 품목을 생성합니다.
def create_ice_cream(db: Session, name: str, price: int):

# 이름으로 특정 기타 품목을 조회합니다.
def read_ice_cream_by_name():

# 모든 기타 품목들을 조회합니다.
def read_all_ice_creams(db: Session):

# 이름으로 특정 기타 품목을 삭제합니다.
def delete_ice_cream_by_name(db: Session, name: str):

# 모든 기타 품목을 삭제합니다.
def delete_all_ice_creams(db: Session):
