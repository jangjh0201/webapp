from sqlalchemy.orm import Session
from models.models import Topping


def create_topping(db: Session, name: str, price: int):
    if db.query(Topping).filter(Topping.name == name).first():
        print(f"{name}은(는) 이미 등록된 품목입니다.")
        return None
    db_topping = Topping(name=name, price=price)
    db.add(db_topping)
    db.commit()
    db.refresh(db_topping)
    return db_topping


def get_all_toppings(db: Session):
    return db.query(Topping).all()


def delete_topping_by_name(db: Session, name: str):
    db_topping = db.query(Topping).filter(Topping.name == name).first()
    if db_topping:
        db.delete(db_topping)
        db.commit()
        print(f"{name} 토핑을 삭제했습니다.")
    else:
        print(f"{name} 토핑이 존재하지 않습니다.")


def delete_all_toppings(db: Session):
    db.query(Topping).delete()
    db.commit()
    print("모든 토핑을 삭제했습니다.")
