import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database import initialize_tables
from database.database import SessionLocal
from models.models import IceCream, Topping, Consumable, Order
from crud.ice_cream import (
    create_ice_cream,
    get_all_ice_creams,
    get_ice_cream_by_id,
    update_ice_cream,
    delete_ice_cream_by_id,
    delete_all_ice_creams,
)
from crud.topping import (
    create_topping,
    get_all_toppings,
    get_topping_by_id,
    update_topping,
    delete_topping_by_id,
    delete_all_toppings,
)
from crud.consumable import (
    create_consumable,
    get_all_consumables,
    get_consumable_by_id,
    update_consumable,
    delete_consumable_by_id,
    delete_all_consumables,
)
from crud.order import (
    create_order,
    get_all_orders,
    get_order_by_id,
    update_order,
    delete_order_by_id,
    delete_all_orders,
)


def test_crud_operations():
    # 초기화
    initialize_tables()

    # 데이터베이스 연결
    db = SessionLocal()

    # 아이스크림 생성 및 조회 테스트
    vanilla = create_ice_cream(db, "바닐라", 2500, 100)
    chocolate = create_ice_cream(db, "초콜릿", 2500, 100)
    strawberry = create_ice_cream(db, "딸기", 2500, 100)

    print("특정 아이스크림 조회:", get_ice_cream_by_id(db, vanilla.id))
    print("전체 아이스크림 조회:", get_all_ice_creams(db))

    update_ice_cream(db, vanilla.id, price=3200)
    print("업데이트된 아이스크림 조회:", get_ice_cream_by_id(db, vanilla.id))

    # 토핑 생성 및 조회 테스트
    choco_ball = create_topping(db, "초코볼", 500, 100)
    cereal = create_topping(db, "시리얼", 700, 100)

    print("특정 토핑 조회:", get_topping_by_id(db, choco_ball.id))
    print("전체 토핑 조회:", get_all_toppings(db))

    update_topping(db, choco_ball.id, price=600)
    print("업데이트된 토핑 조회:", get_topping_by_id(db, choco_ball.id))

    # 소모품 생성 및 조회 테스트
    cup = create_consumable(db, "컵", 200, 100)
    spoon = create_consumable(db, "스푼", 100, 100)
    holder = create_consumable(db, "홀더", 300, 100)

    print("특정 소모품 조회:", get_consumable_by_id(db, cup.id))
    print("전체 소모품 조회:", get_all_consumables(db))

    update_consumable(db, cup.id, price=250)
    print("업데이트된 소모품 조회:", get_consumable_by_id(db, cup.id))

    # 주문 생성 및 조회 테스트
    order1 = create_order(db, vanilla.id, [choco_ball.id, cereal.id], [cup.id])
    order2 = create_order(db, strawberry.id, [], [spoon.id, holder.id])

    print("특정 주문 조회:", get_order_by_id(db, order1.id))
    print("전체 주문 조회:", get_all_orders(db))

    print("특정 아이스크림 조회 (주문 후):", get_ice_cream_by_id(db, vanilla.id))
    print("특정 토핑 조회 (주문 후):", get_topping_by_id(db, choco_ball.id))
    print("특정 소모품 조회 (주문 후):", get_consumable_by_id(db, cup.id))

    update_order(
        db,
        order1.id,
        ice_cream_id=strawberry.id,
        topping_ids=[cereal.id],
        consumable_ids=[holder.id],
    )
    print("업데이트된 주문 조회:", get_order_by_id(db, order1.id))

    print("전체 주문 조회:", get_all_orders(db))

    print("전체 토핑 조회:", get_all_toppings(db))

    print("전체 소모품 조회:", get_all_consumables(db))

    print("전체 아이스크림 조회:", get_all_ice_creams(db))

    # delete_order_by_id(db, order2.id)
    # delete_all_orders(db)
    # delete_topping_by_id(db, cereal.id)
    # delete_all_toppings(db)
    # delete_consumable_by_id(db, spoon.id)
    # delete_all_consumables(db)
    # delete_ice_cream_by_id(db, chocolate.id)
    # delete_all_ice_creams(db)

    # 세션 닫기
    db.close()


if __name__ == "__main__":
    test_crud_operations()
