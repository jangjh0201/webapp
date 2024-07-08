# order.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Order, IceCream, Topping, OtherItem, Inventory
import json


def create_order(
    db: Session,
    ice_cream_name: str,
    other_item_names: list = [],
    topping_names: list = [],
):
    ice_cream = db.query(IceCream).filter(IceCream.name == ice_cream_name).first()
    cup = db.query(OtherItem).filter(OtherItem.name == "컵").first()
    other_items = [
        db.query(OtherItem).filter(OtherItem.name == name).first()
        for name in other_item_names
    ]
    toppings = [
        db.query(Topping).filter(Topping.name == name).first() for name in topping_names
    ]

    # 필수 품목 검증
    if not ice_cream:
        print(f"아이스크림 '{ice_cream_name}'이(가) 존재하지 않습니다.")
        return None
    if not cup:
        print(f"컵이 존재하지 않습니다.")
        return None

    # 선택 품목 검증
    for item in other_items:
        if not item:
            print(
                f"기타 품목 '{other_item_names[other_items.index(item)]}'이(가) 존재하지 않습니다."
            )
            return None
    for topping in toppings:
        if not topping:
            print(
                f"토핑 '{topping_names[toppings.index(topping)]}'이(가) 존재하지 않습니다."
            )
            return None

    # 재고 업데이트 및 주문 생성
    if update_inventory(db, "ice_cream", ice_cream.id, -1) and update_inventory(
        db, "other_item", cup.id, -1
    ):
        for item in other_items:
            if not update_inventory(db, "other_item", item.id, -1):
                print(f"{item.name} 재고가 부족합니다.")
                return None
        for topping in toppings:
            if not update_inventory(db, "topping", topping.id, -1):
                print(f"{topping.name} 토핑 재고가 부족합니다.")
                return None

        other_item_ids = [cup.id] + [item.id for item in other_items]
        toppings_ids = [topping.id for topping in toppings]
        db_order = Order(
            ice_cream_id=ice_cream.id,
            other_item_ids=json.dumps(other_item_ids),
            toppings=json.dumps(toppings_ids) if toppings else None,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        print("주문이 성공적으로 생성되었습니다.")
        return db_order
    else:
        print("재고가 부족하여 주문을 처리할 수 없습니다.")
        return None


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_orders_by_item(db: Session, item_name: str):
    ice_cream_orders = (
        db.query(Order).join(IceCream).filter(IceCream.name == item_name).all()
    )
    topping_orders = db.query(Order).filter(Order.toppings.contains(item_name)).all()
    other_item_orders = (
        db.query(Order).filter(Order.other_item_ids.contains(item_name)).all()
    )
    return ice_cream_orders + topping_orders + other_item_orders


def get_orders_by_date(db: Session, date: str):
    return db.query(Order).filter(func.date(Order.order_time) == date).all()


def delete_order_by_name(
    db: Session,
    ice_cream_name: str,
    other_item_names: list = [],
    topping_names: list = [],
):
    ice_cream = db.query(IceCream).filter(IceCream.name == ice_cream_name).first()
    cup = db.query(OtherItem).filter(OtherItem.name == "컵").first()

    if ice_cream and cup:
        other_item_ids = [cup.id] + [
            db.query(OtherItem).filter(OtherItem.name == name).first().id
            for name in other_item_names
        ]
        db_order = (
            db.query(Order)
            .filter(
                Order.ice_cream_id == ice_cream.id,
                Order.other_item_ids.contains(json.dumps(other_item_ids)),
            )
            .first()
        )
        if db_order:
            db.delete(db_order)
            db.commit()
            print(
                f"{ice_cream_name}, 컵, {', '.join(other_item_names)} 주문을 삭제했습니다."
            )
        else:
            print(
                f"{ice_cream_name}, 컵, {', '.join(other_item_names)} 주문이 존재하지 않습니다."
            )
    else:
        print("주문에 필요한 모든 필수 품목이 존재하지 않습니다.")


def delete_all_orders(db: Session):
    db.query(Order).delete()
    db.commit()
    print("모든 주문을 삭제했습니다.")


def update_inventory(db: Session, item_type: str, item_id: int, quantity_change: int):
    inventory = (
        db.query(Inventory)
        .filter(Inventory.item_type == item_type, Inventory.item_id == item_id)
        .first()
    )
    if inventory and inventory.quantity + quantity_change >= 0:
        inventory.quantity += quantity_change
        db.commit()
        return True
    else:
        return False
