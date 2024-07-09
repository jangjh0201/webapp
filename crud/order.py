from sqlalchemy.orm import Session
from models import Order, IceCream, Topping, OtherItem, Inventory


# ice_cream, topping, other_item의 이름들을 받아 객체들을 조회하여 주문을 생성합니다.
def create_order(
    db: Session, ice_cream_name: str, topping_names: list, other_item_names: list
):
    ice_cream = db.query(IceCream).filter(IceCream.name == ice_cream_name).first()
    if not ice_cream:
        return None

    toppings = []
    for name in topping_names:
        topping = db.query(Topping).filter(Topping.name == name).first()
        if topping:
            toppings.append(topping.id)

    other_items = []
    for name in other_item_names:
        other_item = db.query(OtherItem).filter(OtherItem.name == name).first()
        if other_item:
            other_items.append(other_item.id)

    return create_order(db, ice_cream.id, toppings, other_items)


# ID로 특정 주문을 조회합니다.
def read_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


# 모든 주문을 조회합니다.
def read_all_orders(db: Session):
    return db.query(Order).all()


# ID로 특정 주문을 삭제합니다.
def delete_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order


# 모든 주문을 삭제합니다.
def delete_all_orders(db: Session):
    orders = db.query(Order).all()
    for order in orders:
        db.delete(order)
    db.commit()
    return orders
