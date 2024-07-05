from sqlalchemy.orm import Session
from ...models.item.ice_cream import IceCream

def create_ice_cream(db: Session, name: str):
    existing_item = db.query(IceCream).filter(IceCream.name == name).first()
    if existing_item:
        print("이미 존재하는 아이스크림입니다.")
        return existing_item

    db_item = IceCream(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_ice_cream(db: Session, ice_cream_id: int):
    return db.query(IceCream).filter(IceCream.id == ice_cream_id).first()

def get_all_ice_creams(db: Session):
    return db.query(IceCream).all()
