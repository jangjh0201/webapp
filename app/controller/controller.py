import sys
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.service import robot_service
from database.database import SessionLocal
from service import item_service, order_service


app = FastAPI()

templates = Jinja2Templates(directory="app/resource/templates")
app.mount("/static", StaticFiles(directory="app/resource/static"), name="static")

db = SessionLocal()


def get_db():
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def show_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/item")
def show_item(request: Request, db: Session = Depends(get_db)):
    ice_creams, toppings, consumables = item_service.show_item(db)
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
    item_service.add_item(item_type, item_name, item_price, item_quantity, db)
    return show_item(request, db)


@app.delete("/item/{item_type}/{item_id}")
def remove_item(item_type: str, item_id: int, db: Session = Depends(get_db)):
    if item_service.remove_item(item_type, item_id, db):
        return {"success": True}
    else:
        return {"success": False}


@app.get("/order")
def show_order(request: Request, db: Session = Depends(get_db)):
    ice_creams, toppings, consumables = order_service.show_order(db)
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
    try:
        order_service.add_order(ice_cream_id, topping_ids, consumable_ids, db)
        return templates.TemplateResponse(
            "index.html", {"request": request, "message": "주문이 완료되었습니다."}
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={"OR": {"detail": e.detail}}
        )


@app.post("/kiosk")
async def add_order_by_kiosk(request: Request, db: Session = Depends(get_db)):
    try:
        result = await order_service.add_order_by_kiosk(await request.json(), db)
        return JSONResponse(status_code=201, content={"OR": result})
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={"OR": {"detail": e.detail}}
        )


@app.post("/robot")
async def add_robot_log(request: Request, db: Session = Depends(get_db)):
    robot_service.add_robot_log(await request.json(), db)
    return JSONResponse(status_code=201, content={"message": "로그가 저장되었습니다."})


@app.get("/log")
def show_logs(request: Request, db: Session = Depends(get_db)):
    logs = robot_service.show_all_logs(db)
    return templates.TemplateResponse("log.html", {"request": request, "logs": logs})


@app.get("/stock")
def show_inventory(request: Request, db: Session = Depends(get_db)):
    ice_creams, toppings, consumables = item_service.show_inventory(db)
    return templates.TemplateResponse(
        "stock.html",
        {
            "request": request,
            "inventory_data": {
                "ice_cream": ice_creams,
                "topping": toppings,
                "consumable": consumables,
            },
        },
    )


@app.get("/history")
def show_history(request: Request, db: Session = Depends(get_db)):
    orders = order_service.show_history(db)
    return templates.TemplateResponse(
        "history.html", {"request": request, "orders": orders}
    )
