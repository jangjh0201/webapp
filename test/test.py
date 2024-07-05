import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import SessionLocal
from db.crud.item.ice_cream import get_all_ice_creams
from EDA.db.crud.item.topping import get_all_toppings
from db.crud.order import get_all_orders
from db.crud.inventory import get_all_inventory

# 세션을 생성합니다
db = SessionLocal()

# 모든 아이스크림 조회
ice_creams = get_all_ice_creams(db)
print("아이스크림 목록:", ice_creams)

# 모든 토핑 조회
toppings = get_all_toppings(db)
print("토핑 목록:", toppings)

# 모든 주문 조회
orders = get_all_orders(db)
print("주문 목록:", orders)

# 모든 재고 조회
inventory = get_all_inventory(db)
print("재고 목록:", inventory)

# 세션 닫기
db.close()
