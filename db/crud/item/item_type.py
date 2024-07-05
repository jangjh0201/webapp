from sqlalchemy.orm import Session
from ...models.item.item_type import ItemType

def create_item_type(db: Session, name: str):
    existing_item = db.query(ItemType).filter(ItemType.name == name).first()
    if existing_item:
        print("이미 존재하는 아이템 타입입니다.")
        return existing_item

    db_item = ItemType(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_type(db: Session, name: str):
    return db.query(ItemType).filter(ItemType.name == name).first()

def get_all_item_types(db: Session):
    return db.query(ItemType).all()
