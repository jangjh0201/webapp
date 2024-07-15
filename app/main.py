import sys
import os
from typing import Optional
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.utils import get_item_id_by_name
from models.models import Consumable, IceCream, Topping
from database.database import initialize_tables, SessionLocal
from crud.ice_cream import create_ice_cream, get_all_ice_creams
from crud.topping import create_topping, get_all_toppings
from crud.consumable import create_consumable, get_all_consumables
from crud.order import create_order, get_all_orders

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 테이블 및 데이터베이스 설정
initialize_tables()

# 테스트
db = SessionLocal()
# 아이스크림 생성 및 조회 테스트
vanilla = create_ice_cream(db, "바닐라", 2500, 100)
chocolate = create_ice_cream(db, "초콜릿", 2500, 100)
strawberry = create_ice_cream(db, "딸기", 2500, 100)

# 토핑 생성 및 조회 테스트
choco_ball = create_topping(db, "초코볼", 500, 100)
cereal = create_topping(db, "시리얼", 700, 100)
oreo = create_topping(db, "오레오", 700, 100)

# 소모품 생성 및 조회 테스트
cup = create_consumable(db, "컵", 200, 100)
spoon = create_consumable(db, "스푼", 100, 100)
holder = create_consumable(db, "홀더", 300, 100)


@app.get("/")
def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/item")
def get_add_item_page(request: Request, db: Session = Depends(get_db)):
    ice_creams = get_all_ice_creams(db)
    toppings = get_all_toppings(db)
    consumables = get_all_consumables(db)
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
def create_new_item(
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
    return get_add_item_page(request, db)


@app.delete("/item/{item_type}/{item_id}")
def delete_item(item_type: str, item_id: int, db: Session = Depends(get_db)):
    if item_type == "ice_cream":
        db.query(IceCream).filter(IceCream.id == item_id).delete()
    elif item_type == "topping":
        db.query(Topping).filter(Topping.id == item_id).delete()
    elif item_type == "consumable":
        db.query(Consumable).filter(Consumable.id == item_id).delete()
    db.commit()
    return {"success": True}


@app.get("/order")
def get_order_page(request: Request, db: Session = Depends(get_db)):
    ice_creams = get_all_ice_creams(db)
    toppings = get_all_toppings(db)
    consumables = get_all_consumables(db)
    consumables = [c for c in consumables if c.name != "컵"]
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
def create_new_order(
    request: Request,
    ice_cream_name: str = Form(...),
    topping_names: Optional[str] = Form(None),  # 콤마로 구분된 토핑 이름 목록
    consumable_names: Optional[str] = Form(None),  # 콤마로 구분된 소모품 이름 목록
    db: Session = Depends(get_db),
):
    print(
        f"Received order: ice_cream_name={ice_cream_name}, topping_names={topping_names}, consumable_names={consumable_names}"
    )

    # 아이템 이름을 ID로 변환
    ice_cream_id = get_item_id_by_name(db, "ice_cream", ice_cream_name)
    if ice_cream_id is None:
        raise HTTPException(status_code=400, detail="Invalid ice cream name")

    topping_ids_list = []
    if topping_names:
        for name in topping_names.split(","):
            topping_id = get_item_id_by_name(db, "topping", name.strip())
            if topping_id:
                topping_ids_list.append(topping_id)

    consumable_ids_list = []
    if consumable_names:
        for name in consumable_names.split(","):
            consumable_id = get_item_id_by_name(db, "consumable", name.strip())
            if consumable_id:
                consumable_ids_list.append(consumable_id)

    create_order(db, ice_cream_id, topping_ids_list, consumable_ids_list)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/stock")
def read_inventory_page(request: Request, db: Session = Depends(get_db)):
    ice_creams = get_all_ice_creams(db)
    toppings = get_all_toppings(db)
    consumables = get_all_consumables(db)
    inventory_data = {
        "ice_cream": {ic.name: ic.quantity for ic in ice_creams},
        "topping": {tp.name: tp.quantity for tp in toppings},
        "consumable": {cs.name: cs.quantity for cs in consumables},
    }
    return templates.TemplateResponse(
        "stock.html", {"request": request, "inventory_data": inventory_data}
    )


@app.get("/history")
def read_order_history(request: Request, db: Session = Depends(get_db)):
    orders = get_all_orders(db)
    return templates.TemplateResponse(
        "history.html", {"request": request, "orders": orders}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
