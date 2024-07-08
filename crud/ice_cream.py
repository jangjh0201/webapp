# ice_cream.py

from sqlalchemy.orm import Session
from models.models import IceCream


def create_ice_cream(db: Session, name: str, price: int):
    if db.query(IceCream).filter(IceCream.name == name).first():
        print(f"{name}은(는) 이미 등록된 품목입니다.")
        return None
    db_ice_cream = IceCream(name=name, price=price)
    db.add(db_ice_cream)
    db.commit()
    db.refresh(db_ice_cream)
    return db_ice_cream


def get_all_ice_creams(db: Session):
    return db.query(IceCream).all()


def delete_ice_cream_by_name(db: Session, name: str):
    db_ice_cream = db.query(IceCream).filter(IceCream.name == name).first()
    if db_ice_cream:
        db.delete(db_ice_cream)
        db.commit()
        print(f"{name} 아이스크림을 삭제했습니다.")
    else:
        print(f"{name} 아이스크림이 존재하지 않습니다.")


def delete_all_ice_creams(db: Session):
    db.query(IceCream).delete()
    db.commit()
    print("모든 아이스크림을 삭제했습니다.")
