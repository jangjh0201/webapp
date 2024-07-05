from sqlalchemy.orm import Session
from .item.ice_cream import get_ice_cream
from .item.topping import get_topping

from .order import Order
from .inventory import reduce_inventory

def create_order(db: Session, ice_cream_id: int, topping_id: int):
    ice_cream = get_ice_cream(db, ice_cream_id)
    topping = get_topping(db, topping_id)
    
    if ice_cream and topping:
        order = Order(ice_cream_id=ice_cream_id, topping_id=topping_id)
        
        if reduce_inventory(db, 'ice_cream', ice_cream_id, 1) and reduce_inventory(db, 'topping', topping_id, 1):
            db.add(order)
            db.commit()
            db.refresh(order)
            return order
        else:
            print("재고 부족으로 주문을 완료할 수 없습니다.")
    return None

def get_all_orders(db: Session):
    return db.query(Order).all()