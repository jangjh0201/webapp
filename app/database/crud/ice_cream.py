from sqlalchemy.orm import Session
from models.models import IceCream


def create_ice_cream(db: Session, name: str, price: int, quantity: int):
    ice_cream = IceCream(name=name, price=price, quantity=quantity)
    db.add(ice_cream)
    db.commit()
    db.refresh(ice_cream)
    return ice_cream


def read_ice_cream_by_id(db: Session, ice_cream_id: float):
    return db.query(IceCream).filter(IceCream.id == ice_cream_id).first()


def read_all_ice_creams(db: Session):
    return db.query(IceCream).all()


def update_ice_cream(
    db: Session,
    ice_cream_id: float,
    name: str = None,
    price: int = None,
    quantity: int = None,
):
    ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
    if ice_cream is None:
        return None

    if name is not None:
        ice_cream.name = name
    if price is not None:
        ice_cream.price = price
    if quantity is not None:
        ice_cream.quantity = quantity

    db.commit()
    db.refresh(ice_cream)
    return ice_cream


def delete_ice_cream_by_id(db: Session, ice_cream_id: float):
    ice_cream = db.query(IceCream).filter(IceCream.id == ice_cream_id).first()
    if ice_cream:
        db.delete(ice_cream)
        db.commit()
    return ice_cream


def delete_all_ice_creams(db: Session):
    ice_creams = db.query(IceCream).all()
    for ice_cream in ice_creams:
        db.delete(ice_cream)
    db.commit()
    return ice_creams
