from sqlalchemy.orm import Session
from models.models import Topping


def create_topping(db: Session, name: str, price: int, quantity: int):
    topping = Topping(name=name, price=price, quantity=quantity)
    db.add(topping)
    db.commit()
    db.refresh(topping)
    return topping


def read_topping_by_id(db: Session, topping_id: float):
    return db.query(Topping).filter(Topping.id == topping_id).first()


def read_all_toppings(db: Session):
    return db.query(Topping).all()


def update_topping(
    db: Session,
    topping_id: float,
    name: str = None,
    price: int = None,
    quantity: int = None,
):
    topping = db.query(Topping).filter(Topping.id == topping_id).first()
    if topping is None:
        return None

    if name is not None:
        topping.name = name
    if price is not None:
        topping.price = price
    if quantity is not None:
        topping.quantity = quantity

    db.commit()
    db.refresh(topping)
    return topping


def delete_topping_by_id(db: Session, topping_id: float):
    topping = db.query(Topping).filter(Topping.id == topping_id).first()
    if topping:
        db.delete(topping)
        db.commit()
    return topping


def delete_all_toppings(db: Session):
    toppings = db.query(Topping).all()
    for topping in toppings:
        db.delete(topping)
    db.commit()
    return toppings
