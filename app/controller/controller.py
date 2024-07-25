from datetime import datetime
import io
import sys
import os
import base64
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
import matplotlib.pyplot as plt

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.database import SessionLocal
from service import item_service, order_service, robot_service, sales_service

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
    ice_creams, toppings, consumables = item_service.get_all_items(db)
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
    return item_service.get_all_items(db)


@app.delete("/item/{item_type}/{item_id}")
def remove_item(item_type: str, item_id: int, db: Session = Depends(get_db)):
    if item_service.remove_item(item_type, item_id, db):
        return {"success": True}
    else:
        return {"success": False}


@app.get("/order")
def show_order(request: Request, db: Session = Depends(get_db)):
    ice_creams, toppings, consumables = order_service.get_all_orders(db)
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
    logs = robot_service.get_all_logs(db)
    return templates.TemplateResponse("log.html", {"request": request, "logs": logs})


@app.get("/stock")
def show_inventory(request: Request, db: Session = Depends(get_db)):
    ice_creams, toppings, consumables = item_service.get_all_inventories(db)
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
    orders = order_service.get_all_histories(db)
    return templates.TemplateResponse(
        "history.html", {"request": request, "orders": orders}
    )


@app.get("/sales", response_class=HTMLResponse)
def show_sales(request: Request, db: Session = Depends(get_db)):
    sales_data = sales_service.get_sales_data(db)
    dates, choco_sales, mint_sales, strawberry_sales = sales_service.process_data(
        sales_data
    )

    # 그래프를 그립니다.
    plt.figure(figsize=(10, 5))

    if dates:
        plt.plot(
            dates, choco_sales, label="Choco", color="saddlebrown", linewidth=3
        )  # 선의 굵기 설정
        plt.plot(
            dates, mint_sales, label="Mint", color="cyan", linewidth=3
        )  # 선의 굵기 설정
        plt.plot(
            dates, strawberry_sales, label="Strawberry", color="hotpink", linewidth=3
        )  # 선의 굵기 설정

        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.title("Sales by Flavor")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
    else:
        plt.text(
            0.5,
            0.5,
            "No data available",
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
            fontsize=20,
        )  # 글자 크기 설정
        plt.axis("off")

    # 그래프를 HTML에 삽입할 수 있는 형식으로 변환합니다.
    png_image = io.BytesIO()
    plt.savefig(png_image, format="png", transparent=True)  # 배경을 투명으로 설정
    png_image_b64_string = "data:image/png;base64," + base64.b64encode(
        png_image.getvalue()
    ).decode("utf8")

    return templates.TemplateResponse(
        "sales.html", {"request": request, "sales_data": png_image_b64_string}
    )


@app.post("/test")
async def test_order(request: Request, db: Session = Depends(get_db)):
    try:
        json_data = await request.json()
        order_time = json_data.get("OR", {}).get("order_time")
        result = await order_service.add_order_by_kiosk(json_data, db)
        order_id = result["orderId"]
        order_service.edit_order_time(db, order_id, order_time)
        return JSONResponse(status_code=201, content={"orderId": order_id})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
