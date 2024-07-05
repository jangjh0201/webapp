from sqlalchemy.orm import Session
from .inventory import Inventory

def create_inventory_item(db: Session, item_id: int, item_type_id: int, quantity: int):
    existing_item = db.query(Inventory).filter(Inventory.item_id == item_id, Inventory.item_type_id == item_type_id).first()
    if existing_item:
        print("이미 존재하는 재고 항목입니다.")
        return existing_item

    db_item = Inventory(item_id=item_id, item_type_id=item_type_id, quantity=quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_inventory_item(db: Session, item_id: int, item_type_id: int):
    return db.query(Inventory).filter(Inventory.item_id == item_id, Inventory.item_type_id == item_type_id).first()

def update_inventory(db: Session, item_id: int, item_type_id: int, quantity: int):
    inventory_item = get_inventory_item(db, item_id, item_type_id)
    if inventory_item:
        inventory_item.quantity = quantity
        db.commit()
        db.refresh(inventory_item)
        return inventory_item
    return None

def reduce_inventory(db: Session, item_id: int, item_type_id: int, quantity: int):
    inventory_item = get_inventory_item(db, item_id, item_type_id)
    if inventory_item and inventory_item.quantity >= quantity:
        inventory_item.quantity -= quantity
        db.commit()
        db.refresh(inventory_item)
        return inventory_item
    return None

def get_all_inventory(db: Session):
    return db.query(Inventory).all()
