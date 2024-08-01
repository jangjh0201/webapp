from datetime import datetime
from sqlalchemy.orm import Session
from database.crud.ice_cream import read_all_ice_creams, read_ice_cream_by_id
from database.crud.topping import read_all_toppings, read_topping_by_id
from database.crud.consumable import (
    read_all_consumables,
    read_consumable_by_id,
    read_cup,
)
from database.crud.order import (
    create_order,
    read_all_orders,
)
from utils.utils import get_item_id_by_name
from models.models import IceCream, Order, Topping, Consumable
from fastapi import HTTPException


def get_all_orders(db: Session):
    """
    모든 주문 정보 조회 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        ice_creams: 모든 아이스크림 정보 리스트
        toppings: 모든 토핑 정보 리스트
        consumables: 모든 소모품 정보 리스트
    """
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    consumables = [c for c in consumables if c.name != "cup"]
    return ice_creams, toppings, consumables


def add_order(ice_cream_id: int, topping_ids: str, consumable_ids: str, db: Session):
    """
    주문 추가 함수
    Args:
        ice_cream_id: 아이스크림 ID
        topping_ids: 토핑 ID 리스트
        consumable_ids: 소모품 ID 리스트
        db: 데이터베이스 세션
    Returns:
        order: 주문 정보
    """
    topping_ids_list = (
        [int(id) for id in topping_ids.split(",") if id] if topping_ids else []
    )
    consumable_ids_list = (
        [int(id) for id in consumable_ids.split(",") if id] if consumable_ids else []
    )

    details = []

    # 아이스크림 재고 확인
    ice_cream = read_ice_cream_by_id(db, ice_cream_id)
    if ice_cream is None:
        details.append(f"아이스크림 '{ice_cream_id}'가 존재하지 않습니다.")
    elif ice_cream.quantity <= 0:
        details.append(f"아이스크림 '{ice_cream.name}'의 재고가 부족합니다.")

    # 토핑 재고 확인
    for topping_id in topping_ids_list:
        topping = read_topping_by_id(db, topping_id)
        if topping is None:
            details.append(f"토핑 '{topping_id}'가 존재하지 않습니다.")
        elif topping.quantity <= 0:
            details.append(f"토핑 '{topping.name}'의 재고가 부족합니다.")

    # 소모품 재고 확인
    for consumable_id in consumable_ids_list:
        consumable = read_consumable_by_id(db, consumable_id)
        if consumable is None:
            details.append(f"소모품 '{consumable_id}'가 존재하지 않습니다.")
        elif consumable.quantity <= 0:
            details.append(f"소모품 '{consumable.name}'의 재고가 부족합니다.")

    # 컵 재고 확인
    cup = read_cup(db)
    if cup is None:
        details.append("컵이 존재하지 않습니다.")
    elif cup.quantity <= 0:
        details.append("컵 재고가 부족합니다.")

    if details:
        raise HTTPException(status_code=409, detail=details)
    else:
        # 재고가 충분하면 주문 생성
        order = create_order(db, ice_cream_id, topping_ids_list, consumable_ids_list)
        return order


async def add_order_by_kiosk(json_data: dict, db: Session):
    """
    키오스크 주문 추가 함수
    Args:
        json_data: 요청 JSON 데이터
        db: 데이터베이스 세션
    Returns:
        order: 주문 정보
    """
    detail_body = json_data.get("OR", {})
    icecream = detail_body.get("icecream")
    topping = detail_body.get("topping")

    if not icecream:
        raise HTTPException(status_code=400, detail=["아이스크림 선택은 필수입니다."])

    details = []

    # 아이스크림 존재 or 재고 여부 확인
    ice_cream_id = get_item_id_by_name(db, "ice_cream", icecream)
    if ice_cream_id is None:
        details.append(f"아이스크림 '{icecream}' 부재")
    else:
        ice_cream = read_ice_cream_by_id(db, ice_cream_id)
        if ice_cream.quantity <= 0:
            details.append(f"아이스크림 '{icecream}' 재고 부족")

    # 토핑 존재 or 재고 여부 확인
    topping_ids_list = []
    if topping:
        for name in topping.split(","):
            topping_id = get_item_id_by_name(db, "topping", name.strip())
            if topping_id is None:
                details.append(f"토핑 '{name.strip()}' 부재")
            else:
                topping_item = read_topping_by_id(db, topping_id)
                if topping_item.quantity <= 0:
                    details.append(f"토핑 '{name.strip()}' 재고 부족")
                topping_ids_list.append(topping_id)

    # 컵 재고 여부 확인
    cup = read_cup(db)
    if cup.quantity <= 0:
        details.append("컵 재고가 부족합니다.")

    if details:
        raise HTTPException(status_code=409, detail=details)

    order = create_order(db, ice_cream_id, topping_ids_list, consumable_ids=[])

    response_content = {
        "orderId": order.id,
    }
    return response_content


def get_all_histories(db: Session):
    """
    모든 주문 정보 조회 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        orders: 모든 주문 정보 리스트
    """
    orders = read_all_orders(db)
    return orders


def edit_order_time(db: Session, order_id: int, new_order_time: datetime):
    """
    주문 시간 수정 함수
    Args:
        db: 데이터베이스 세션
        order_id: 주문 ID
        new_order_time: 새로운 주문 시간
    Returns:
        order: 수정된 주문 정보
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=404, detail=f"주문번호 {order_id}번이 존재하지 않습니다."
        )
    order.order_time = new_order_time
    db.commit()
    db.refresh(order)
    return order
