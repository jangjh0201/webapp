import json
import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "db")))

from database.tables import initailize
from database.session import SessionLocal
from models.models import OtherItem, Topping
from crud.ice_cream import create_ice_cream, get_all_ice_creams
from crud.topping import create_topping, get_all_toppings
from crud.other_item import create_other_item, get_all_other_items
from crud.order import create_order, get_all_orders
from crud.inventory import create_inventory, get_all_inventory


def main():
    # 초기화
    initailize

    # 데이터베이스 연결
    db = SessionLocal()

    # 예제 데이터 추가
    vanilla = create_ice_cream(db, "바닐라", 2500)
    chocolate = create_ice_cream(db, "초콜릿", 2500)
    strawberry = create_ice_cream(db, "딸기", 2500)

    oreo = create_topping(db, "오레오", 300)
    choco_ball = create_topping(db, "초코볼", 300)
    cereal = create_topping(db, "시리얼", 400)

    cup = create_other_item(db, "컵", 500)
    spoon = create_other_item(db, "숟가락", 100)
    holder = create_other_item(db, "홀더", 100)

    # 예제 재고 추가
    create_inventory(db, "ice_cream", strawberry.id, 100)
    create_inventory(db, "ice_cream", vanilla.id, 100)
    create_inventory(db, "ice_cream", chocolate.id, 80)

    create_inventory(db, "topping", oreo.id, 80)
    create_inventory(db, "topping", choco_ball.id, 150)
    create_inventory(db, "topping", cereal.id, 120)

    create_inventory(db, "other_item", cup.id, 200)
    create_inventory(db, "other_item", spoon.id, 300)
    create_inventory(db, "other_item", holder.id, 200)

    # 예제 주문 추가 (다중 토핑 포함, 스푼은 선택적)
    create_order(db, "바닐라", topping_names=["초코볼", "시리얼", "오레오"])
    create_order(db, "딸기", other_item_names=["홀더"], topping_names=["초코볼"])
    create_order(db, "초콜릿", other_item_names=["숟가락", "홀더"])
    create_order(db, "바닐라", topping_names=["초코볼", "시리얼"])

    # 모든 아이스크림 조회
    ice_creams = get_all_ice_creams(db)
    print("아이스크림 목록:")
    for ice_cream in ice_creams:
        print(f"ID: {ice_cream.id}, 이름: {ice_cream.name}, 가격: {ice_cream.price}")

    # 모든 토핑 조회
    toppings = get_all_toppings(db)
    print("토핑 목록:")
    for topping in toppings:
        print(f"ID: {topping.id}, 이름: {topping.name}, 가격: {topping.price}")

    # 모든 기타 품목 조회
    other_items = get_all_other_items(db)
    print("기타 품목 목록:")
    for other_item in other_items:
        print(f"ID: {other_item.id}, 이름: {other_item.name}, 가격: {other_item.price}")

    # 모든 재고 조회
    inventory = get_all_inventory(db)
    print("재고 목록:")
    for inv in inventory:
        print(
            f"Item Type: {inv.item_type}, Item ID: {inv.item_id}, Quantity: {inv.quantity}"
        )

    # 모든 주문 조회
    orders = get_all_orders(db)
    print("주문 목록:")
    for order in orders:
        other_item_ids = json.loads(order.other_item_ids)
        other_item_names = [
            db.query(OtherItem).filter(OtherItem.id == item_id).first().name
            for item_id in other_item_ids
        ]
        toppings_ids = json.loads(order.toppings) if order.toppings else []
        toppings_names = [
            db.query(Topping).filter(Topping.id == topping_id).first().name
            for topping_id in toppings_ids
        ]
        print(
            f"ID: {order.id}, Ice Cream ID: {order.ice_cream_id}, Other Items: {other_item_names}, Toppings: {toppings_names}, Order Time: {order.order_time}"
        )

    # 세션 닫기
    db.close()


if __name__ == "__main__":
    main()
