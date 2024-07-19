from sqlalchemy.orm import Session
from models.models import IceCream, Topping, Consumable
from database.crud.ice_cream import create_ice_cream, read_all_ice_creams
from database.crud.topping import create_topping, read_all_toppings
from database.crud.consumable import create_consumable, read_all_consumables


def show_item(db: Session):
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    return ice_creams, toppings, consumables


def add_item(
    item_type: str, item_name: str, item_price: int, item_quantity: int, db: Session
):
    if item_type == "ice_cream":
        create_ice_cream(db, item_name, item_price, item_quantity)
    elif item_type == "topping":
        create_topping(db, item_name, item_price, item_quantity)
    elif item_type == "consumable":
        create_consumable(db, item_name, item_price, item_quantity)
    return True


def remove_item(item_type: str, item_id: int, db: Session):
    if item_type == "ice_cream":
        db.query(IceCream).filter(IceCream.id == item_id).delete()
    elif item_type == "topping":
        db.query(Topping).filter(Topping.id == item_id).delete()
    elif item_type == "consumable":
        db.query(Consumable).filter(Consumable.id == item_id).delete()
    db.commit()
    return True


def show_inventory(db: Session):
    ice_creams = {ic.name: ic.quantity for ic in read_all_ice_creams(db)}
    toppings = {tp.name: tp.quantity for tp in read_all_toppings(db)}
    consumables = {cs.name: cs.quantity for cs in read_all_consumables(db)}
    return ice_creams, toppings, consumables
