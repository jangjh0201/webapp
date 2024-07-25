from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from database.database import get_db
from service import item_service, robot_service, sales_service, order_service
from auth.auth import manager
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter()
templates = Jinja2Templates(directory="app/resource/templates")


@router.get("/log", dependencies=[Depends(manager)])
def show_logs(request: Request, db: Session = Depends(get_db)):
    logs = robot_service.get_all_logs(db)
    return templates.TemplateResponse("log.html", {"request": request, "logs": logs})


@router.get("/stock", dependencies=[Depends(manager)])
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


@router.get("/history", dependencies=[Depends(manager)])
def show_history(request: Request, db: Session = Depends(get_db)):
    orders = order_service.get_all_histories(db)
    return templates.TemplateResponse(
        "history.html", {"request": request, "orders": orders}
    )


@router.get("/sales", response_class=HTMLResponse, dependencies=[Depends(manager)])
def show_sales(request: Request, db: Session = Depends(get_db)):
    sales_data = sales_service.get_sales_data(db)
    dates, choco_sales, mint_sales, strawberry_sales = sales_service.process_data(
        sales_data
    )

    plt.figure(figsize=(10, 5))

    if dates:
        plt.plot(dates, choco_sales, label="Choco", color="saddlebrown", linewidth=3)
        plt.plot(dates, mint_sales, label="Mint", color="cyan", linewidth=3)
        plt.plot(
            dates, strawberry_sales, label="Strawberry", color="hotpink", linewidth=3
        )

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
        )
        plt.axis("off")

    png_image = io.BytesIO()
    plt.savefig(png_image, format="png", transparent=True)
    png_image_b64_string = "data:image/png;base64," + base64.b64encode(
        png_image.getvalue()
    ).decode("utf8")

    return templates.TemplateResponse(
        "sales.html", {"request": request, "sales_data": png_image_b64_string}
    )


@router.get("/item", dependencies=[Depends(manager)])
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


@router.post("/item", dependencies=[Depends(manager)])
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


@router.delete("/item/{item_type}/{item_id}", dependencies=[Depends(manager)])
def remove_item(item_type: str, item_id: int, db: Session = Depends(get_db)):
    if item_service.remove_item(item_type, item_id, db):
        return {"success": True}
    else:
        return {"success": False}
