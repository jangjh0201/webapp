# main.py

from db import SessionLocal
from db.base import Base
from db.crud import create_inventory_item, get_inventory, record_purchase
from db.models import Inventory

def main():
    # 데이터베이스 연결
    db = SessionLocal()
    
    # 예제 데이터 추가
    create_inventory_item(db, "Vanilla Ice Cream", 23, 2500)
    create_inventory_item(db, "Chocolate Ice Cream", 31, 2500)
    
    # 예제 데이터 조회
    items = db.query(Inventory).all()
    for item in items:
        print(f"ID: {item.id}, Name: {item.item_name}, Quantity: {item.quantity}, Price: {item.price}")

if __name__ == "__main__":
    main()
