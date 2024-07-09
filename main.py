from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn
from crud import ice_cream, inventory, order, other_item, topping
from database import database
from database.database import initialize_tables
from schemas import schemas

initialize_tables()
app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return RedirectResponse(url="/ice_cream/")


# IceCream Endpoints
@app.get("/ice_cream/")
async def get_ice_creams(request: Request, db: Session = Depends(get_db)):
    ice_creams = ice_cream.get_all_ice_creams(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "ice_creams": ice_creams}
    )


@app.post("/ice_cream/")
async def create_ice_cream(
    ice_cream: schemas.IceCreamCreate, db: Session = Depends(get_db)
):
    return ice_cream.create_ice_cream(db, ice_cream.name, ice_cream.price)


@app.delete("/ice_cream/{name}")
async def delete_ice_cream(name: str, db: Session = Depends(get_db)):
    ice_cream.delete_ice_cream_by_name(db, name)
    return {"message": "Ice cream deleted successfully"}


@app.delete("/ice_cream/")
async def delete_all_ice_creams(db: Session = Depends(get_db)):
    ice_cream.delete_all_ice_creams(db)
    return {"message": "All ice creams deleted successfully"}


# Topping Endpoints
@app.get("/topping/")
async def get_toppings(request: Request, db: Session = Depends(get_db)):
    toppings = topping.get_all_toppings(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "toppings": toppings}
    )


@app.post("/topping/")
async def create_topping(topping: schemas.ToppingCreate, db: Session = Depends(get_db)):
    return topping.create_topping(db, topping.name, topping.price)


@app.delete("/topping/{name}")
async def delete_topping(name: str, db: Session = Depends(get_db)):
    topping.delete_topping_by_name(db, name)
    return {"message": "Topping deleted successfully"}


@app.delete("/topping/")
async def delete_all_toppings(db: Session = Depends(get_db)):
    topping.delete_all_toppings(db)
    return {"message": "All toppings deleted successfully"}


# OtherItem Endpoints
@app.get("/other_item/")
async def get_other_items(request: Request, db: Session = Depends(get_db)):
    other_items = other_item.get_all_other_items(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "other_items": other_items}
    )


@app.post("/other_item/")
async def create_other_item(
    other_item: schemas.OtherItemCreate, db: Session = Depends(get_db)
):
    return other_item.create_other_item(db, other_item.name, other_item.price)


@app.delete("/other_item/{name}")
async def delete_other_item(name: str, db: Session = Depends(get_db)):
    other_item.delete_other_item_by_name(db, name)
    return {"message": "Other item deleted successfully"}


@app.delete("/other_item/")
async def delete_all_other_items(db: Session = Depends(get_db)):
    other_item.delete_all_other_items(db)
    return {"message": "All other items deleted successfully"}


# Order Endpoints
@app.get("/order/")
async def get_orders(request: Request, db: Session = Depends(get_db)):
    orders = order.get_all_orders(db)
    return templates.TemplateResponse(
        "order.html", {"request": request, "orders": orders}
    )


@app.post("/order/")
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return order.create_order(
        db, order.ice_cream_id, order.other_item_ids, order.toppings
    )


@app.delete("/order/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_item = order.get_order(db, order_id)
    if order_item is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order.delete_order(db, order_item)
    return {"message": "Order deleted successfully"}


# Inventory Endpoints
@app.get("/inventory/")
async def get_inventory(request: Request, db: Session = Depends(get_db)):
    ice_cream_inventory = inventory.get_inventory_by_item(db, "ice_cream")
    topping_inventory = inventory.get_inventory_by_item(db, "topping")
    other_item_inventory = inventory.get_inventory_by_item(db, "other_item")
    inventory_data = {
        "ice_cream": {item.item.name: item.quantity for item in ice_cream_inventory},
        "topping": {item.item.name: item.quantity for item in topping_inventory},
        "other_item": {item.item.name: item.quantity for item in other_item_inventory},
    }
    return templates.TemplateResponse(
        "inventory.html", {"request": request, "inventory_data": inventory_data}
    )


@app.post("/inventory/")
async def create_inventory_item(
    inventory_item: schemas.InventoryCreate, db: Session = Depends(get_db)
):
    return inventory.create_inventory(
        db, inventory_item.item_type, inventory_item.item_id, inventory_item.quantity
    )


@app.delete("/inventory/{inventory_id}")
async def delete_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    inventory_item = inventory.get_inventory_item(db, inventory_id)
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    inventory.delete_inventory_item(db, inventory_item)
    return {"message": "Inventory item deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
