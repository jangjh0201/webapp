import sys
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.utils import get_item_id_by_name
from models.models import Consumable, IceCream, Topping, Order
from database.database import initialize_tables, SessionLocal
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
from database.crud.order import (
    create_order,
    read_all_orders,
)

app = FastAPI()

templates = Jinja2Templates(directory="app/resource/templates")
app.mount("/static", StaticFiles(directory="app/resource/static"), name="static")


# 테이블 및 데이터베이스 설정
initialize_tables()

db = SessionLocal()


def get_db():
    try:
        yield db
    finally:
        db.close()


# 아이스크림 생성 및 조회 테스트
mint = create_ice_cream(db, "mint", 2500, 100)
chocolate = create_ice_cream(db, "choco", 2500, 100)
strawberry = create_ice_cream(db, "strawberry", 2500, 100)

# 토핑 생성 및 조회 테스트
choco_ball = create_topping(db, "chocoball", 500, 100)
cereal = create_topping(db, "cereal", 700, 100)
oreo = create_topping(db, "oreo", 700, 100)

# 소모품 생성 및 조회 테스트
cup = create_consumable(db, "cup", 0, 100)


@app.get("/")
def show_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/item")
def show_item(request: Request, db: Session = Depends(get_db)):
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


@app.post("/item")
def add_item(
    request: Request,
    item_type: str = Form(...),
    item_name: str = Form(...),
    item_price: int = Form(...),
    item_quantity: int = Form(...),
    db: Session = Depends(get_db),
):
    if item_type == "ice_cream":
        create_ice_cream(db, item_name, item_price, item_quantity)
    elif item_type == "topping":
        create_topping(db, item_name, item_price, item_quantity)
    elif item_type == "consumable":
        create_consumable(db, item_name, item_price, item_quantity)
    return show_item(request, db)


@app.delete("/item/{item_type}/{item_id}")
def remove_item(item_type: str, item_id: int, db: Session = Depends(get_db)):
    if item_type == "ice_cream":
        db.query(IceCream).filter(IceCream.id == item_id).delete()
    elif item_type == "topping":
        db.query(Topping).filter(Topping.id == item_id).delete()
    elif item_type == "consumable":
        db.query(Consumable).filter(Consumable.id == item_id).delete()
    db.commit()
    return {"success": True}


@app.get("/order")
def show_order(request: Request, db: Session = Depends(get_db)):
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


@app.post("/order")
def add_order(
    request: Request,
    ice_cream_id: int = Form(...),
    topping_ids: str = Form(None),
    consumable_ids: str = Form(None),
    db: Session = Depends(get_db),
):
    topping_ids_list = (
        [int(id) for id in topping_ids.split(",") if id] if topping_ids else []
    )
    consumable_ids_list = (
        [int(id) for id in consumable_ids.split(",") if id] if consumable_ids else []
    )
    create_order(db, ice_cream_id, topping_ids_list, consumable_ids_list)
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/kiosk")
async def add_order_by_kiosk(request: Request, db: Session = Depends(get_db)):
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


@app.get("/stock")
def show_inventory(request: Request, db: Session = Depends(get_db)):
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


@app.get("/history")
def show_history(request: Request, db: Session = Depends(get_db)):
    orders = read_all_orders(db)
    return templates.TemplateResponse(
        "history.html", {"request": request, "orders": orders}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
