from sqlalchemy.orm import Session
from models.models import Order, IceCream, Topping, Consumable


def create_order(
    db: Session, ice_cream_id: int, topping_ids: list, consumable_ids: list
):
    order = Order(ice_cream_id=ice_cream_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
    if ice_cream:
        ice_cream.quantity -= 1
        db.commit()

    for topping_id in topping_ids:
        topping = db.query(Topping).filter(Topping.id == topping_id).first()
        if topping:
            topping.quantity -= 1
            order.toppings.append(topping)
            db.commit()

    for consumable_id in consumable_ids:
        consumable = db.query(Consumable).filter(Consumable.id == consumable_id).first()
        if consumable:
            consumable.quantity -= 1
            order.consumables.append(consumable)
            db.commit()

    db.commit()
    return order


def get_all_orders(db: Session):
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int):
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
        # 기존 주문의 재고 복구
        old_ice_cream = (
            db.query(IceCream).filter(IceCream.id == order.ice_cream_id).first()
        )
        if old_ice_cream:
            old_ice_cream.quantity += 1

        for topping in order.toppings:
            old_topping = db.query(Topping).filter(Topping.id == topping.id).first()
            if old_topping:
                old_topping.quantity += 1

        for consumable in order.consumables:
            old_consumable = (
                db.query(Consumable).filter(Consumable.id == consumable.id).first()
            )
            if old_consumable:
                old_consumable.quantity += 1

        # 새로운 주문의 재고 차감
        order.ice_cream_id = ice_cream_id
        new_ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
        if new_ice_cream:
            new_ice_cream.quantity -= 1

        order.toppings = []
        for topping_id in topping_ids:
            new_topping = db.query(Topping).filter(Topping.id == topping_id).first()
            if new_topping:
                new_topping.quantity -= 1
                order.toppings.append(new_topping)

        order.consumables = []
        for consumable_id in consumable_ids:
            new_consumable = (
                db.query(Consumable).filter(Consumable.id == consumable_id).first()
            )
            if new_consumable:
                new_consumable.quantity -= 1
                order.consumables.append(new_consumable)

        db.commit()
    return order


def delete_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        # 기존 주문의 재고 복구
        old_ice_cream = (
            db.query(IceCream).filter(IceCream.id == order.ice_cream_id).first()
        )
        if old_ice_cream:
            old_ice_cream.quantity += 1

        for topping in order.toppings:
            old_topping = db.query(Topping).filter(Topping.id == topping.id).first()
            if old_topping:
                old_topping.quantity += 1

        for consumable in order.consumables:
            old_consumable = (
                db.query(Consumable).filter(Consumable.id == consumable.id).first()
            )
            if old_consumable:
                old_consumable.quantity += 1

        db.delete(order)
        db.commit()


def delete_all_orders(db: Session):
    orders = db.query(Order).all()
    for order in orders:
        # 기존 주문의 재고 복구
        old_ice_cream = (
            db.query(IceCream).filter(IceCream.id == order.ice_cream_id).first()
        )
        if old_ice_cream:
            old_ice_cream.quantity += 1

        for topping in order.toppings:
            old_topping = db.query(Topping).filter(Topping.id == topping.id).first()
            if old_topping:
                old_topping.quantity += 1

        for consumable in order.consumables:
            old_consumable = (
                db.query(Consumable).filter(Consumable.id == consumable.id).first()
            )
            if old_consumable:
                old_consumable.quantity += 1

    db.query(Order).delete()
    db.commit()
