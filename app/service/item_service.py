from sqlalchemy.orm import Session
from models.models import IceCream, Topping, Consumable
from database.crud.ice_cream import create_ice_cream, read_all_ice_creams
from database.crud.topping import create_topping, read_all_toppings
from database.crud.consumable import create_consumable, read_all_consumables

def add_item(
    item_type: str, item_name: str, item_price: int, item_quantity: int, db: Session
):
    """
    아이템 추가 함수
    Args:
        item_type: 아이템 타입
        item_name: 아이템 이름
        item_price: 아이템 가격
        item_quantity: 아이템 수량
        db: 데이터베이스 세션
    Returns:
        성공 여부
    """
    if item_type == "ice_cream":
        create_ice_cream(db, item_name, item_price, item_quantity)
    elif item_type == "topping":
        create_topping(db, item_name, item_price, item_quantity)
    elif item_type == "consumable":
        create_consumable(db, item_name, item_price, item_quantity)
    return True

def get_all_items(db: Session):
    """
    모든 아이템 정보 조회 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        ice_creams: 모든 아이스크림 정보 리스트
        toppings: 모든 토핑 정보 리스트
        consumables: 모든 소모품 정보 리스트
    """
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    return ice_creams, toppings, consumables

def get_all_inventories(db: Session):
    """
    모든 아이템 수량 정보 조회 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        ice_creams: 모든 아이스크림 수량 정보 딕셔너리
        toppings: 모든 토핑 수량 정보 딕셔너리
        consumables: 모든 소모품 수량 정보 딕셔너리
    """
    ice_creams = {ic.name: ic.quantity for ic in read_all_ice_creams(db)}
    toppings = {tp.name: tp.quantity for tp in read_all_toppings(db)}
    consumables = {cs.name: cs.quantity for cs in read_all_consumables(db)}
    return ice_creams, toppings, consumables

def remove_item(item_type: str, item_id: int, db: Session):
    """
    아이템 삭제 함수
    Args:
        item_type: 아이템 타입
        item_id: 아이템 ID
        db: 데이터베이스 세션
    Returns:
        성공 여부
    """
    if item_type == "ice_cream":
        db.query(IceCream).filter(IceCream.id == item_id).delete()
    elif item_type == "topping":
        db.query(Topping).filter(Topping.id == item_id).delete()
    elif item_type == "consumable":
        db.query(Consumable).filter(Consumable.id == item_id).delete()
    db.commit()
    return True


