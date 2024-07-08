from sqlalchemy.orm import Session
from models.models import OtherItem


def create_other_item(db: Session, name: str, price: int):
    if db.query(OtherItem).filter(OtherItem.name == name).first():
        print(f"{name}은(는) 이미 등록된 품목입니다.")
        return None
    db_other_item = OtherItem(name=name, price=price)
    db.add(db_other_item)
    db.commit()
    db.refresh(db_other_item)
    return db_other_item


def get_all_other_items(db: Session):
    return db.query(OtherItem).all()


def delete_other_item_by_name(db: Session, name: str):
    db_other_item = db.query(OtherItem).filter(OtherItem.name == name).first()
    if db_other_item:
        db.delete(db_other_item)
        db.commit()
        print(f"{name} 을 삭제했습니다.")
    else:
        print(f"{name} 이 존재하지 않습니다.")


def delete_all_other_items(db: Session):
    db.query(OtherItem).delete()
    db.commit()
    print("모든 기타 품목을 삭제했습니다.")
