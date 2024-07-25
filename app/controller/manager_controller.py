from datetime import datetime, timedelta
import cv2
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from matplotlib.ticker import MultipleLocator
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, JSONResponse, StreamingResponse
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

    # 날짜 형식 변환
    formatted_dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    plt.figure(figsize=(10, 5))

    if dates:
        plt.plot(
            formatted_dates,
            choco_sales,
            label="Choco",
            color="saddlebrown",
            linewidth=3,
        )
        plt.plot(formatted_dates, mint_sales, label="Mint", color="cyan", linewidth=3)
        plt.plot(
            formatted_dates,
            strawberry_sales,
            label="Strawberry",
            color="hotpink",
            linewidth=3,
        )

        for i, date in enumerate(formatted_dates):
            plt.annotate(
                f"{choco_sales[i]}",
                (date, choco_sales[i]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )
            plt.annotate(
                f"{mint_sales[i]}",
                (date, mint_sales[i]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )
            plt.annotate(
                f"{strawberry_sales[i]}",
                (date, strawberry_sales[i]),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
            )

        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.title("Sales by Flavor")
        plt.legend()
        plt.xticks(rotation=45)

        # 5일 간격으로 주요 눈금 설정
        start_date = formatted_dates[0]
        end_date = formatted_dates[-1]
        ticker_dates = [
            start_date + timedelta(days=x)
            for x in range(0, (end_date - start_date).days + 1, 5)
        ]
        ticker_labels = [date.strftime("%m/%d") for date in ticker_dates]

        plt.gca().set_xticks(ticker_dates)
        plt.gca().set_xticklabels(ticker_labels)

        # 작은 눈금 설정
        ax = plt.gca()
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.tick_params(
            which="minor", length=5, direction="inout", bottom=True
        )  # 작은 눈금을 위 방향으로

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
    plt.savefig(png_image, format="png", transparent=False)  # transparent=False로 변경
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


# 카메라 피드 캡처 함수
def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@router.get("/camera_feed", dependencies=[Depends(manager)])
def camera_feed():
    return StreamingResponse(
        gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/camera", dependencies=[Depends(manager)], response_class=HTMLResponse)
def show_camera(request: Request):
    return templates.TemplateResponse("camera.html", {"request": request})
