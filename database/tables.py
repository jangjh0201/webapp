# tables.py

from database.base import Base
from database.session import engine
from models.models import IceCream, Topping, OtherItem, Order, Inventory


def initailize():
    # 테이블 삭제
    Base.metadata.drop_all(bind=engine)
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
