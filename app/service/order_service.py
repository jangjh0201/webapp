from sqlalchemy.orm import Session
from database.crud.ice_cream import read_all_ice_creams
from database.crud.topping import read_all_toppings
from database.crud.consumable import read_all_consumables
from database.crud.order import (
    create_order,
    read_all_orders,
)
from utils.utils import get_item_id_by_name
from models.models import IceCream, Topping, Consumable
from fastapi import HTTPException


def show_order(db: Session):
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    consumables = [c for c in consumables if c.name != "cup"]
    return ice_creams, toppings, consumables


def add_order(ice_cream_id: int, topping_ids: str, consumable_ids: str, db: Session):
    topping_ids_list = (
        [int(id) for id in topping_ids.split(",") if id] if topping_ids else []
    )
    consumable_ids_list = (
        [int(id) for id in consumable_ids.split(",") if id] if consumable_ids else []
    )

    details = []

    # 아이스크림 재고 확인
    ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
    if ice_cream is None:
        details.append({"type": "icecream", "name": "unknown", "code": 404})
    elif ice_cream.quantity <= 0:
        details.append({"type": "icecream", "name": ice_cream.name, "code": 409})

    # 토핑 재고 확인
    for topping_id in topping_ids_list:
        topping = db.query(Topping).filter(Topping.id == topping_id).first()
        if topping is None:
            details.append({"type": "topping", "name": "unknown", "code": 404})
        elif topping.quantity <= 0:
            details.append({"type": "topping", "name": topping.name, "code": 409})

    # 소모품 재고 확인
    for consumable_id in consumable_ids_list:
        consumable = db.query(Consumable).filter(Consumable.id == consumable_id).first()
        if consumable is None:
            details.append({"type": "consumable", "name": "unknown", "code": 404})
        elif consumable.quantity <= 0:
            details.append({"type": "consumable", "name": consumable.name, "code": 409})

    # 컵 재고 확인
    cup = db.query(Consumable).filter(Consumable.name == "cup").first()
    if cup is None:
        details.append({"type": "consumable", "name": "cup", "code": 404})
    elif cup.quantity <= 0:
        details.append({"type": "consumable", "name": "cup", "code": 409})

    if details:
        raise HTTPException(status_code=400, detail=details)
    else:
        # 재고가 충분하면 주문 생성
        create_order(db, ice_cream_id, topping_ids_list, consumable_ids_list)
        details = [{"code": 201}]
        return details


async def add_order_by_kiosk(order_details: dict, db: Session):
    icecream = order_details.get("icecream")
    topping = order_details.get("topping")

    if not icecream:
        raise HTTPException(
            status_code=400, detail=[{"type": "icecream", "name": "required"}]
        )

    details = []

    # 아이스크림 존재 or 재고 여부 확인
    ice_cream_id = get_item_id_by_name(db, "ice_cream", icecream)
    if ice_cream_id is None:
        details.append({"type": "icecream", "name": icecream, "code": 404})
    else:
        ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
        if ice_cream.quantity <= 0:
            details.append({"type": "icecream", "name": icecream, "code": 409})

    # 토핑 존재 or 재고 여부 확인
    topping_ids_list = []
    if topping:
        for name in topping.split(","):
            topping_id = get_item_id_by_name(db, "topping", name.strip())
            if topping_id is None:
                details.append({"type": "topping", "name": name.strip(), "code": 404})
            else:
                topping_item = (
                    db.query(Topping).filter(Topping.id == topping_id).first()
                )
                if topping_item.quantity <= 0:
                    details.append(
                        {"type": "topping", "name": name.strip(), "code": 409}
                    )
                topping_ids_list.append(topping_id)

    # 컵 재고 여부 확인
    cup = db.query(Consumable).filter(Consumable.name == "cup").first()
    if cup.quantity <= 0:
        details.append({"type": "consumable", "name": "cup", "code": 409})

    if details:
        raise HTTPException(status_code=400, detail=details)

    order = create_order(db, ice_cream_id, topping_ids_list, consumable_ids=[])

    response_content = {
        "orderId": order.id,
        # "detail": {
        #     "icecream": icecream,
        #     "topping": topping,
        # },
    }
    return response_content


def show_history(db: Session):
    orders = read_all_orders(db)
    return orders
