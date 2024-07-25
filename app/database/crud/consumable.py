from sqlalchemy.orm import Session
from models.models import Consumable


def create_consumable(db: Session, name: str, price: int, quantity: int):
    consumable = Consumable(name=name, price=price, quantity=quantity)
    db.add(consumable)
    db.commit()
    db.refresh(consumable)
    return consumable


def read_consumable_by_id(db: Session, consumable_id: float):
    return db.query(Consumable).filter(Consumable.id == consumable_id).first()


def read_all_consumables(db: Session):
    return db.query(Consumable).all()


def read_cup(db: Session):
    return db.query(Consumable).filter(Consumable.name == "cup").first()


def update_consumable(
    db: Session,
    consumable_id: float,
    name: str = None,
    price: int = None,
    quantity: int = None,
):
    consumable = db.query(Consumable).filter(Consumable.id == consumable_id).first()
    if consumable is None:
        return None

    if name is not None:
        consumable.name = name
    if price is not None:
        consumable.price = price
    if quantity is not None:
        consumable.quantity = quantity

    db.commit()
    db.refresh(consumable)
    return consumable


def delete_consumable_by_id(db: Session, consumable_id: float):
    consumable = db.query(Consumable).filter(Consumable.id == consumable_id).first()
    if consumable:
        db.delete(consumable)
        db.commit()
    return consumable


def delete_all_consumables(db: Session):
    consumables = db.query(Consumable).all()
    for consumable in consumables:
        db.delete(consumable)
    db.commit()
    return consumables
