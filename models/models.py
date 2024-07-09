from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class IceCream(Base):
    __tablename__ = "ice_cream"
    id = Column(Float, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)


class Topping(Base):
    __tablename__ = "topping"
    id = Column(Float, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)


class OtherItem(Base):
    __tablename__ = "other_item"
    id = Column(Float, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Float, primary_key=True, index=True)
    item_type = Column(String(50), nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "order"
    id = Column(Float, primary_key=True, index=True)
    ice_cream_id = Column(Integer, nullable=False)
    topping_ids = Column(JSON, nullable=True)
    other_item_ids = Column(JSON, nullable=True)
    order_time = Column(DateTime(timezone=True), server_default=func.now())
