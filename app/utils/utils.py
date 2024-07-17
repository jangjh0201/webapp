from typing import Optional
from models.models import IceCream, Topping, Consumable
from sqlalchemy.orm import Session


def get_item_id_by_name(db: Session, item_type: str, item_name: str) -> Optional[int]:
    if item_type == "ice_cream":
        item = db.query(IceCream).filter(IceCream.name == item_name).first()
    elif item_type == "topping":
        item = db.query(Topping).filter(Topping.name == item_name).first()
    elif item_type == "consumable":
        item = db.query(Consumable).filter(Consumable.name == item_name).first()
    else:
        return None

    return item.id if item else None
