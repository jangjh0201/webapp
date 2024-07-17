from fastapi import Request, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from models.models import Consumable, IceCream, Topping
from database.crud.ice_cream import (
    create_ice_cream,
    read_all_ice_creams,
)
from database.crud.topping import (
    create_topping,
    read_all_toppings,
)
from database.crud.consumable import (
    create_consumable,
    read_all_consumables,
)


def show_item(request: Request, db: Session, templates: Jinja2Templates):
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    return templates.TemplateResponse(
        "item.html",
        {
            "request": request,
            "ice_creams": ice_creams,
            "toppings": toppings,
            "consumables": consumables,
        },
    )


def add_item(
    request: Request,
    item_type: str,
    item_name: str,
    item_price: int,
    item_quantity: int,
    db: Session,
    templates: Jinja2Templates,
):
    if item_type == "ice_cream":
        create_ice_cream(db, item_name, item_price, item_quantity)
    elif item_type == "topping":
        create_topping(db, item_name, item_price, item_quantity)
    elif item_type == "consumable":
        create_consumable(db, item_name, item_price, item_quantity)
    return show_item(request, db, templates)


def remove_item(item_type: str, item_id: int, db: Session):
    if item_type == "ice_cream":
        db.query(IceCream).filter(IceCream.id == item_id).delete()
    elif item_type == "topping":
        db.query(Topping).filter(Topping.id == item_id).delete()
    elif item_type == "consumable":
        db.query(Consumable).filter(Consumable.id == item_id).delete()
    db.commit()
    return {"success": True}


def show_inventory(request: Request, db: Session, templates: Jinja2Templates):
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    inventory_data = {
        "ice_cream": {ic.name: ic.quantity for ic in ice_creams},
        "topping": {tp.name: tp.quantity for tp in toppings},
        "consumable": {cs.name: cs.quantity for cs in consumables},
    }
    return templates.TemplateResponse(
        "stock.html", {"request": request, "inventory_data": inventory_data}
    )
