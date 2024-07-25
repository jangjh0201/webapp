from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from database.database import get_db
from service import order_service, robot_service

router = APIRouter()
templates = Jinja2Templates(directory="app/resource/templates")


@router.get("/")
def show_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/order")
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


@router.post("/order")
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
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.post("/kiosk")
async def add_order_by_kiosk(request: Request, db: Session = Depends(get_db)):
    try:
        result = await order_service.add_order_by_kiosk(await request.json(), db)
        return JSONResponse(status_code=201, content={"order": result})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.post("/robot")
async def add_robot_log(request: Request, db: Session = Depends(get_db)):
    robot_service.add_robot_log(await request.json(), db)
    return JSONResponse(status_code=201, content={"message": "로그가 저장되었습니다."})


@router.post("/test")
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
