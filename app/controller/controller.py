import sys
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.utils import get_item_id_by_name
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
    return item_service.show_item(request, db, templates)


@app.post("/item")
def add_item(
    request: Request,
    item_type: str = Form(...),
    item_name: str = Form(...),
    item_price: int = Form(...),
    item_quantity: int = Form(...),
    db: Session = Depends(get_db),
):
    return item_service.add_item(
        request, item_type, item_name, item_price, item_quantity, db, templates
    )


@app.delete("/item/{item_type}/{item_id}")
def remove_item(item_type: str, item_id: int, db: Session = Depends(get_db)):
    return item_service.remove_item(item_type, item_id, db)


@app.get("/order")
def show_order(request: Request, db: Session = Depends(get_db)):
    return order_service.show_order(request, db, templates)


@app.post("/order")
def add_order(
    request: Request,
    ice_cream_id: int = Form(...),
    topping_ids: str = Form(None),
    consumable_ids: str = Form(None),
    db: Session = Depends(get_db),
):
    return order_service.add_order(
        request, ice_cream_id, topping_ids, consumable_ids, db, templates
    )


@app.post("/kiosk")
async def add_order_by_kiosk(request: Request, db: Session = Depends(get_db)):
    return await order_service.add_order_by_kiosk(request, db)


@app.get("/stock")
def show_inventory(request: Request, db: Session = Depends(get_db)):
    return item_service.show_inventory(request, db, templates)


@app.get("/history")
def show_history(request: Request, db: Session = Depends(get_db)):
    return order_service.show_history(request, db, templates)
