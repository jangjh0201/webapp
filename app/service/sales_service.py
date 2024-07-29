from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.models import Order, IceCream


def get_sales_data(db: Session):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    one_month_ago = today - timedelta(days=30)

    sales = (
        db.query(Order.order_time, IceCream.name, IceCream.quantity, Order)
        .join(IceCream, Order.ice_cream_id == IceCream.id)
        .filter(Order.order_time <= today)
        .all()
    )

    sales_data = []
    for sale in sales:
        order_time = sale[0]
        if order_time < one_month_ago:
            continue

        total_price = sale[3].ice_cream.price
        for topping in sale[3].toppings:
            total_price += topping.price
        for consumable in sale[3].consumables:
            total_price += consumable.price

        sales_data.append(
            {
                "order_time": order_time.strftime("%Y-%m-%d"),
                "name": sale[1],
                "quantity": sale[2],
                "total_price": total_price,
            }
        )

    return sales_data


def process_data(sales_data):
    choco_sales = {}
    mint_sales = {}
    strawberry_sales = {}

    for sale in sales_data:
        date = sale["order_time"]
        if sale["name"] == "choco":
            if date not in choco_sales:
                choco_sales[date] = 0
            choco_sales[date] += sale["total_price"]
        elif sale["name"] == "mint":
            if date not in mint_sales:
                mint_sales[date] = 0
            mint_sales[date] += sale["total_price"]
        elif sale["name"] == "strawberry":
            if date not in strawberry_sales:
                strawberry_sales[date] = 0
            strawberry_sales[date] += sale["total_price"]

    dates = sorted(
        list(
            set(choco_sales.keys())
            | set(mint_sales.keys())
            | set(strawberry_sales.keys())
        )
    )

    choco_values = [choco_sales.get(date, 0) for date in dates]
    mint_values = [mint_sales.get(date, 0) for date in dates]
    strawberry_values = [strawberry_sales.get(date, 0) for date in dates]

    return dates, choco_values, mint_values, strawberry_values


def process_data_for_volumes(sales_data):
    choco_volumes = {}
    mint_volumes = {}
    strawberry_volumes = {}

    for sale in sales_data:
        date = sale["order_time"]
        quantity = sale["quantity"]
        if sale["name"] == "choco":
            if date not in choco_volumes:
                choco_volumes[date] = 0
            choco_volumes[date] += quantity
        elif sale["name"] == "mint":
            if date not in mint_volumes:
                mint_volumes[date] = 0
            mint_volumes[date] += quantity
        elif sale["name"] == "strawberry":
            if date not in strawberry_volumes:
                strawberry_volumes[date] = 0
            strawberry_volumes[date] += quantity

    dates = sorted(
        list(
            set(choco_volumes.keys())
            | set(mint_volumes.keys())
            | set(strawberry_volumes.keys())
        )
    )

    choco_volume_values = [choco_volumes.get(date, 0) for date in dates]
    mint_volume_values = [mint_volumes.get(date, 0) for date in dates]
    strawberry_volume_values = [strawberry_volumes.get(date, 0) for date in dates]

    return dates, choco_volume_values, mint_volume_values, strawberry_volume_values
