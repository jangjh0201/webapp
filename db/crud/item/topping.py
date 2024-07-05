from sqlalchemy.orm import Session
from ...models.topping import Topping

def create_topping(db: Session, name: str):
    existing_item = db.query(Topping).filter(Topping.name == name).first()
    if existing_item:
        print("이미 존재하는 토핑입니다.") 
        return existing_item

    db_item = Topping(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_topping(db: Session, topping_id: int):
    return db.query(Topping).filter(Topping.id == topping_id).first()

def get_all_toppings(db: Session):
    return db.query(Topping).all()