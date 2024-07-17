from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database.crud.ice_cream import read_all_ice_creams
from database.crud.topping import read_all_toppings
from database.crud.consumable import read_all_consumables
from database.crud.order import (
    create_order,
    read_all_orders,
)
from utils.utils import get_item_id_by_name


def show_order(request: Request, db: Session, templates: Jinja2Templates):
    ice_creams = read_all_ice_creams(db)
    toppings = read_all_toppings(db)
    consumables = read_all_consumables(db)
    consumables = [c for c in consumables if c.name != "cup"]
    return templates.TemplateResponse(
        "order.html",
        {
            "request": request,
            "ice_creams": ice_creams,
            "toppings": toppings,
            "consumables": consumables,
        },
    )


def add_order(
    request: Request,
    ice_cream_id: int,
    topping_ids: str,
    consumable_ids: str,
    db: Session,
    templates: Jinja2Templates,
):
    topping_ids_list = (
        [int(id) for id in topping_ids.split(",") if id] if topping_ids else []
    )
    consumable_ids_list = (
        [int(id) for id in consumable_ids.split(",") if id] if consumable_ids else []
    )
    create_order(db, ice_cream_id, topping_ids_list, consumable_ids_list)
    return templates.TemplateResponse("index.html", {"request": request})


async def add_order_by_kiosk(request: Request, db: Session):
    try:
        body = await request.json()
        order_details = body.get("OR", {})
        icecream = order_details.get("icecream")
        topping = order_details.get("topping")

        if not icecream:
            raise HTTPException(status_code=400, detail="Field 'icecream' is required")

        print(f"Received order: icecream={icecream}, topping={topping}")

        # 아이템 이름을 ID로 변환
        ice_cream_id = get_item_id_by_name(db, "ice_cream", icecream)
        if ice_cream_id is None:
            raise HTTPException(status_code=400, detail="Invalid ice cream name")

        topping_ids_list = []
        if topping:
            for name in topping.split(","):
                topping_id = get_item_id_by_name(db, "topping", name.strip())
                if topping_id:
                    topping_ids_list.append(topping_id)

        order = create_order(db, ice_cream_id, topping_ids_list, consumable_ids=[])

        return {
            "HTTPstatus": "201 Created",
            "orderId": order.id,
            "icecream": icecream,
            "topping": topping,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def show_history(request: Request, db: Session, templates: Jinja2Templates):
    orders = read_all_orders(db)
    return templates.TemplateResponse(
        "history.html", {"request": request, "orders": orders}
    )
