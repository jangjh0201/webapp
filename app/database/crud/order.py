from datetime import datetime
from sqlalchemy.orm import Session
from models.models import Order, IceCream, Topping, Consumable


def create_order(
    db: Session, ice_cream_id: int, topping_ids: list, consumable_ids: list
):
    ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
    ice_cream.quantity -= 1

    order = Order(ice_cream_id=ice_cream_id)

    for topping_id in topping_ids:
        topping = db.query(Topping).filter(Topping.id == topping_id).first()
        topping.quantity -= 1
        order.toppings.append(topping)

    for consumable_id in consumable_ids:
        consumable = db.query(Consumable).filter(Consumable.id == consumable_id).first()
        consumable.quantity -= 1
        order.consumables.append(consumable)

    # 컵 재고 차감
    cup = db.query(Consumable).filter(Consumable.name == "cup").first()
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


def update_order_time(db: Session, order_id: int, new_order_time: datetime):
    order = read_order_by_id(db, order_id)
    order.order_time = new_order_time
    db.commit()
    db.refresh(order)
    return order


def delete_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()


def delete_all_orders(db: Session):
    db.query(Order).delete()
    db.commit()
