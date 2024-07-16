from sqlalchemy.orm import Session
from models.models import Order, IceCream, Topping, Consumable
from fastapi import HTTPException


def create_order(
    db: Session, ice_cream_id: int, topping_ids: list, consumable_ids: list
):
    ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
    if ice_cream.quantity <= 0:
        raise HTTPException(status_code=400, detail="아이스크림 재고가 부족합니다.")
    ice_cream.quantity -= 1

    order = Order(ice_cream_id=ice_cream_id)

    for topping_id in topping_ids:
        topping = db.query(Topping).filter(Topping.id == topping_id).first()
        if topping.quantity <= 0:
            raise HTTPException(status_code=400, detail="토핑 재고가 부족합니다.")
        topping.quantity -= 1
        order.toppings.append(topping)

    for consumable_id in consumable_ids:
        consumable = db.query(Consumable).filter(Consumable.id == consumable_id).first()
        if consumable.quantity <= 0:
            raise HTTPException(status_code=400, detail="소모품 재고가 부족합니다.")
        consumable.quantity -= 1
        order.consumables.append(consumable)

    # 컵 재고 차감
    cup = db.query(Consumable).filter(Consumable.name == "cup").first()
    if cup.quantity <= 0:
        raise HTTPException(status_code=400, detail="컵 재고가 부족합니다.")
    cup.quantity -= 1

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def read_all_orders(db: Session):
    return db.query(Order).all()


def read_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def update_order(
    db: Session,
    order_id: int,
    ice_cream_id: int,
    topping_ids: list,
    consumable_ids: list,
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.ice_cream_id = ice_cream_id
        order.toppings = []
        for topping_id in topping_ids:
            topping = db.query(Topping).filter(Topping.id == topping_id).first()
            order.toppings.append(topping)
        order.consumables = []
        for consumable_id in consumable_ids:
            consumable = (
                db.query(Consumable).filter(Consumable.id == consumable_id).first()
            )
            order.consumables.append(consumable)
        db.commit()
        db.refresh(order)


def delete_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()


def delete_all_orders(db: Session):
    db.query(Order).delete()
    db.commit()
