from sqlalchemy.orm import Session
from ...models.item.other import Other

def create_other(db: Session, name: str):
    existing_item = db.query(Other).filter(Other.name == name).first()
    if existing_item:
        print("이미 존재하는 기타 항목입니다.")
        return existing_item

    db_item = Other(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_other(db: Session, other_id: int):
    return db.query(Other).filter(Other.id == other_id).first()

def get_all_others(db: Session):
    return db.query(Other).all()
