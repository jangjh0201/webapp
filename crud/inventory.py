# inventory.py

from sqlalchemy.orm import Session
from models.models import IceCream, Inventory, OtherItem, Topping


def create_inventory(db: Session, item_type: str, item_id: int, quantity: int):
    if quantity < 0:
        print("수량은 음수일 수 없습니다.")
        return None

    inventory = (
        db.query(Inventory)
        .filter(Inventory.item_type == item_type, Inventory.item_id == item_id)
        .first()
    )
    if inventory:
        inventory.quantity += quantity
        db.commit()
        db.refresh(inventory)
        return inventory
    else:
        db_inventory = Inventory(
            item_type=item_type, item_id=item_id, quantity=quantity
        )
        db.add(db_inventory)
        db.commit()
        db.refresh(db_inventory)
        return db_inventory


def get_all_inventory(db: Session):
    return db.query(Inventory).all()


def get_inventory_by_item(db: Session, item_name: str):
    ice_cream_inventory = (
        db.query(Inventory).join(IceCream).filter(IceCream.name == item_name).all()
    )
    topping_inventory = (
        db.query(Inventory).join(Topping).filter(Topping.name == item_name).all()
    )
    other_item_inventory = (
        db.query(Inventory).join(OtherItem).filter(OtherItem.name == item_name).all()
    )
    return ice_cream_inventory + topping_inventory + other_item_inventory


def get_inventory_below_quantity(db: Session, quantity: int):
    return db.query(Inventory).filter(Inventory.quantity <= quantity).all()


def delete_inventory_by_name(db: Session, item_name: str):
    ice_cream_inventory = (
        db.query(Inventory).join(IceCream).filter(IceCream.name == item_name).all()
    )
    topping_inventory = (
        db.query(Inventory).join(Topping).filter(Topping.name == item_name).all()
    )
    other_item_inventory = (
        db.query(Inventory).join(OtherItem).filter(OtherItem.name == item_name).all()
    )

    if ice_cream_inventory:
        for item in ice_cream_inventory:
            db.delete(item)
        db.commit()
        print(f"{item_name} 아이스크림 재고를 삭제했습니다.")
    elif topping_inventory:
        for item in topping_inventory:
            db.delete(item)
        db.commit()
        print(f"{item_name} 토핑 재고를 삭제했습니다.")
    elif other_item_inventory:
        for item in other_item_inventory:
            db.delete(item)
        db.commit()
        print(f"{item_name} 기타 품목 재고를 삭제했습니다.")
    else:
        print(f"{item_name} 재고가 존재하지 않습니다.")


def delete_all_inventory(db: Session):
    db.query(Inventory).delete()
    db.commit()
    print("모든 재고를 삭제했습니다.")
